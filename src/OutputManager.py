# -*- coding: utf-8 -*-

import sys;

class OutputManager:

    def __init__(self, quiet_mode):
        self.quiet_mode = quiet_mode;
        
    def print_message(self, *messages):
        if not self.quiet_mode:
            print("INFO:", *messages);
    
    def print_error(self, *messages):
        if not self.quiet_mode:
            print("ERROR:", *messages, file = sys.stderr);
