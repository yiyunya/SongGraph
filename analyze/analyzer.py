import os
import json
import networkx as nx
import networkx.algorithms as alg

def open_json_file(id):
    path = os.path.abspath('..')
    for i in range(4):
        if os.path.exists(path + "/data/valid_" + str(i) + "/" + id + ".json"):
            f = open(path + "/data/valid_" + str(i) + "/" + id + ".json", 'r')
            return f

def load_relation_rank():
    index = {}
    path = os.path.abspath('..')
    dir = path+"/data/relation_rank.txt"
    f = open(dir, 'r')
    lines = f.readlines()
    for line in lines:
        rel, rel_rank = line.split(' ')
        index[rel] = int(rel_rank)
    return index



def build_unweighted_rank_graph():
    index = load_relation_rank()
    graph = nx.DiGraph()
    path = os.path.abspath('..')
    f = open(path + "/data/node_checklist.json", 'r')
    node_list = json.load(f)
    for (k, name) in node_list.items():
        f = open_json_file(k)
        data = json.load(f)
        for kin in data["ValidKinship"]:
            out_node = int(k)
            in_node = int(kin["KinPersonId"])
            route_id = int(kin["KinCode"])
            graph.add_edge(out_node, in_node)

        for social in data["ValidSocialAssociation"]:
            out_node = int(k)
            in_node = int(social["AssocPersonId"])
            route_id = int(social["AssocCode"]) + 1000
            graph.add_edge(out_node, in_node)
    return graph

path = os.path.abspath('..')
f = open(path+"/data/klcommunity4_0.txt")
lines = f.readlines()
cluster_0 = []
cluster_1 = []
for i,line in enumerate(lines):
    id, name, rank = line.split()
    cluster_0.append({'id':id,'name':name,'rank':rank})

graph = build_unweighted_rank_graph()
nodes_0 = []
for i in cluster_0:
    nodes_0.append(int(i['id']))
print(len(nodes_0))
graph = graph.to_undirected()
p_0 = alg.average_clustering(graph, nodes_0)
print(p_0)

sum_0 = 0

for i in cluster_0:
    sum_0 += float(i['rank'])

print(sum_0)

f = open(path+"/data/klcommunity4_1.txt")
lines = f.readlines()
for i,line in enumerate(lines):
    id, name, rank = line.split()
    cluster_1.append({'id':id,'name':name,'rank':rank})

graph = build_unweighted_rank_graph()
nodes_1 = []
for i in cluster_1:
    nodes_1.append(int(i['id']))
print(len(nodes_1))
graph = graph.to_undirected()
p_1 = alg.average_clustering(graph, nodes_1)
print(p_1)

sum_1 = 0

for i in cluster_1:
    sum_1 += float(i['rank'])
print(sum_1)