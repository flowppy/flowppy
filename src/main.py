# -*- coding: utf-8 -*-

#Imports
import sys;
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

        
    return;

if __name__ == "__main__":
    sys.argv[0] = "opdis-control-flow-graph";
    run(main);
