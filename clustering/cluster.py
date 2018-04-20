from clustering.utils import *
import networkx.algorithms.community as alg
import pprint
from networkx import *
import itertools

class Cluster:
    def __init__(self):
        return

    def kernighan_lin_bisection(self):
        graph = build_negative_rank_graph()
        graph = graph.to_undirected()
        result = alg.kernighan_lin_bisection(graph)
        return result

    def asyn_lpa_communities(self):
        graph = build_rank_graph()
        result = alg.asyn_lpa_communities(graph)
        return result

    def asyn_fluidc(self, k):
        graph = build_unweighted_rank_graph()
        graph = graph.to_undirected()
        result = alg.asyn_fluidc(graph, k, max_iter = 100)
        return result

    def girvan_newman(self, k):
        graph = build_rank_graph()
        comp = alg.girvan_newman(graph)
        limited = itertools.takewhile(lambda c: len(c) <= k, comp)
        f = open(os.path.abspath('..')+"/data/girvan_newman.txt",'w')
        for communities in limited:
            print("community count:",len(communities),":")
            print(tuple(sorted(c) for c in communities),file = f)
            print(" ")
            print(" ")

#
cluster = Cluster()
# cluster.girvan_newman(10)


k = 2
result = cluster.kernighan_lin_bisection()
community_list = {}
for i, d in enumerate(result):
    community_list[i] = d


path = os.path.abspath('..')
f = open(path + "/data/node_checklist.json", 'r')
node_list = json.load(f)
pagerank = open(path + "/data/pagerank.json", 'r')
pagerank = json.load(pagerank)
name_rank = {}
community = []
sorter = []
for i in range(k):
    community.append([])
for i in range(k):
    for id in community_list[i]:
        community[i].append({'id':id, 'name':node_list[str(id)], 'rank':pagerank[str(id)]})
for i in range(k):
    sorter.append([[v['rank'], v['name'], v['id']] for v in community[i]])
    sorter[i].sort(reverse=True)
for i in range(k):
    dir = os.path.abspath('..') + "/data/klcommunity3_" + str(i) + ".txt"
    with open(dir, 'w') as f:
        for i in sorter[i]:
            print(i[2], " ", i[1], " ", i[0], file=f)
    f.close()





