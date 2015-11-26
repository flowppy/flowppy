# -*- coding: utf-8 -*-

class Instruction:
    def __init__(self, offset, vma, ascii, mnemonic):
        self.offset = offset;
        self.vma = vma;
        self.ascii = ascii;
        self.mnemonic = mnemonic;
        self.operands = [];
        
    #Ajoute une opérande à l'instruction
    def add_operand(self, operand):
        self.operands.append(operand);
        
    #Renvoie une représentation sous forme de String de l'instruction
    #pour l'affichage
    def create_string(self):
        prefix = "";
        if int(self.offset, 0) != -1:
            prefix = "[" + self.offset + " (" + self.vma + ")] ";
        return prefix + self.ascii;
