# -*- coding: utf-8 -*-

#Imports
import sys;
import shutil;
import subprocess;
import xml.dom.minidom;
from xml.dom.minidom import parseString;
import networkx as nx;
from clize import Parameter, run;
from sigtools.modifiers import annotate, autokwoargs;

#Liste des mnemonic des jump
JUMPS = ["je", "jbe"];

#Main
@annotate(input_file = "i", output_file = "o", render_engine = "r", graph_type = "t")
@autokwoargs
def main(input_file = "", output_file = "", render_engine = "dot", graph_type = "regular", *render_options):
    """
    Creates an control flow graph from a binary file using opdis and graphviz
    
    input_file: The binary file to create the graph from. Will use stdin if missing
    
    output_file: The file to save the graph to (can be .png, .gif, .svg, .svgz, .dot). Will use stdout with png format if missing
    
    render_engine: The graphviz engine to use when rendering the graph. Can be "dot", "neato", "circo", "fdp", "sfdp" or "twopi"
    
    graph_type: The type of the final graph. Can be "regular" (one instruction per node), "condensed" (multiple instructions per node, jumps and calls as edges), "translated" (multiple instructions per node, with flow control structures detection)
    
    render_options: The options to use when rendering the graph. See graphviz's "dot" manual for more details.
    """
    
    #Vérification de la présence d'opdis dans le PATH
    if (shutil.which("opdis") is None):
        print("Impossible de trouver opdis, est-il installé ?");
        return;
        
    #Chargement du XML    
    xml = subprocess.Popen(["opdis", "-f", "xml", "-E", "./testbinaries/bin/acc"], stdout=subprocess.PIPE).stdout.read();
    
    ###Création des structures de données
    document = parseString(xml).documentElement;
    
    instructions = [];
    instructionsVmaTable = {};
    
    for instruction in document.getElementsByTagName("instruction"):
        instructions.append(instruction);
        instructionsVmaTable[int(getInstructionChild(instruction, "vma"), 0)] = instruction;
        
    ###Création du graph
    graph = nx.DiGraph();
    
    for i in range(len(instructions)):
        if (i !=0):
            graph.add_edge(createInstructionString(instructions[i-1]), createInstructionString(instructions[i]));
            
        if getInstructionChild(instructions[i], "mnemonic") in JUMPS:
            targetVma = getJumpTarget(instructions[i]);
            graph.add_edge(createInstructionString(instructions[i]), createInstructionString(instructionsVmaTable[targetVma]));
        
            
    ###Export du graph
    nx.write_dot(graph, "graph.dot");
    
    neato_output = subprocess.Popen(["dot", "-Gstart=42", "-Goverlap=false", "-Gsplines=true", "-Nshape=box", "-Tpng", "graph.dot"], stdout=subprocess.PIPE).stdout.read();
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
    sys.argv[0] = "opdis-control-flow-graph";
    run(main);
