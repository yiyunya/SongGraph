import networkx as nx
import os
import json

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

def build_rank_graph():
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
            # graph.add_edge(out_node, in_node, route_id)
            if graph.has_edge(out_node, in_node):
                graph[out_node][in_node]['weight'] += 1
            else:
                graph.add_edge(out_node, in_node, weight=1)

        for social in data["ValidSocialAssociation"]:
            out_node = int(k)
            in_node = int(social["AssocPersonId"])
            route_id = int(social["AssocCode"]) + 1000
            if index[social["AssocCode"]] == 1:
                if graph.has_edge(out_node, in_node):
                    graph[out_node][in_node]['weight'] += 1
                else:
                    graph.add_edge(out_node, in_node, weight=1)
    return graph

def build_negative_rank_graph():
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
            # graph.add_edge(out_node, in_node, route_id)
            if graph.has_edge(out_node, in_node):
                graph[out_node][in_node]['weight'] += 1
            else:
                graph.add_edge(out_node, in_node, weight=1)

        for social in data["ValidSocialAssociation"]:
            out_node = int(k)
            in_node = int(social["AssocPersonId"])
            route_id = int(social["AssocCode"]) + 1000
            if index[social["AssocCode"]] == 1:
                if graph.has_edge(out_node, in_node):
                    graph[out_node][in_node]['weight'] += 1
                else:
                    graph.add_edge(out_node, in_node, weight=1)
            elif index[social["AssocCode"]] == -1:
                if graph.has_edge(out_node, in_node):
                    graph[out_node][in_node]['weight'] += -1
                else:
                    graph.add_edge(out_node, in_node, weight=-1)
    return graph


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


def open_json_file(id):
    path = os.path.abspath('..')
    for i in range(4):
        if os.path.exists(path + "/data/valid_" + str(i) + "/" + id + ".json"):
            f = open(path + "/data/valid_" + str(i) + "/" + id + ".json", 'r')
            return f


def change_into_name():
    path = os.path.abspath('..')
    f = open(path+"/data/node_checklist.json",'r')
    node_list = json.load(f)
    pagerank = open(path+"/data/pagerank.json", 'r')
    pagerank = json.load(pagerank)
    name_rank = {}
    for (k,v) in node_list.items():
        name_rank[k] = {'name':v, 'rank':pagerank[k]}
    return name_rank