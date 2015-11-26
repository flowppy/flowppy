# -*- coding: utf-8 -*-

import sys;

class OutputManager:

    def __init__(self, quiet_mode):
        self.quiet_mode = quiet_mode;
        
    #Affiche un message dans stdout
    def print_message(self, *messages):
        if not self.quiet_mode:
            print("INFO:", *messages);
    
    #Affiche une erreur dans stderr
    def print_error(self, *messages):
        if not self.quiet_mode:
            print("ERROR:", *messages, file = sys.stderr);
