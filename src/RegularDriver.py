# -*- coding: utf-8 -*-

import GraphDriver;
import networkx as nx;

class RegularDriver(GraphDriver.GraphDriver):
    
    def get_name(self):
        return "regular";
        
    def create_graph(self, instructions_table, vma_instructions_table):
        graph = nx.DiGraph();
        
        for i in range(len(instructions_table)):
            if (i != 0):
                instruction_string = instructions_table[i-1].create_string();
                graph.add_edge(instruction_string, instruction_string);
                
            instruction = instructions_table[i];
            if self.is_jump(instruction):
                targetVma = instruction.operands[0].ascii;
                graph.add_edge(instruction.create_string(), vma_instructions_table[int(targetVma, 0)].create_string());
        return graph;
