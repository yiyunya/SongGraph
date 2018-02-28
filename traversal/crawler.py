# coding: utf-8
import json
import os
from urllib import request
from traversal.utils import *
import time


# url = "http://cbdb.fas.harvard.edu/cbdbapi/person.php?id=1763&o=json"
# path = os.path.abspath('..')
# datapath = path+"/data/raw_0/1763.json"
# f = request.urlretrieve(url,datapath)

class Crawler:
    def __init__(self, year = 1110, min_rel = 3, min_social_rel = 1, female = True):
        self.year = year
        self.min_rel = min_rel
        self.min_social_rel = min_social_rel
        self.female = female

    def BFS(self, start_id , warmup = 0):

        all = start_id
        valid = start_id

        a = start_id
        v = start_id

        counter = 0
        step_counter = warmup
        time_start = time.time()

        while len(v) is not 0:
            step_counter += 1
            tmp_a = []
            tmp_v = []
            for id in v:
                step_a ,step_v = step(id, step_counter, self.year, self.min_rel, self.min_social_rel, self.female)
                tmp_a.extend(step_a)
                tmp_v.extend(step_v)
            a = tmp_a
            v = tmp_v
            all.extend(a)
            valid.extend(v)
            counter += len(v)
            step_time = time.time() - time_start
            path = os.path.abspath('..')
            f = open(path + "/data/valid_" + str(step_counter) + "/step_message.txt",'w')
            print("After " + str(step_counter) + " steps, " + "valid datasize:" + str(counter), file = f)
            print("Time used:" + str(step_time) + "s", file = f)
            print("Step valid IDs:", file = f)
            for i in v:
                print(str(i), file = f)
            print("After " + str(step_counter) + " steps, " + "valid datasize:" + str(counter))
            print("Time used:" + str(step_time) + "s")
            f.close()

        return step_counter, counter, a, v

crawl = Crawler()
start = step_list(0)
total_step, total, all, valid = crawl.BFS(start_id = start, warmup = 0)
print(total_step, total)
path = os.path.abspath('..')
f = open(path + "/data/crawl.txt", 'w')
print("After "+str(total_step)+" steps,"+" valid datasize:" + str(total), file=f)
print("All IDs:", file = f)
for i in all:
    print(str(i), file = f)
print("All valid IDs:", file = f)
for i in valid:
    print(str(i), file = f)
f.close()
