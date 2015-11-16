# -*- coding: utf-8 -*-

class Bloc(object):
    
    def __init__(self, vma):
        self.etiquette = vma;
        self.instruction = "";
        
        self.blocSonLeft = None;
        self.blocSonRight = None;
        
    def addSon(self, bloc):
        if self.blocSonLeft is None:
            self.blocSonLeft = bloc; 
        elif self.blocSonRight is None:
            self.blocSonRight = bloc;
        
    def addInstruction(self, instruction):
        self.instruction = self.instruction + instruction.create_string() + "\n";
        
    def get_graph(self, graph):
        if self.blocSonLeft is not None:
            graph = self.blocSonLeft.get_graph(graph);
            graph.add_edge(self.instruction, self.blocSonLeft.instruction);
        if self.blocSonRight is not None:
            graph = self.blocSonRight.get_graph(graph);
            graph.add_edge(self.instruction, self.blocSonRight.instruction);
            
        return graph;
        