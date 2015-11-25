# -*- coding: utf-8 -*-

class Bloc(object):
    
    def __init__(self, vma):
        self.etiquette = vma;
        self.instruction = [];
        self.passedR = False;
        self.passedL = False;
        #ajout d'un attribut de Graphdriver
        
        self.blocSonLeft = None;
        self.blocSonRight = None;
        self.dad = None;
        self.is_clean = False;
        
    def addSon(self, bloc):
        if self.blocSonLeft is None:
            self.blocSonLeft = bloc;
            self.blocSonLeft.dad = self;
        elif self.blocSonRight is None:
            self.blocSonRight = bloc;
            self.blocSonRight.dad = self;
        
    def addInstruction(self, instruction):
        self.instruction.append(instruction);

    def getParent(self):
        return self.dad;

    def getSon(self):
            if self.blocSonLeft is not None:
                return self.blocSonLeft;
            if self.blocSonRight is not None:
                return self.blocSonRight;
            return self;


    def instructionStr(self, driver):
        #mettre un if si l'instruction conerne un jumps pour concaténer le offset et l'adresse cible du jump.
        #à voir si on peut appeler la methode is_jump() à partir d'ici
        str = "";
        line =0;
        for i in range (0,len(self.instruction)-1):
            #if(self.driver.is_jump(inst)){ ajout du offset}
            str = str  + self.instruction[i].create_string()+ "\l";
            line = 1;
        if len(self.instruction) >0:
            if not (driver.is_jump(self.instruction[len(self.instruction)-1])) and not self.instruction[len(self.instruction)-1].mnemonic == "callq":
                str = str  +self.instruction[len(self.instruction)-1].create_string()+ "\l";
    
            if(line==0):
                    str= self.instruction[0].ascii
        else:
            self.dad.replaceSon(self,self.blocSonLeft);
      
            
        return str;
        
    def getVMAInstruction(self):
        instruction=[];
        for xx in self.instruction:
            instruction.append(int(xx.vma,0));
            
        return instruction;
            
    def replaceSon(self, bloc1, bloc2):
        #bloc1 is the future new son of the current bloc
        #bloc2 is the the bloc to replace
        if self.blocSonLeft == bloc2:
            self.blocSonLeft = bloc1; 
        elif self.blocSonRight == bloc2:
            self.blocSonRight = bloc1;
        elif self.blocSonLeft is None:
            self.blocSonLeft = bloc1; 
        elif self.blocSonRight is None:
            self.blocSonRight = bloc1;
        
    def get_graph(self, graph, driver):
        #Passed mark
        #inst_length =len(self.instruction)-2;
        label_str=" ";
        label_str2=" ";
        """
        Condition première
        """
        
        if self.blocSonLeft is not None and not self.passedL:
            if driver.is_jump(self.instruction[len(self.instruction)-1]) :
                if int(self.instruction[len(self.instruction)-1].operands[0].ascii,0) >= int(self.blocSonLeft.instruction[0].vma,0):
            
                    label_str = self.instruction[len(self.instruction)-1].create_string();
            elif self.instruction[len(self.instruction)-1].mnemonic == "callq" :
                label_str = self.instruction[len(self.instruction)-1].create_string();
            elif not(len(self.instruction)>0):
                self.dad.replaceSon(self,self.blocSonLeft);
                
            
            self.passedL = True;
            
            
            graph = self.blocSonLeft.get_graph(graph, driver);
            
            graph.add_edge(self.instructionStr(driver), self.blocSonLeft.instructionStr(driver), label = label_str);
        """
        Condition seconde
        """
        if self.blocSonRight is not None and not self.passedR:
            if driver.is_jump(self.instruction[len(self.instruction)-1]):
                if int(self.instruction[len(self.instruction)-1].operands[0].ascii,0) >= int(self.blocSonRight.instruction[0].vma,0):
                    
                    label_str2 = self.instruction[len(self.instruction)-1].create_string();
            elif self.instruction[len(self.instruction)-1].mnemonic == "callq":
                label_str2 = self.instruction[len(self.instruction)-1].create_string();
            elif not(len(self.instruction)>0):
                self.dad.replaceSon(self,self.blocSonLeft);
            
            self.passedR = True;
            
            graph = self.blocSonRight.get_graph(graph, driver);
            
            graph.add_edge(self.instructionStr(driver), self.blocSonRight.instructionStr(driver), label = label_str2);
        return graph;
        
        
        
    def is_empty(self):
        return (len(self.instruction) == 0);
        
    def clean_empty_bloc(self):
        if(not self.is_clean):
            if(self.is_empty()):
                if(self.blocSonLeft is not None):
                    self.dad.replaceSon(self.blocSonLeft,self);
            self.is_clean = True;
            if(self.blocSonLeft is not None):
                self.blocSonLeft.clean_empty_bloc();
            if(self.blocSonRight):
                self.blocSonRight.clean_empty_bloc();
        
        