# -*- coding: utf-8 -*-

class Bloc(object):
    
    def __init__(self, vma):
        self.etiquette = vma;
        self.instruction = "";
        
        self.blocSonLeft = None;
        self.blocSonRight = None;
        
    def setSon(self, bloc):
        if self.blocSonLeft is None:
            self.blocSonRight = bloc; 
        else:
            self.blocSonLeft = bloc;
        
    def addInstruction(self, instruction):
        self.instruction = self.instruction + instruction.create_string() + "\n";
        
    def toString(self):
        text = self.instruction;
        if self.blocSonLeft:
            text += self.blocSonLeft.instruction;
        if self.blocSonRight:
            text += self.blocSonRight.instruction;
        return text;
        
    def get_graph(self, graph):
        if self.blocSonLeft:
            graph2 = self.blocSonLeft.get_graph(graph);
            graph.add_edge(self.instruction, graph2);
        if self.blocSonRight:
            graph2 = self.blocSonRight.get_graph(graph);
            graph.add_edge(self.instruction, graph2);
        return graph;
        