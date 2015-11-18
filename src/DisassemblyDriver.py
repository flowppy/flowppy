# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod;
import re;
import abstractclassmethod;

class DisassemblyDriver(object):
    
    def __init__(self):
        __metaclass__ = ABCMeta; 
        
        #Compilation des regexes
        self.compiled_jumps_regexes = [];
        for regex in self.get_jumps_regexes():
            self.compiled_jumps_regexes.append(re.compile(regex));
        
    #Méthode pour désassembler à partir d'un fichier
    #renvoie un tuple (instructions_table, vma_instructions_table)
    @abstractmethod
    def disassemble(self, filename): pass;
    
    #Méthode pour récupérer la liste des regexes
    @abstractmethod
    def get_jumps_regexes(self): pass;
    
    @abstractclassmethod.abstractclassmethod
    def get_name(): pass;
    
    @abstractmethod
    def get_dependencies(self): pass;

        
