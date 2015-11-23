# -*- coding: utf-8 -*-

import DisassemblyDriver;
import Instruction;
import Operand;
from xml.dom.minidom import parseString;
import subprocess;

class OpdisDriver(DisassemblyDriver.DisassemblyDriver):
    
    def get_jumps_regexes(self): 
        return [
            "je?cxz|jpo|jn[abgl]e|j[abglp]e|jn?[abceglopsz]" #x86-64
        ];
        
    def get_name():
        return "opdis";
        
    def get_dependencies(self):
        return [
            "opdis"
        ];
        
    def disassemble(self, filename):
        #Exécution d'opdis et récupération du XML
        xml = subprocess.Popen(["opdis", "-q", "-d", "-f", "xml", "-S", ".text", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.read();
        document = parseString(xml).documentElement;   
        
        #Création de la liste des instructions
        instructions_table = [];
        vma_instructions_table = {};
        
        for instructionNode in document.getElementsByTagName("instruction"):
            instruction = Instruction.Instruction(
                self.get_xml_child_value(instructionNode, "offset"),
                self.get_xml_child_value(instructionNode, "vma"),
                self.get_xml_child_value(instructionNode, "ascii"),
                self.get_xml_child_value(instructionNode, "mnemonic")
            );
            
            if (self.xml_node_has_child(instructionNode, "operands")):
                for operandNode in instructionNode.getElementsByTagName("operand"):
                    operand = Operand.Operand(
                        operandNode.attributes["name"],
                        self.get_xml_child_value(operandNode, "ascii")
                    );
                    instruction.add_operand(operand);
                    
            instructions_table.append(instruction);
            vma_instructions_table[int(instruction.vma, 0)] = instruction;
        
        return (instructions_table, vma_instructions_table);
        
    #Méthode pour récupérer l'enfant d'un node XML
    def get_xml_child_value(self, node, child_name):
        return node.getElementsByTagName(child_name)[0].childNodes[0].data;
    
    def xml_node_has_child(self, node, child_name):
        return len(node.getElementsByTagName(child_name)) > 0;
