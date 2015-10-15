# -*- coding: utf-8 -*-

#Imports
import shutil;
import subprocess;
import xml.dom.minidom;
from xml.dom.minidom import parseString;
import networkx as nx;

#Main
def main():
    #Vérification de la présence d'opdis dans le PATH
    if (shutil.which("opdis") is None):
        print("Impossible de trouver opdis, est-il installé ?");
        return;
        
    #Chargement du XML    
    xml = subprocess.Popen(["opdis", "-f", "xml", "-E", "/home/ubuntu/workspace/testbinaries/bin/acc"], stdout=subprocess.PIPE).stdout.read();
    
    ###Essai de minidom
    document = parseString(xml).documentElement;
    
    instructions = [];
    
    for instruction in document.getElementsByTagName("instruction"):
        instructions.append(getInstructionChild(instruction, "offset") + " - " +  getInstructionChild(instruction, "ascii"));
        
    ###Essai de nx
    graph = nx.Graph();
    #graph.add_nodes_from(instructions);
    
    for i in range(len(instructions)):
        if (i != 0):
            graph.add_edge(instructions[i-1], instructions[i]);
    
    nx.write_dot(graph, "graph.dot");
    
    neato_output = subprocess.Popen(["neato", "-Tpng", "graph.dot"], stdout=subprocess.PIPE).stdout.read();
    png = open("graph.png", 'wb');
    png.write(neato_output);
    png.close();
        
    return;



def getInstructionChild(instruction, tag):
    return instruction.getElementsByTagName(tag)[0].childNodes[0].data;

if __name__ == "__main__":
    main();