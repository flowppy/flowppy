# -*- coding: utf-8 -*-

#Imports
import shutil;
import subprocess;
from lxml import etree;

#Main
def main():
    #Vérification de la présence d'opdis dans le PATH
    if (shutil.which("opdis") is None):
        print("Impossible de trouver opdis, est-il installé ?");
        return;
        
    #xml = subprocess.Popen(["opdis", "-f", "xml", "-E", "/home/ubuntu/workspace/testbinaries/bin/acc"], stdout=subprocess.PIPE).stdout.read();

    tree = etree.parse("/home/ubuntu/workspace/dis.xml");
    
    for node in tree.xpath("/disassembly/instruction/ascii"):
        print(node.text);
        
        
    return;



if __name__ == "__main__":
    main();