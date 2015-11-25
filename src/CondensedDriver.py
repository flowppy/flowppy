# -*- coding: utf-8 -*-

import GraphDriver;
import networkx as nx;
import Bloc;
import Instruction;


class CondensedDriver(GraphDriver.GraphDriver):
    
    def get_name():
        return "condensed";
        
    def create_graph(self, instructions_table, vma_instructions_table):
        waiting_list = {};
        classed_list = {};
        i = 0;
        start = Instruction.Instruction("-0x1", "-0x1", "\\<start\\>", "\\<start\\>")
        blocStart = Bloc.Bloc(start.vma);
        blocStart.addInstruction(start);
        bloc_cur = Bloc.Bloc(instructions_table[0].vma);
        bloc_origin = blocStart;
        blocStart.addSon(bloc_cur);

        
        while(i <= len(instructions_table)-1):
            cur_inst = instructions_table[i];
            
            
            if(super(CondensedDriver, self).is_jump(cur_inst)):
                #condition pour faire remonter l'adresse cible d'un jump vers un bloc déjà créé
                if(int(cur_inst.operands[0].ascii, 0)<int(cur_inst.vma,0)):#
                    # DONE utilisation d'une table de hachage. Maintenant tu travaille l'algo pour les retQ xD
                    bloc_cur.addInstruction(cur_inst);
                    classed_list[int(cur_inst.vma, 0)] = bloc_cur;
                    bloc_tmp = classed_list[int(cur_inst.operands[0].ascii, 0)];
                    
                    if not len(bloc_tmp.instruction)==0:
                        
                        Bloc_mid1 = Bloc.Bloc("Bloc1");
                        Bloc_mid2 = Bloc.Bloc("Bloc2");
                        if int(cur_inst.operands[0].ascii,0) in bloc_tmp.getVMAInstruction():
                            instructionList= bloc_tmp.getVMAInstruction();
                            i=0;
                            while (not (int(bloc_tmp.instruction[i].vma,0) == int(cur_inst.operands[0].ascii,0))) :
                                i=i+1;
                            list1 = bloc_tmp.instruction[:i-1];
                            list2 = bloc_tmp.instruction[len(bloc_tmp.instruction)-(i-1):];
                            for xl1 in list1:
                                Bloc_mid1.addInstruction(xl1);
                            for xl2 in list1:
                                Bloc_mid2.addInstruction(xl2);
                            bloc_tmp.getParent().addSon(Bloc_mid1);
                            Bloc_mid1.addSon(Bloc_mid2)
                            bloc_cur.addSon(Bloc_mid2);
                            Bloc_mid2.addSon(bloc_tmp.getSon());
                           
                            
                            Bloc_tmp=Bloc.Bloc( instructions_table[i]);
                            bloc_cur.addSon(Bloc_tmp);
                            classed_list[int(cur_inst.vma, 0)] = bloc_cur;
                            waiting_list[int(cur_inst.operands[0].ascii, 0)] = bloc_cur;
                            bloc_cur = Bloc_tmp;
                        else: 
                            bloc_cur = Bloc_tmp;

                else:
                    bloc_cur.addInstruction(cur_inst);
                    classed_list[int(cur_inst.vma, 0)] = bloc_cur;
                    Bloc_tmp=Bloc.Bloc( instructions_table[i]);
                    bloc_cur.addSon(Bloc_tmp);
                    waiting_list[int(cur_inst.operands[0].ascii, 0)] = bloc_cur;
                    bloc_cur = Bloc_tmp;
                    
            elif(cur_inst.mnemonic == "callq"): #Detection des calls de fonction
                    bloc_cur.addInstruction(cur_inst); 
                    classed_list[int(cur_inst.vma, 0)] = bloc_cur;
                    bloc_tmp = Bloc.Bloc("nawak");
                    str = "\\<function at "+ cur_inst.operands[0].ascii + "\\>";
                    bloc_tmp.addInstruction(Instruction.Instruction("-0x1 ", "0x0", str, "function"));
                    bloc_cur.addSon(bloc_tmp);
                    bloc_cur = Bloc.Bloc("");
                    bloc_tmp.addSon(bloc_cur);
                
            else:
                if(int(cur_inst.vma,0) in waiting_list):
                    #print(waiting_list[int(cur_inst.vma, 0)]);
                    classed_list[int(cur_inst.vma, 0)] = bloc_cur;
                    bloc_tmp=Bloc.Bloc(cur_inst);
                    waiting_list[int(cur_inst.vma, 0)].addSon(bloc_tmp);
                    bloc_cur.addSon(bloc_tmp);
                    bloc_cur = bloc_tmp;
                
                else:
                    bloc_cur.addInstruction(cur_inst);
                    classed_list[int(cur_inst.vma, 0)] = bloc_cur;
            i = i+1;
            
        bloc_origin.clean_empty_bloc();
        graph = nx.DiGraph();
        graph = bloc_origin.get_graph(graph, self);
        
        return graph;




