import json
import os


def relation_index(step):
    index = {}
    path = os.path.abspath('..')
    for i in range(step + 1):
        dir = path + "/data/valid_" + str(i) + "/"
        files = os.listdir(dir)
        for name in files:
            if (name.endswith(".json")):
                datapath = dir + name
                f = open(datapath,'r')
                data = json.load(f)
                for rel in data['SocialAssociation']:
                    if rel["AssocCode"] not in index.keys():
                        index[rel["AssocCode"]] = rel["AssocName"]
    return index


def kinship_index(step):
    index = {}
    path = os.path.abspath('..')
    for i in range(step + 1):
        dir = path + "/data/valid_" + str(i) + "/"
        files = os.listdir(dir)
        for name in files:
            if (name.endswith(".json")):
                datapath = dir + name
                f = open(datapath,'r')
                data = json.load(f)
                for rel in data['Kinship']:
                    if rel["AssocCode"] not in index.keys():
                        index[rel["AssocCode"]] = rel["AssocName"]
    return index


def node_index(step):
    index = {}
    path = os.path.abspath('..')
    for i in range(step + 1):
        dir = path + "/data/valid_" + str(i) + "/"
        files = os.listdir(dir)
        for name in files:
            if (name.endswith(".json")):
                datapath = dir + name
                f = open(datapath,'r')
                data = json.load(f)
                index[data["BasicInfo"]["PersonId"]] = data["BasicInfo"]["ChName"]
    return index


def male_node_index(step):
    index = {}
    path = os.path.abspath('..')
    for i in range(step + 1):
        dir = path + "/data/valid_" + str(i) + "/"
        files = os.listdir(dir)
        for name in files:
            if (name.endswith(".json")):
                datapath = dir + name
                f = open(datapath,'r')
                data = json.load(f)
                if data["BasicInfo"]["Gender"] == '0':
                    index[data["BasicInfo"]["PersonId"]] = data["BasicInfo"]["ChName"]
    return index

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


def sorted():
    path = os.path.abspath('..')
    f = open(path+"/data/node_checklist.json",'r')
    node_list = json.load(f)
    pagerank = open(path+"/data/pagerank.json", 'r')
    pagerank = json.load(pagerank)
    name_rank = {}
    for (k,v) in node_list.items():
        name_rank[k] = {'name':v, 'rank':pagerank[k]}
    items = name_rank.items()
    sorter = [[v[1]['rank'],v[0],v[1]['name']] for v in items]
    sorter.sort()
    return sorter


def weight_sorted():
    path = os.path.abspath('..')
    f = open(path+"/data/node_checklist.json",'r')
    node_list = json.load(f)
    pagerank = open(path+"/data/weighted_pagerank.json", 'r')
    pagerank = json.load(pagerank)
    name_rank = {}
    for (k,v) in node_list.items():
        name_rank[k] = {'name':v, 'rank':pagerank[k]}
    items = name_rank.items()
    sorter = [[v[1]['rank'],v[0],v[1]['name']] for v in items]
    sorter.sort()
    return sorter


def positive_sorted():
    path = os.path.abspath('..')
    f = open(path+"/data/node_checklist.json",'r')
    node_list = json.load(f)
    pagerank = open(path+"/data/positive_weighted_pagerank.json", 'r')
    pagerank = json.load(pagerank)
    name_rank = {}
    for (k,v) in node_list.items():
        if k in pagerank.keys():
            name_rank[k] = {'name':v, 'rank':pagerank[k]}
    items = name_rank.items()
    sorter = [[v[1]['rank'],v[0],v[1]['name']] for v in items]
    sorter.sort()
    return sorter


def search_association(id):
    index = {}
    path = os.path.abspath('..')
    for i in range(4):
        dir = path + "/data/valid_" + str(i) + "/"
        files = os.listdir(dir)
        for name in files:
            if (name.endswith(".json")):
                datapath = dir + name
                f = open(datapath,'r')
                data = json.load(f)
                for rel in data['SocialAssociation']:
                    if rel["AssocPersonId"] == str(id):
                        index[data["BasicInfo"]["PersonId"]] = [rel["AssocPersonName"],rel["AssocName"]]

    for i in range(4):
        if os.path.exists(path + "/data/valid_" + str(i) + "/" + str(id) + ".json"):
            dir = path + "/data/valid_" + str(i) + "/" + str(id) + ".json"
            f = open(dir, 'r')
            data = json.load(f)
            for rel in data['SocialAssociation']:
                index[rel["AssocPersonId"]] = [rel["AssocPersonName"],rel["AssocName"]]
    return index




index = positive_sorted()
print(len(index))
dir = os.path.abspath('..') + "/data/positive_weighted_ranking.txt"
with open(dir, 'w') as f:
    for i in index:
        print(i[1]," ",i[2]," ",i[0],file = f)

# index = search_association(9008)
# dir = os.path.abspath('..') + "/data/9008.txt"
# with open(dir, 'w') as f:
#     for k,v in index.items():
#         print(k," ",v[0]," ",v[1], file = f)



