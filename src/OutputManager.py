# -*- coding: utf-8 -*-

class OutputManager:

    def __init__(self, quiet_mode):
        self.quiet_mode = quiet_mode;
        
    def print_message(self, message):
        if not self.quiet_mode:
            print(message);
