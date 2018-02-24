import json
from urllib import request
import os

class JSONObject:
    def __init__(self,d):
        self.__dict__ = d


def get_json(id = 1763):
    url = "http://cbdb.fas.harvard.edu/cbdbapi/person.php?id="+str(id)+"&o=json"
    path = os.path.abspath('..')
    datapath = path + "/data/raw/"+str(id)+".json"
    f = request.urlretrieve(url, datapath)

def load_json(data):
    data = json.load(data)
    return data

def check_valid(data):
    return

def dump_dict(data):
    d = {}
    basic_info = data['Package']['PersonAuthority']['PersonInfo']['Person']['BasicInfo']
    basic_info_list = ["PersonId", "EngName", "ChName", "IndexYear", "Gender", "YearBirth", "YearDeath", "Dynasty"]
    d['BasicInfo']=simplify(basic_info,basic_info_list)

    # d['BasicInfo']={"PersonId":bi["PersonId"], "EngName":bi["EngName"], "ChName":bi["ChName"],
    #                 "IndexYear":bi["IndexYear"], "Gender":bi["Gender"], "YearBirth":bi["YearBirth"],
    #                 "YearDeath":bi["YearDeath"], "Dynasty":bi["Dynasty"]}
    #
    return d

def simplify(data,list):
    d = {}
    for item in list:
        d[item]=data[item]
    return d


path = os.path.abspath('..')
f = open(path+"/data/raw/1763.json",'r')
d = load_json(f)
print(d['Package']['PersonAuthority']['PersonInfo']['Person']['BasicInfo']['ChName'])
