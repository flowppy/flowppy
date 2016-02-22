def to_json(graph, output_file, graph_type):
    nodes_id = {};
    json = "";
    nodes = graph.node;
    edges = graph.edges(data = True);
    json = json + "nodes : [ \n";
    cpt = 1;
    for node in nodes:
        if graph_type == "condensed":
            node_str = node.replace("\l", "\\n");
            node_str = node_str[:len(node)-1]+'"\n';
        else:
            node_str = node[:len(node)-2]+'\\n"';
        str_buff = "{id:"+str(cpt)+", label:"+node_str+"},  \n";
        nodes_id[node] = cpt;
        json = json + str_buff;
        cpt = cpt+1;
    json = json + "],\n";
    
    one_edge = scan_edges(graph, nodes_id);
    
    json = json + "edges : [\n";
    for edge in edges:
        str_buff = "{from: "+str(nodes_id[edge[0]])+", to: "+str(nodes_id[edge[1]]);
        if(edge[2]['label'] != '""'):
            str_buff = str_buff + ', label : '+edge[2]['label'];
        if (nodes_id[edge[0]] in one_edge or nodes_id[edge[1]] in one_edge):
            str_buff = str_buff + ",	smooth: { enabled: false }";
        str_buff = str_buff + "},\n";
        json = json + str_buff;
    json = json + "]";
    if output_file != "":
        json_file = open(output_file, "w");
        json_file.write(json);
        json_file.close();
    else:
        print(json);
        
#retourne un tableau associatif id    
def get_dictionnary_nodes(graph):
    nodes = graph.node;
    node_id = {};
    cpt = 1;
    for node in nodes:
        node_id[cpt] = node;
        cpt = cpt +1;
    return node_id;
    
    
#méthode qui permet de renvoyer les noeuds qui n'ont qu'un pont        
def scan_edges(graph, nodes_id):
    edges = graph.edges();
    node_nb_edge = {};
    node_one_edge = [];
    for edge in edges:
        id_node_a = nodes_id[edge[0]];
        id_node_b = nodes_id[edge[1]];
        if id_node_a not in node_nb_edge.keys():
            node_nb_edge[id_node_a] = 1;
        else:
            node_nb_edge[id_node_a] = node_nb_edge[id_node_a] + 1;
        if id_node_b not in node_nb_edge.keys():
            node_nb_edge[id_node_b] = 1;
        else:
            node_nb_edge[id_node_b] = node_nb_edge[id_node_b] + 1;
    for node in node_nb_edge.keys():
        if node_nb_edge[node] <= 1:
            node_one_edge.append(node);
    return node_one_edge;