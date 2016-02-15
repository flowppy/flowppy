![](https://github.com/natinusala/flowppy/blob/master/images/banniere.png)

Ce programme en Python (3.4) consiste en la génération d’un graphe de flot de contrôle à partir du fichier binaire d’un programme. Autrement dit, à partir d’un fichier obtenu après compilation, notre programme va permettre de récupérer les instructions assembleur correspondant à son déroulement et de les visualiser sous forme d’un graphe.

Le type de graphe ainsi que le moteur utilisé pour désassembler sont abstraits, ce qui permet d’avoir plusieurs rendus différents et une prise en charge de plusieurs langages de programmation.

Le programme se base sur plusieurs modules externes en Python (principalement `networkx`) ainsi que sur des utilitaires tels qu’`opdis` ou `graphviz` (liste détaillée plus bas).

###Améliorations possibles
* interface graphique dynamique
* version intégrée à un site web
* exécution pas à pas liée au graphe
* gestion des fonctions avec une pile
* extraction des données du SVG pour obtenir le placement des noeuds
* écrire des drivers pour d'autres langages : Java, C#, Smali...

##Fonctionnalités
    Usage: flowppy [OPTIONS] [render-options...]
    
    Creates an control flow graph from a binary file using graphviz.
    
    Arguments:
      render-options...              The options to use when rendering the graph. See graphviz's "dot" manual for more details.
    
    Options:
      -i, --input-file=STR           The binary file to create the graph from. Will use stdin if missing. (default: )
      -o, --output-file=STR          The file to save the graph to (will use stdout if missing). The extension is used to guess the format, please use the output-format option to override it. (default: )
      -r, --render-engine=STR        The graphviz engine to use when rendering the graph. Can be "dot", "neato", "circo", "fdp", "sfdp" or "twopi". (default: dot)
      -t, --graph-type=STR           The type of the final graph. Can be "regular" (one instruction per node) or "condensed" (multiple instructions per node, jumps and calls as edges). (default: regular)
      -q, --quiet-mode               If enabled, the program will not output anything except for the resulting graph, even when failing.
      -f, --output-format=STR        The format of the output file. Can be png, gif, svg, svgz or dot. Will take the output file extension if omitted. (default: )
      -d, --disassembly-driver=STR   The disassembly driver to use. The only driver currently supported is opdis. (default: opdis)
    
    Other actions:
      -h, --help                     Show the help

Le programme prend un fichier binaire en entrée (`--input-file`) et génère en sortie un graphe sous la forme d'une image ou d'un fichier `dot` (`--output-file`). Si rien n'est mis, le programme utilisera l'entrée et la sortie standard. Le format de sortie est déduit de l'extention du fichier de sortie, mais peut être écrasé avec l'option `--output-format` (qui est cependant nécessaire pour la sortie standard, il n'y a pas d'extension avec laquelle déduire). Si vous ne souhaitez pas afficher les potentielles erreurs, utilisez l'option `--quiet-mode`.

Les options `--graph-type` et `--render-engine` permettent de personnaliser le rendu final, avec respectivement le type de graphe à produire (une ou plusieurs instructions par noeud) et le moteur de rendu à utiliser (voir la documentation de `graphviz` pour plus de détails).

Dans l'optique de supporter plusieurs langages de programmation, le désassembleur a été abstrait, même si il n'y a qu'`opdis` de supporté pour l'instant. Il peut néanmoins être changé à l'aide de `--disassembly-driver`.

##Exemples d'utilisation
Des fichiers binaires d'exemples sont fournis dans le dossier `testbinaries` et peuvent être compilés via le script fourni à cet effet (nécessite `gcc`).

    #Générer un graphe simple du binaire acc au format PNG
    ./flowppy -i testbinaries/acc -o graph.png 
    
    #Générer un graphe condensé du binaire acc au format GIF et avec le moteur neato
    ./flowppy -i testbinaries/acc -o graph.gif -t condensed -r neato
    
    #Récupérer le graphe au format DOT dans la sortie standard (pas de -o)
    ./flowppy -i testbinaries/acc -f dot

##Dépendances
Le programme est développé en Python 3.4, il donc nécessite de l'avoir d'installé. Il faut également installer ces modules (via la commande `pip3`) :
* `clize` - utilisé pour parser les options en ligne de commande et pour générer le message d'aide
* `networkx` - utilisé pour générer le graphe en interne
* `pydotplus` - utilisé pour effectuer l'exporation du graphe vers le format de `graphviz`

Il y a également des dépendances externes obligatoires :
* `graphviz` - utilisé pour le rendu des graphes en images

Enfin, des dépendances externes optionnelles selon le driver que vous voulez utiliser :
* `opdis` - utilisé pour désassembler des fichiers binaires - peut être installé sur le système ou localement dans le dossier `opdis` adjacent au projet.


##Installation sous Debian et dérivés
Pour installer le programme, clonez le dépôt dans un dossier local. Vérifiez que vous avez Python 3.4 d'installé puis récupérez les modules via la commande :

`sudo pip3 install clize networkx pydotplus`

Installez ensuite les dépendances externes :

`sudo apt-get install graphviz`

Et enfin `opdis` si vous souhaitez l'utiliser ; pour ce faire, allez sur [leur dépôt](https://github.com/mkfs/opdis), clonez le et suivez leurs instructions :

    sudo apt-get install binutils binutils-dev libtool
    ./bootstrap
    ./configure
    make

Pour l'installer localement :
`make dist`

Pour l'installer sur le système :
`sudo make install`

##Pour les développeurs

Si vous souhaitez étendre le programme, libre à vous d'ajouter les drivers adéquats et de proposer une pull request. Vous pouvez actuellement ajouter deux types de drivers (consultez le wiki pour connaître la spécification des classes à étendre) :
* `GraphDriver`, le driver décrivant le type de graphe à créer, il prend en paramètres la table des instructions et retourne un graphe
* `DisassemblyDriver`, le driver permettant le désassemblage d'un fichier, il prend en entrée un fichier et retourne une table d'instructions ainsi qu'une expression régulière pour connaître si une instruction est un branchement

Pour ajouter un driver, vous n'avez qu'à créer une nouvelle classe étendant de la bonne superclasse, puis importez la dans le fichier `Main.py`. Le nouveau driver sera chargé automatiquement, il n'y a rien besoin de faire de plus.
