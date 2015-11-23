# -*- coding: utf-8 -*-

class Instruction:
    def __init__(self, offset, vma, ascii, mnemonic):
        self.offset = offset;
        self.vma = vma;
        self.ascii = ascii;
        self.mnemonic = mnemonic;
        self.operands = [];
        
    def add_operand(self, operand):
        self.operands.append(operand);
        
    def create_string(self):
        prefix = "";
        if int(self.offset, 0) != -1:
            prefix = "[" + self.offset + " (" + self.vma + ")] ";
        return prefix + self.ascii;
