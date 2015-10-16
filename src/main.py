# -*- coding: utf-8 -*-

#Imports
import shutil;
import subprocess;
import xml.dom.minidom;
from xml.dom.minidom import parseString;
import networkx as nx;

#Liste des mnemonic des jump
JUMPS = ["je", "jbe"];

#Main
def main():
    #Vérification de la présence d'opdis dans le PATH
    if (shutil.which("opdis") is None):
        print("Impossible de trouver opdis, est-il installé ?");
        return;
        
    #Chargement du XML    
    xml = subprocess.Popen(["opdis", "-f", "xml", "-E", "./testbinaries/bin/acc"], stdout=subprocess.PIPE).stdout.read();
    
    ###Essai de minidom
    document = parseString(xml).documentElement;
    
    instructions = [];
    instructionsVmaTable = {};
    
    for instruction in document.getElementsByTagName("instruction"):
        instructions.append(instruction);
        instructionsVmaTable[int(getInstructionChild(instruction, "vma"), 0)] = instruction;
        
    ###Essai de nx
    graph = nx.Graph();
    
    for i in range(1, len(instructions)):
        graph.add_edge(createInstructionString(instructions[i-1]), createInstructionString(instructions[i]));
            
    for i in range(len(instructions)):
        if getInstructionChild(instructions[i], "mnemonic") in JUMPS:
            targetVma = getJumpTarget(instructions[i]);
            graph.add_edge(createInstructionString(instructions[i]), createInstructionString(instructionsVmaTable[targetVma]));
            
    nx.write_dot(graph, "graph.dot");
    
    neato_output = subprocess.Popen(["circo", "-Tpng", "graph.dot"], stdout=subprocess.PIPE).stdout.read();
    png = open("graph.png", 'wb');
    png.write(neato_output);
    png.close();
        
    return;
    
def createInstructionString(instruction):
    return getInstructionChild(instruction, "offset") + " - " +  getInstructionChild(instruction, "ascii");

def getInstructionChild(instruction, tag):
    return instruction.getElementsByTagName(tag)[0].childNodes[0].data;
    
def getJumpTarget(instruction):
    
    return int(instruction.getElementsByTagName("operands")[0].
    getElementsByTagName("ascii")[0].
    childNodes[0].data, 0);
    
    return 0;

if __name__ == "__main__":
    main();
