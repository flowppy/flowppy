# -*- coding: utf-8 -*-

#Imports
import shutil;

#Main
def main():
    #Vérification de la présence d'opdis dans le PATH
    if (shutil.which("opdis") is None):
        print("Impossible de trouver opdis, est-il installé ?");
        return;
        
    return;



if __name__ == "__main__":
    main();