# -*- coding: utf-8 -*-

#Imports
import sys;
from clize import Parameter, run;
import shutil;
from sigtools.modifiers import annotate, autokwoargs;
import tempfile;
import os.path;
import OutputManager;

#Liste des valeurs supportées par les différentes options
render_engines = ["dot", "neato", "circo", "fdp", "sfdp", "twopi"];
graph_types = ["regular", "condensed"];

#Main
@annotate(input_file = "i", output_file = "o", render_engine = "r", graph_type = "t", quiet_mode = "q")
@autokwoargs
def main(input_file = "", output_file = "", render_engine = "dot", graph_type = "regular", quiet_mode = False, *render_options):
    """
    Creates an control flow graph from a binary file using opdis and graphviz.
    
    input_file: The binary file to create the graph from. Will use stdin if missing.
    
    output_file: The file to save the graph to (can be .png, .gif, .svg, .svgz, .dot). Will use stdout with png format if missing.
    
    render_engine: The graphviz engine to use when rendering the graph. Can be "dot", "neato", "circo", "fdp", "sfdp" or "twopi".
    
    graph_type: The type of the final graph. Can be "regular" (one instruction per node) or "condensed" (multiple instructions per node, jumps and calls as edges).
    
    render_options: The options to use when rendering the graph. See graphviz's "dot" manual for more details.
    
    quiet_mode: If enabled, the program will not output anything except for the resulting graph, even when failing.
    """

    #Vérification de la présence d'opdis dans le PATH
    if (shutil.which("opdis") is None):
        print("Unable to find opdis, is it installed ?");
        return;
        
    #Création de l'OutputManager qui gère la sortie standard (erreurs, données)
    outputManager = OutputManager.OutputManager(quiet_mode);
        
    #Vérification de la validité des options
    #render_engine
    if not render_engine in render_engines:
        outputManager.print_message("Unknown render engine : " + render_engine);
        return;
    #graph_type
    if not graph_type in graph_types:
        outputManager.print_message("Unknown graph type : " + graph_type);
        return;
    #input_file - si l'option est présente le fichier doit exister
    if input_file and not os.path.isfile(input_file):
        outputManager.print_message("File not found : " + input_file);
        return;
        
    #Lecture des données en entrée
    if not input_file:
        #Fichier en entrée non présent, lecture depuis l'entrée standard
        binary = sys.stdin.read();
        
        #On écrit ce qu'on a en entrée standard dans un fichier temporaire pour opdis
        binary_file = tempfile.NamedTemporaryFile();
        binary_file.write(bytes(binary, 'UTF-8'));
        binary_file.close();
        input_file = binary_file.name;
        
    #Exécution d'opdis et récupération du XML
    xml = subprocess.Popen(["opdis", "-f", "xml", "-E", input_file], stdout=subprocess.PIPE).stdout.read();

if __name__ == "__main__":
    sys.argv[0] = "opdis-control-flow-graph";
    run(main);
