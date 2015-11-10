# -*- coding: utf-8 -*-

class Bloc(object):
    
    def __init__(self, vma):
        self.etiquette = vma;
        self.instruction = "";
        
        self.blocSonLeft = None;
        self.blocSonRight = None;
        
    def setSon(self, bloc):
        if self.blocSonLeft is not None:
            self.blocSonRight = bloc; 
        else:
            self.blocSonLeft = bloc;
        
    def addInstruction(self, instruction):
        self.instruction = self.instruction + instruction.create_string() + "\n";
        
    def get_graph(self, graph):
        if self.blocSonLeft is not None:
            graph.add_edge(self.instruction, self.blocSonLeft.instruction);
            self.blocSonLeft.get_graph(graph);
        if self.blocSonRight is not None:
            graph.add_edge(self.instruction, self.blocSonRight.instruction);
            self.blocSonRight.get_graph(graph);
        return graph;
        