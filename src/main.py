# -*- coding: utf-8 -*-

#Imports
import shutil;
import subprocess;
from xml.dom.minidom import parseString;
import xml.dom.minidom;

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
    
    for instruction in document.getElementsByTagName("instruction"):
        print(instruction.getElementsByTagName('mnemonic')[0].childNodes[0].data);
        
    return;



if __name__ == "__main__":
    main();