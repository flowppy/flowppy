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
        
        
        #Ajout d'un fils au noeud courant
    def addSon(self, bloc):
        if self.blocSonLeft is None:
            self.blocSonLeft = bloc;
            self.blocSonLeft.dad = self;
        elif self.blocSonRight is None:
            self.blocSonRight = bloc;
            self.blocSonRight.dad = self;
        
        #Ajout d'une instruction au bloc courant
    def addInstruction(self, instruction):
        self.instruction.append(instruction);

        #getter de Dad
    def getParent(self):
        return self.dad;
        
        
        #getter de fils (le premier)
    def getSon(self):
            if self.blocSonLeft is not None:
                return self.blocSonLeft;
            if self.blocSonRight is not None:
                return self.blocSonRight;
            return self;

    #Création des étiquettes d'instruction avec prise en charge des blocs artificiels start et end, plus génération des blocs fonctions, réponse aux callq
    def instructionStr(self, driver):
        str = "";
        line =0;
        for i in range (0,len(self.instruction)-2):
            #if(self.driver.is_jump(inst)){ ajout du offset}
            str = str  + self.instruction[i].create_string()+ "\\n";
            line = 1;
        if len(self.instruction) >0:
                str = str  +self.instruction[len(self.instruction)-1].create_string();
        else:
            self.dad.replaceSon(self,self.blocSonLeft);
      
            
        return str;
        
        #Getter tableau d'instructions
    def getVMAInstruction(self):
        instruction=[];
        for xx in self.instruction:
            instruction.append(int(xx.vma,0));
            
        return instruction;
            
         #Methode de remplacement d'un fils du bloc courant   
    def replaceSon(self, bloc1, bloc2):
        #bloc1 est le nouveau fils
        #bloc2 est le fils a remplacer
        if self.blocSonLeft == bloc2:
            self.blocSonLeft = bloc1; 
        elif self.blocSonRight == bloc2:
            self.blocSonRight = bloc1;
        elif self.blocSonLeft is None:
            self.blocSonLeft = bloc1; 
        elif self.blocSonRight is None:
            self.blocSonRight = bloc1;
        
        
        
    def getJumpFlag(self,instruction):
        if instruction.mnemonic == "je":
            return "ZF == 1",
        if instruction.mnemonic == "jne":
            return "ZF == 0"
        if instruction.mnemonic == "jg":
            return "(ZF == 0) AND (SF == OF)"
        if instruction.mnemonic == "jge":
            return "SF == OF"
        if instruction.mnemonic == "jl":
            return "SF ≠ OF"
        if instruction.mnemonic == "jle":
            return "(ZF == 1) OR (SF ≠ OF)"
        if instruction.mnemonic == "ja":
            return "(CF == 0) AND (ZF == 0)","(CF == 0) AND (ZF == 0)"
        if instruction.mnemonic == "jae":
            return "CF == 0"
        if instruction.mnemonic == "jb":
            return "CF == 1"
        if instruction.mnemonic == "jbe":
            return "(CF == 1) OR (ZF == 1)"
        if instruction.mnemonic == "jo":
            return "OF == 1"
        if instruction.mnemonic == "jno":
            return "OF == 0"
        if instruction.mnemonic == "jc":
            return "CF == 1"
        if instruction.mnemonic == "jnc":
            return "CF == 0"
        if instruction.mnemonic == "js":
            return "SF == 1"
        if instruction.mnemonic == "jns":
            return "SF == 0"
        if instruction.mnemonic == "jz":
            return "ZF == 1"
        if instruction.mnemonic == "jnz":
            return "ZF == 0"
        return "Unknow Jump"
        
        
    
        
        #Méthode de création du graph
    def get_graph(self, graph, driver):
        #Passed mark
        label_str="";
        label_str2="";
        """
        Condition Gauche:
        
        Ici, travail recursif sur l'arbre, meme chose du coté droit. Condition pour eviter de tourner infinimment dans l'arbre,
        et pour que les etiquettes de jump n'apparaissent que sur les liens concernés.
        """
        if self.blocSonLeft is not None and not self.passedL:
            if driver.is_jump(self.instruction[len(self.instruction)-1]) :
                if int(self.instruction[len(self.instruction)-1].operands[0].ascii,0) >= int(self.blocSonLeft.instruction[0].vma,0):
            
                    label_str,label_str2 = Bloc.getJumpFlag(self,self.instruction[len(self.instruction)-1]);
            elif not(len(self.instruction)>0):
                self.dad.replaceSon(self,self.blocSonLeft);
            
                
            
            self.passedL = True;
            
            
            graph = self.blocSonLeft.get_graph(graph, driver);
            
            graph.add_edge("\"" + self.instructionStr(driver)+ "\"" ,"\"" + self.blocSonLeft.instructionStr(driver)+ "\"", label = "\""+label_str+"\"");
        """
        Condition Droite
        """
        if self.blocSonRight is not None and not self.passedR:
            if driver.is_jump(self.instruction[len(self.instruction)-1]):
                if int(self.instruction[len(self.instruction)-1].operands[0].ascii,0) >= int(self.blocSonRight.instruction[0].vma,0):
                    
                    label_str2 = Bloc.getJumpFlag(self,self.instruction[len(self.instruction)-1]);
            elif not(len(self.instruction)>0):
                self.dad.replaceSon(self,self.blocSonLeft);

            
            self.passedR = True;
            graph = self.blocSonRight.get_graph(graph, driver);
            
            graph.add_edge("\"" + self.instructionStr(driver)+ "\"", "\"" + self.blocSonRight.instructionStr(driver) + "\"", label = "\""+label_str2+"\"");
        return graph;
        
        
        #Verification du contenu du bloc courant
    def is_empty(self):
        return (len(self.instruction) == 0);
        
        # Nettoyage du graphe pour supprimer les blocs vides
        #TODO Handle delete of "ghost" blocs
    def clean_empty_bloc(self):
        if(not self.is_clean):
            if(self.is_empty()):
                if(self.blocSonLeft is not None):
                    self.dad.replaceSon(self.blocSonLeft,self);
                else:
                     self.dad.replaceSon(self.blocSonRight,self);
            self.is_clean = True;
            if(self.dad is None):
                if(self.blocSonLeft is None and self.blocSonRight is None):
                    self = None;
            if(self.blocSonLeft is not None):
                self.blocSonLeft.clean_empty_bloc();
            if(self.blocSonRight is not None):
                self.blocSonRight.clean_empty_bloc();
            