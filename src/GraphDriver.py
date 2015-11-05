# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class GraphDriver:

    JUMPS_X86 = ["jo", "jno", "js", "jns", "je", "jz", "jne", "jnz", "jb", "jnae", "jc", "jnb", "jae", "jnc", "jbe", "jna", "ja", "jnbe", "jl", "jnge", "jge", "jnl", "jle", "jng", "jg", "jnle", "jp", "jpe", "jlp", "jpo", "jcxz", "jecxz"];
    
    def __init__(self, outputmanager):
        __metaclass__ = ABCMeta;
    
        self.outputManager = outputmanager;
        
    @abstractmethod
    def get_name(self): pass;
    
    @abstractmethod
    def create_graph(self, instructions_table, vma_instructions_table): pass;
