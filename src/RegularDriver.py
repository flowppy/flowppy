# -*- coding: utf-8 -*-

import GraphDriver;
import networkx as nx;
import Instruction;

class RegularDriver(GraphDriver.GraphDriver):
    
    def get_name():
        return "regular";
        
    def create_graph(self, instructions_table, vma_instructions_table):
        graph = nx.DiGraph();
            
        start = Instruction.Instruction("-0x1", "-0x1", "\\<start\\>", "\\<start\\>")
        end = Instruction.Instruction("-0x1", "-0x1", "\\<end\\>", "\\<end\\>")
        instructions_table.insert(0,start);
        instructions_table.append(end);
        for i in range(len(instructions_table)):
            if (i != 0):
                graph.add_edge("\"" + instructions_table[i-1].create_string() + "\"", "\"" + instructions_table[i].create_string() + "\"");
                
            instruction = instructions_table[i];
            if super(RegularDriver, self).is_jump(instruction):
                targetVma = instruction.operands[0].ascii;
                graph.add_edge("\"" + instruction.create_string() + "\"", "\"" + vma_instructions_table[int(targetVma, 0)].create_string() + "\"");
        return graph;
