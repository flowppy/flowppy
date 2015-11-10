# -*- coding: utf-8 -*-

class Bloc:
    
    def __init__(self, vma):
        self.etiquette = vma;
        self.instruction = "";
        
        
    def setSon(bloc):
        if(self.blocSonLeft != null):
            self.blocSonRight = bloc; 
        else:
            self.blocSonLeft = bloc;
        
    def addInstruction(instruction):
        self.instruction = self.instruction + instruction.create_string() + "\n";
        
    def get_graph(self, graph):
        if(self.blocSonLeft != null):
            graph.add_edge(self.instruciton, self.blocSonLeft.instruction);
            self.blocSonLeft.get_graph(graph);
        if(self.blocSonRight != null):
            graph.add_edge(self.instruciton, self.blocSonRight.instruction);
            self.blocSonRight.get_graph(graph);
        return graph;
        