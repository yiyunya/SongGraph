import numpy as np
from rank.utils import *
import networkx as nx


class Ranker:
    def __init__(self, alpha = 0.85):
        self.alpha = alpha

        return

    def rank(self):
        self.graph = build_graph()
        pr = nx.pagerank(self.graph)
        return pr

    def weight_rank(self):
        self.graph = build_weight_graph()
        pr = nx.pagerank(self.graph)
        return pr

    def positive_rank(self):
        self.graph = build_rank_graph()
        pr = nx.pagerank(self.graph)
        return pr


ranker = Ranker()
pr = ranker.positive_rank()
dir = os.path.abspath('..') + "/data/positive_weighted_pagerank.json"
with open(dir, 'w') as f:
    json.dump(pr, f, indent=4, ensure_ascii=False)






