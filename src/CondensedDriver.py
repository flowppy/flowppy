# -*- coding: utf-8 -*-

import GraphDriver;
import networkx as nx;
import Bloc;

class CondensedDriver(GraphDriver.GraphDriver):
    
    def get_name():
        return "condensed";
        
    def create_graph(self, instructions_table, vma_instructions_table):
        waiting_list = {};
        i = 0;
        bloc = Bloc.Bloc(instructions_table[i].vma);
        bloc_origin = bloc;
        while(i <= len(instructions_table)-1):
            cur_inst = instructions_table[i];
            if(super(CondensedDriver, self).is_jump(cur_inst)):
                bloc2 = Bloc.Bloc(cur_inst.vma);
                bloc.addSon(bloc2);
                waiting_list[int(bloc2.etiquette, 0)] = bloc2;
            else:
                if(cur_inst.vma in waiting_list):
                    bloc2 = waiting_list[cur_inst.vma];
                    bloc.addSon(bloc2);
                    bloc = bloc2;
                else:
                    if(cur_inst.ascii is "retq"): #TODO Changer le retq
                        bloc2 = Bloc.Bloc(cur_inst.vma);
                        bloc.addSon(bloc2);
                        bloc = bloc2;
                    else:
                        bloc.addInstruction(cur_inst);
            i = i+1;
            
        graph = nx.DiGraph();
        graph = bloc_origin.get_graph(graph);
        
        return graph;



