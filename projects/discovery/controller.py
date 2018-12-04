import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
import sswitch_CLI
import discovery_MININET as mininet

GRAPH = {"directed": True, "graph": {}, "nodes": [], "links": [], "multigraph": False}

def get_switch(ip):
    for node in GRAPH["nodes"]:
        if (ip == node["ip"]):
            return node
    return None

def get_links():
    print("Get Links")
    links = []
    for node1 in GRAPH['nodes']:
        for node2 in GRAPH['nodes']:
            aux = node1["cli"].get_register_read('discovery_register', node2['id'])
            if aux == 1:
                links.append({ "weight": 1, "source": node1['id'], "target": node2['id'], "porigem": 0, "pdestino": 0})
    GRAPH["links"] = links

def reset_register(ip):
    print('Resetando registradores')
    switch = get_switch(ip)
    if (switch == None):
        print('IP INVALIDO')
        return
    for node in GRAPH['nodes']:
        try:
            node["cli"].do_register_write('discovery_register ' + str(switch['id']) + ' 0')
        except Exception as e:
            pass

def add_rules(ip):
    print("Add Rules")
    switch = get_switch(ip)
    if (switch == None):
        print('IP INVALIDO')
        return
    for node in GRAPH['nodes']:
        try:
            switch["cli"].do_table_add('discovery discovery ' + node['ip'] + ' ' + node['ip'] + ' => ' + str(node['id']))
            if node['ip'] != switch['ip']:
                node["cli"].do_table_add('discovery discovery ' + ip + ' ' + ip + ' => ' + str(switch['id']))
        except Exception as e:
            print(e)
            pass

def new_switch(ip, porta):
    if(get_switch(ip) != None):
        return
    thrift_Cli = sswitch_CLI.get_Cli('localhost', porta, 'build/discovery.json')
    try:
        file = open('util/s' + ip.split('.')[2] + '.txt')
        for line in file:
            getattr(thrift_Cli, 'do_' + line.split()[0])(line[len(line.split()[0]) + 1:])
    except Exception as e:
        pass
    GRAPH["nodes"].append({"id":int(ip.split('.')[2]),"ip":ip,"port":porta,"cli":thrift_Cli})
    add_rules(ip)
    
def show(F):
    F = json_graph.node_link_graph(F)
    pos = nx.circular_layout(F)
    nx.draw(F, pos, node_size=3000)
    node_labels = nx.get_node_attributes(F, 'ip')
    n = {}
    for i in node_labels:
        n[i] = str(i) + "\n" + str(node_labels[i])
    nx.draw_networkx_labels(F, pos, labels=n, font_size=10, font_weight='bold')
    edge_labels = nx.get_edge_attributes(F, 'current_capacity')
    edge_labels2 = nx.get_edge_attributes(F, 'capacity')
    d = {}
    for i in edge_labels:
        d[i] = str(edge_labels[i]) + "/" + str(edge_labels2[i])
    nx.draw_networkx_edge_labels(F, pos, edge_labels=d, font_color='blue', font_size=12, font_weight='bold')
    plt.show()

# net = mininet.start()
# try:
while True:
    try:
        option = input('1 - New Switch\n2 - Discovery Links\n3 - Show\n4 - Reset registers\n0 - Exit\n--> ')
        if(option == 1):
            ip = raw_input("IP: ")
            porta = raw_input("Porta Thrift: ")
            new_switch(ip, porta)
        elif (option == 2):
            # ip = raw_input("IP: ")
            # reset_register(ip.replace('\n',''))
            # print('Executando ping 10.0.0.10 to ' + ip.replace('\n',''))
            # try:
            #     net.ping(hosts=[net.host[0],net.host[int(ip.split('.')[2])]])
            # except Exception as e:
            #     print(e)
            F = get_links()
        elif (option == 3):
            show(GRAPH)
        elif (option == 4):
            ip = raw_input("IP: ")
            reset_register(ip.replace('\n',''))
        elif (option == 0):
            # net.stop()
            break
        else:
            print("Opcao Invalida")
    except Exception as e:
        print("Deu Ruim: " + e)
# except Exception:
#     net.stop()