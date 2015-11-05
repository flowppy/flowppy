# -*- coding: utf-8 -*-

import GraphDriver;
import networkx as nx;

class CondensedDriver(GraphDriver.GraphDriver):
    
    def get_name(self):
        return "condensed";
        
    def create_graph(self, instructions_table, vma_instructions_table):
        pass;
