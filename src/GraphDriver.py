# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import re;

class GraphDriver(object):

    JUMPS_REGEX_LIST = [
        "je?cxz|jpo|jn[abgl]e|j[abglp]e|jn?[abceglopsz]" #x86-64
    ];
    
    def __init__(self, outputmanager):
        __metaclass__ = ABCMeta;
        self.outputManager = outputmanager;
        
    @abstractmethod
    def get_name(self): pass;
    
    @abstractmethod
    def create_graph(self, instructions_table, vma_instructions_table): pass;
    
    def is_jump(self, instruction):
        for regex in self.JUMPS_REGEX_LIST:
            if re.match(regex, instruction.mnemonic):
                return True;    
        return False;    
