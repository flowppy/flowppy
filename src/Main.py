# -*- coding: utf-8 -*-

#Import des modules
import sys;
from clize import Parameter, run;
import shutil;
from sigtools.modifiers import annotate, autokwoargs;
import tempfile;
import os.path;
import OutputManager;
import subprocess;
import traceback;
import networkx as nx;

#Import des drivers
import GraphDriver;
import RegularDriver;
import CondensedDriver;

import DisassemblyDriver;
import OpdisDriver;


#Liste des valeurs supportées par les différentes options
render_engines = ["dot", "neato", "circo", "fdp", "sfdp", "twopi"];
output_formats = ["png", "gif", "svg", "svgz", "dot"];

#Main
@annotate(input_file = "i", output_file = "o", render_engine = "r", graph_type = "t", quiet_mode = "q", output_format = "f", disassembly_driver = "d")
@autokwoargs
def main(input_file = "", output_file = "", output_format = "", render_engine = "dot", graph_type = "regular", quiet_mode = False, disassembly_driver = "opdis", *render_options):
    #Détail des options pour clize
    """
    Creates an control flow graph from a binary file using graphviz.
    
    input_file: The binary file to create the graph from. Will use stdin if missing.
    
    output_file: The file to save the graph to (will use stdout if missing). The extension is used to guess the format, please use the output-format option to override it.
    
    render_engine: The graphviz engine to use when rendering the graph. Can be "dot", "neato", "circo", "fdp", "sfdp" or "twopi".
    
    graph_type: The type of the final graph. Can be "regular" (one instruction per node) or "condensed" (multiple instructions per node, jumps and calls as edges).
    
    render_options: The options to use when rendering the graph. See graphviz's "dot" manual for more details.
    
    quiet_mode: If enabled, the program will not output anything except for the resulting graph, even when failing.
    
    output_format: The format of the output file. Can be png, gif, svg, svgz or dot. Will take the output file extension if omitted.
    
    disassembly_driver: The disassembly driver to use. The only driver currently supported is opdis.
    """
    #Création de l'OutputManager qui gère la sortie standard (erreurs, données)
    outputManager = OutputManager.OutputManager(quiet_mode);
    
    #Vérification de la présence de graphviz dans le PATH
    if (shutil.which("dot") is None):
        outputManager.print_error("graphviz is required and could not be found, aborting.");
        return;
    
    #Chargement des drivers
    #DisassemblyDriver
    disassembly_drivers = {};
    for sub in DisassemblyDriver.DisassemblyDriver.__subclasses__():
        disassembly_drivers[sub.get_name()] = sub;
    #GraphDriver
    graph_drivers = {};
    for sub in GraphDriver.GraphDriver.__subclasses__():
        graph_drivers[sub.get_name()] = sub;

        
    #Vérification de la validité des options
    #disassembly_driver
    if not disassembly_driver in disassembly_drivers:
        outputManager.print_error("Unknown disassembly driver : " + disassembly_driver);
        return;
    #render_engine
    if not render_engine in render_engines:
        outputManager.print_error("Unknown render engine : " + render_engine);
        return;
    #graph_type
    if not graph_type in graph_drivers:
        outputManager.print_error("Unknown graph type : " + graph_type);
        return;
    #input_file - si l'option est présente le fichier doit exister
    if input_file and not os.path.isfile(input_file):
        outputManager.print_error("File not found : " + input_file);
        return;
    #output_format
    if output_file and not output_format:
        output_file_splitted = output_file.split("."); #détection du format depuis l'extension
        output_format = output_file_splitted[len(output_file_splitted)-1];
    elif not output_file and not output_format:
        outputManager.print_error("Missing output format, please use the --output-format (-f) option"); #aucun format donné pour stdout, aucune extension pour deviner
        return;
    if not output_format in output_formats:
        outputManager.print_error("Unknown output format : " + output_format);
        return;
        
    #Lecture des données en entrée
    if not input_file:
        #Fichier en entrée non présent, lecture depuis l'entrée standard
        binary = sys.stdin.read();
        
        #On écrit ce qu'on a en entrée standard dans un fichier temporaire pour opdis
        binary_file = tempfile.NamedTemporaryFile(delete = False);
        binary_file.write(bytes(binary, 'UTF-8'));
        binary_file.close();
        input_file = binary_file.name;
        
    #Traitement
    try:
        #Exécution du désassemblage
        disassembly_driver = disassembly_drivers[disassembly_driver]();
        instructions_table, vma_instructions_table = disassembly_driver.disassemble(input_file);
        
        #Vérification des dépendances
        for dep in disassembly_driver.get_dependencies():  
            if (shutil.which(dep) is None):
                outputManager.print_error(dep + "is required and could not be found, aborting.");
                return;
                
        #Création du graphe
        graph_driver = graph_drivers[graph_type](outputManager, disassembly_driver);
        graph = graph_driver.create_graph(instructions_table, vma_instructions_table);
        
        #Création du .dot dans un fichier temporaire
        dot_file = tempfile.NamedTemporaryFile(delete = False);
        nx.write_dot(graph, dot_file.name);
        
        #On regarde l'output demandé
        if output_file:
            #On veut un fichier
            makedirs(output_file);
            delete_file_if_exists(output_file);
            if output_format == "dot":
                #On copie le .dot temporaire là où il veut
                shutil.copyfile(dot_file.name, output_file);
            else:
                #On convertit l'image là où il veut
                output = render_and_read_graph(render_engine, render_options, output_format, dot_file.name);
                image = open(output_file, 'wb');
                image.write(output);
                image.close();
            outputManager.print_message("Graph saved to " + output_file);
        else:
            #On veut dans stdout
            #On convertit le .dot temporaire dans stdout
            sys.stdout.buffer.write(render_and_read_graph(render_engine, render_options, output_format, dot_file.name));
            sys.stdout.flush();
              
    except Exception as e:
        outputManager.print_error("Error while creating graph : " + str(e) + "\n" + str(traceback.format_exc()));

#Méthode qui exécute le moteur de rendu et affiche le résultat dans stdout
def create_render_graph_subprocess(render_engine, render_options, output_format, dot_file):
    render_command = [];
    render_command.append(render_engine);
    render_command += render_options;
    render_command += ["-Gstart=42", "-Goverlap=false", "-Gsplines=true", "-Nshape=box", "-T" + output_format, dot_file];
    return subprocess.Popen(render_command, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE);
    
#Lit le rendu de stdout dans un string
def render_and_read_graph(render_engine, render_options, output_format, dot_file):
    return create_render_graph_subprocess(render_engine, render_options, output_format, dot_file).stdout.read();

#Méthode pour créer tous les dossiers parents d'un fichier
def makedirs(filename):
    if not os.path.exists(os.path.dirname(os.path.abspath(filename))):
        os.makedirs(os.path.dirname(os.path.abspath(filename)));
        
#Méthode pour supprimer un fichier qui existe peut-être
def delete_file_if_exists(filename):
    try:
        os.remove(filename)
    except OSError:
        pass;
        
if __name__ == "__main__":
    sys.argv[0] = "flowppy";
    run(main);
