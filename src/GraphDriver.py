# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class GraphDriver:
    
    def __init__(self, outputmanager):
        __metaclass__ = ABCMeta
    
        self.outputManager = outputmanager;
        
    @abstractmethod
    def get_name(self): pass;
    
    @abstractmethod
    def create_graph(self, xmldocument): pass;
