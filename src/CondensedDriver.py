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
        #Création d'un bloc de départ
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
                    bloc_cur.addInstruction(cur_inst);#Recupération instruction actuelle
                    classed_list[int(cur_inst.vma, 0)] = bloc_cur; #Ajout en classed_List, pour pouvoir retrouverle bloc
                    Bloc_tmp = classed_list[int(cur_inst.operands[0].ascii, 0)]; #Récupération du bloc cible du jump
                    
                    if not Bloc_tmp.is_empty(): # Verification de consistance du bloc
                        
                        #pointer vers un bloc déjà créé plus haut sur le graphe
                        if int(cur_inst.operands[0].ascii,0) in Bloc_tmp.getVMAInstruction():
                           
                            bloc_cur.addSon(Bloc_tmp); # Ajout du bloc_Tmp aux fils du bloc courant
                            Bloc_tmp=Bloc.Bloc( instructions_table[i]);# Ajout courant des blocs et passage au suivant
                            bloc_cur.addSon(Bloc_tmp);
                            classed_list[int(cur_inst.vma, 0)] = bloc_cur;
                            waiting_list[int(cur_inst.operands[0].ascii, 0)] = bloc_cur;
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
                    bloc_tmp = Bloc.Bloc("function");
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
            
        end = Instruction.Instruction("-0x1", "-0x1", "\\<end\\>", "\\<end\\>")
        blocEnd = Bloc.Bloc(end.vma);
        blocEnd.addInstruction(end);
        bloc_cur.addSon(blocEnd);
        
        bloc_origin.clean_empty_bloc();
        graph = nx.DiGraph();
        graph = bloc_origin.get_graph(graph, self);
        
        return graph;




