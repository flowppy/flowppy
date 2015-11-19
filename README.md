#opdis-flow-control-graph

##Présentation du projet
Ce programme en Python (3.4) consiste en la génération d’un graphe de flot de contrôle à partir du fichier binaire d’un programme. Autrement dit, à partir d’un fichier obtenu après compilation, notre programme va permettre de récupérer les instructions assembleur correspondant à son déroulement et de les visualiser sous forme d’un graphe.

TODO: Mettre une image d'exemple (condensed)

Le type de graphe ainsi que le moteur utilisé pour désassembler sont abstraits, ce qui permet d’avoir plusieurs rendus différents et une prise en charge de plusieurs langages de programmation.

Le programme se base sur plusieurs modules externes en Python (principalement `networkx`) ainsi que sur des utilitaires tels qu’`opdis` ou `graphviz` (liste détaillée plus bas).

##Fonctionnalités
    Usage: opdis-control-flow-graph [OPTIONS] [render-options...]
    
    Creates an control flow graph from a binary file using opdis and graphviz.
    
    Arguments:
      render-options...         The options to use when rendering the graph. See graphviz's "dot"
                                manual for more details.
    
    Options:
      -i, --input-file=STR      The binary file to create the graph from. Will use stdin if missing.
                                (default: )
      -o, --output-file=STR     The file to save the graph to. Will use stdout if missing. (default: )
      -r, --render-engine=STR   The graphviz engine to use when rendering the graph. Can be "dot",
                                "neato", "circo", "fdp", "sfdp" or "twopi". (default: dot)
      -t, --graph-type=STR      The type of the final graph. Can be "regular" (one instruction per
                                node) or "condensed" (multiple instructions per node, jumps and calls
                                as edges). (default: regular)
      -q, --quiet-mode          If enabled, the program will not output anything except for the
                                resulting graph, even when failing.
      -f, --output-format=STR   The format of the output file. Can be png, gif, svg, svgz or dot.
                                (default: png)
      -d, --disassembly-driver=STR
                                The disassembly driver to use. The only driver currently supported is
                                opdis. (default: opdis)
    
    Other actions:
      -h, --help                Show the help 

Le programme prend un fichier binaire en entrée (`--input-file`) et génère en sortie un graphe sous la forme d'une image ou d'un fichier `dot` (`--output-file`). Si rien n'est mis, le programme utilisera l'entrée et la sortie standard. Le format de sortie peut être précisé avec l'option `--output-format`. Si vous ne souhaitez pas afficher les potentielles erreurs, utilisez l'option `--quiet-mode`.

Les options `--graph-type` et `--render-engine` permettent de personnaliser le rendu final, avec respectivement le type de graphe à produire (une ou plusieurs instructions par noeud) et le moteur de rendu à utiliser (voir la documentation de `graphviz` pour plus de détails).

Dans l'optique de supporter plusieurs langages de programmation, le désassembleur a été abstrait, même si il n'y a qu'`opdis` de supporté pour l'instant. Il peut néanmoins être changé à l'aide de `--disassembly-driver`.


##Exemples d'utilisation
Des fichiers binaires d'exemples sont fournis dans le dossier `testbinaries` et peuvent être compilés via le script fourni à cet effet (nécessite `gcc`).

TODO: Mettre les exemples

##Dépendances
Le programme est développé en Python 3.4, il donc nécessite de l'avoir d'installé. Il faut également installer ces modules (via la commande `pip3`) :
* `clize` - utilisé pour parser les options en ligne de commande et pour générer le message d'aide
* `networkx` - utilisé pour générer le graphe en interne
* `pydot2` - utilisé pour effectuer l'exporation du graphe vers le format de `graphviz`

Il y a également des dépendances externes obligatoires :
* `graphviz` - utilisé pour le rendu des graphes en images

Enfin, des dépendances externes optionnelles selon le driver que vous voulez utiliser :
* `opdis` - utilisé pour désassembler des fichiers binaires - peut être installé sur le système ou localement dans le dossier `opdis` adjacent au projet


##Installation
Pour installer le programme, clonez le dépôt dans un dossier local. Vérifiez que vous avez Python 3.4 d'installé puis récupérez les modules via la commande :

`sudo pip3 install clize networkx pydot2`

Installez ensuite les dépendances externes :

`sudo apt-get install graphviz`

Et enfin `opdis` si vous souhaitez l'utiliser ; pour ce faire, allez sur [leur dépôt](https://github.com/mkfs/opdis) et suivez leurs instructions :

    ./bootstrap
    ./configure
    make

Pour l'installer localement :
`make dist`

Pour l'installer sur le système :
`sudo make install`
