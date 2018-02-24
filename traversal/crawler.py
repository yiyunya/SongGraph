import json
import os
from urllib import request
from traversal.utils import *
import time


# url = "http://cbdb.fas.harvard.edu/cbdbapi/person.php?id=1763&o=json"
# path = os.path.abspath('..')
# datapath = path+"/data/raw/1763.json"
# f = request.urlretrieve(url,datapath)

class Crawler:
    def __init__(self, year = 1120, min_rel = 2, min_social_rel = 1, female = True):
        self.year = year
        self.min_rel = min_rel
        self.min_social_rel = min_social_rel
        self.female = female

    def BFS(self, start_id = 1762):

        all = [start_id]
        valid = [start_id]

        a = [start_id]
        v = [start_id]

        counter = 0
        step_counter = 0
        time_start = time.time()

        while len(v) is not 0:
            tmp_a = []
            tmp_v = []
            for id in v:
                step_a ,step_v = step(id, self.year, self.min_rel, self.min_social_rel, self.female)
                tmp_a.append(step_a)
                tmp_v.append(step_v)
            a = tmp_a
            v = tmp_v
            all.extend(a)
            valid.extend(v)
            counter += len(v)
            step_counter += 1
            step_time = time.time() - time_start
            print("After"+str(step_counter)+"steps, "+"valid datasize:"+str(counter))
            print("Time used:"+str(step_time)+"s")

        return step_counter, counter

crawl = Crawler()
total_step, total = crawl.BFS()
print(total_step, total)

