# -*- coding: utf-8 -*-

import GraphDriver;
import networkx as nx;

class CondensedDriver(GraphDriver.GraphDriver):
    
    def get_name(self):
        return "condensed";
        
    def create_graph(self, instructions_table, vma_instructions_table):
        waiting_list = [];
        i = 0;
        bloc = Bloc(intruction_table[i].vma);
        bloc_origin = bloc;
        while(i <= len(instructions_table)-1):
            i++;
            cur_inst =instruction_table[i];
            if(is_jump(self, cur_inst)):
                bloc2 = Bloc(cur_inst.vma);
                bloc.setSon(bloc2);
                waiting_list.append(bloc2.etiquette : bloc2);
            else:
                if(cur_inst.vma in waiting_list):
                    bloc2 = waiting_list[cur_inst.vma];
                    bloc.addSon(bloc2);
                    bloc = bloc2;
                else:
                    if(cur_inst.ascii is "retq"):
                        bloc2 = Bloc(cur_inst.vma);
                        bloc.addSon(bloc2);
                        bloc = bloc2;
                    else:
                        bloc.addInstruction(cur_inst.create_string());
        graph= nx.DiGraph();
        return bloc_origin.get_graph(graph);
