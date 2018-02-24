import json
import os
from urllib import request
from traversal.utils import *


# url = "http://cbdb.fas.harvard.edu/cbdbapi/person.php?id=1763&o=json"
# path = os.path.abspath('..')
# datapath = path+"/data/raw/1763.json"
# f = request.urlretrieve(url,datapath)

class Crawler:
    def __init__(self, year = 1132, min_rel = 3, min_social_rel = 1, female = True):
        self.year = year
        self.min_rel = min_rel
        self.min_social_rel = min_social_rel
        self.female = female

    def BFS(self, start_id = 1762):
        return



