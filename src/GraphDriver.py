# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod;
import re;
import abstractclassmethod;

class GraphDriver(object):
    
    def __init__(self, outputmanager, disassemblerDriver):
        __metaclass__ = ABCMeta;
        self.outputManager = outputmanager;
        self.disassemblerDriver = disassemblerDriver;
        
    @abstractclassmethod.abstractclassmethod
    def get_name(): pass;
    
    @abstractmethod
    def create_graph(self, instructions_table, vma_instructions_table): pass;
    
    def is_jump(self, instruction):
        for regex in self.disassemblerDriver.compiled_jumps_regexes:
            if regex.match(instruction.mnemonic):
                return True;    
        return False;    
