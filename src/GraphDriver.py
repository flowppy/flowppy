# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod;
import re;
import abstractclassmethod;

class GraphDriver(object):
    
    def __init__(self, outputmanager, disassemblerDriver):
        __metaclass__ = ABCMeta;
        self.outputManager = outputmanager;
        self.disassemblerDriver = disassemblerDriver;
        
    #Méthode abstraite et statique pour obtenir le nom du driver
    @abstractclassmethod.abstractclassmethod
    def get_name(): pass;
    
    #Méthode qui crée le graphe
    @abstractmethod
    def create_graph(self, instructions_table, vma_instructions_table): pass;
    
    #Méthode qui fait le pont entre le driver de graphe et le graphe de désassemblage
    #pour savoir si une instructione est un saut
    def is_jump(self, instruction):
        return self.disassemblerDriver.is_jump(instruction);
