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
                data = json.load(datapath)
                for rel in data['SocialAssociation']:
                    if rel["AssocCode"] not in index.keys():
                        index[rel["AssocCode"]] = rel["AssocName"]
    return index


index = relation_index(3)
dir = os.path.abspath('..') + "/data/relation_checklist.json"
with open(dir, 'w') as f:
    json.dump(index, f, indent=4, ensure_ascii=False)



