# -*- coding: utf-8 -*-

class Bloc(object):
    
    def __init__(self, vma):
        self.etiquette = vma;
        self.instruction = [];
        self.passedR = False;
        self.passedL = False;
        
        self.blocSonLeft = None;
        self.blocSonRight = None;
        
    def addSon(self, bloc):
        if self.blocSonLeft is None:
            self.blocSonLeft = bloc; 
        elif self.blocSonRight is None:
            self.blocSonRight = bloc;
        
    def addInstruction(self, instruction):
        self.instruction.append(instruction);
        
    def containsInstruction(self, instruction):
        for xx in self.instruction:
            if(int(xx.vma,0) == int(instruction,0)):
                return True;
        return False;
    
    def getParent(self, bloc_nimp):
        if self.blocSonLeft == bloc_nimp:
            return self;
        if self.blocSonRight == bloc_nimp:
            return self;
        else:
            if self.blocSonLeft is not None:
                return self.blocSonLeft.getParent(bloc_nimp);
            if self.blocSonRight is not None:
                return self.blocSonRight.getParent(bloc_nimp);
            return self;
            
    def getBloc(self, instruction):
        if(self.containsInstruction(instruction)):
            return self;
        else:
            if self.blocSonLeft is not None:
                return self.blocSonLeft.getBloc(instruction)
            if self.blocSonRight is not None:
                return self.blocSonRight.getBloc(instruction)
            return self;
            
    def getSon(self):
            if self.blocSonLeft is not None:
                return self.blocSonLeft;
            if self.blocSonRight is not None:
                return self.blocSonRight;
            return self;


    def instructionStr(self):
        str = "";
        for inst in self.instruction:
            str = str  + inst.create_string()+ "\l";
        return str;
    def replaceSon(self, bloc1, bloc2):
        if self.blocSonLeft == bloc2:
            self.blocSonLeft = bloc1; 
        elif self.blocSonRight == bloc2:
            self.blocSonRight = bloc1;
        elif self.blocSonLeft is None:
            self.blocSonLeft = bloc1; 
        elif self.blocSonRight is None:
            self.blocSonRight = bloc1;
        
    def get_graph(self, graph):
        #Passed mark
        if self.blocSonLeft is not None and not self.passedL:
            self.passedL = True;
            graph = self.blocSonLeft.get_graph(graph);
            graph.add_edge(self.instructionStr(), self.blocSonLeft.instructionStr());
        if self.blocSonRight is not None and not self.passedR:
            self.passedR = True;
            graph = self.blocSonRight.get_graph(graph);
            graph.add_edge(self.instructionStr(), self.blocSonRight.instructionStr());
        
            
        return graph;
        