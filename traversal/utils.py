import json
from urllib import request
import os


def get_json(id):
    url = "http://cbdb.fas.harvard.edu/cbdbapi/person.php?id="+str(id)+"&o=json"
    path = os.path.abspath('..')
    datapath = path + "/data/raw/"+str(id)+".json"
    f = request.urlretrieve(url, datapath)

def load_json(data):
    data = json.load(data)
    return data

def step(id,index_year, min_rel, min_social_rel, female):
    all = []
    f = open(path+"/data/raw/"+str(id)+".json",'r')
    data = load_json(f)
    data = dump_dict(data)

    for rel in data['Kinship']:
        rel_id = rel['KinPersonId']
        if rel_id is not 'Nan':
            get_json(int(rel_id))
            all.append(int(rel_id))




def check_valid(data, index_year, min_rel, min_social_rel, female):
    if data['BasicInfo']['IndexYear'] is 'Nan' or  int(data['BasicInfo']['IndexYear']) > index_year:
        return False
    if len(data['Kinship'])+len(data['SocialAssociation']) < min_rel:
        return False
    if len(data['SocialAssociation']) < min_social_rel:
        return False
    if female is False:
        if data['BasicInfo']['Gender'] is '1':
            return False
    return True


def dump_dict(data):
    d = {}
    basic_info = data['Package']['PersonAuthority']['PersonInfo']['Person']['BasicInfo']
    basic_info_list = ["PersonId", "EngName", "ChName", "IndexYear", "Gender", "YearBirth", "YearDeath", "Dynasty"]
    d['BasicInfo']=simplify(basic_info,basic_info_list)

    address_info_list = ["AddrType", "AddrName", "belongs1_name", "belongs2_name", "belongs3_name"]
    if data['Package']['PersonAuthority']['PersonInfo']['Person']["PersonAddresses"] is not "":
        address_info = data['Package']['PersonAuthority']['PersonInfo']['Person']["PersonAddresses"]["Address"]

        flag = 0
        if isinstance(address_info,dict):
            d['Address']=simplify(address_info,address_info_list)
            flag = 1
        elif isinstance(address_info,list):
            for i in address_info:
                if i["AddrType"]=="籍貫(基本地址)":
                    d['Address'] = simplify(i, address_info_list)
                    flag = 1
                    break
        else:
            for item in address_info_list:
                d['Address'][item] = 'Nan'
            flag = 1
        if flag == 0:
            for item in address_info_list:
                d['Address'][item] = 'Nan'
            flag = 1
    else:
        for item in address_info_list:
            d['Address'][item] = 'Nan'

    entry_info_list = ["RuShiDoor", "RuShiType", "RuShiYear"]
    if data['Package']['PersonAuthority']['PersonInfo']['Person']["PersonEntryInfo"] is not "":
        entry_info = data['Package']['PersonAuthority']['PersonInfo']['Person']["PersonEntryInfo"]["Entry"]

        if isinstance(address_info,dict):
            d['Entry']=simplify(entry_info,entry_info_list)
        else:
            for item in entry_info_list:
                d['Entry'][item]='Nan'
    else:
        for item in entry_info_list:
            d['Entry'][item] = 'Nan'


    status_info_list = ["StatusName"]
    if data['Package']['PersonAuthority']['PersonInfo']['Person']["PersonSocialStatus"] is not "":
        status_info = data['Package']['PersonAuthority']['PersonInfo']['Person']["PersonSocialStatus"]["SocialStatus"]
        if isinstance(status_info,dict):
            d['Status']=[simplify(status_info,status_info_list)]
        elif isinstance(status_info,list):
            l = []
            for i in status_info:
                l.append(simplify(i,status_info_list))
            d['Status']=l
    else:
        d['Status'] = []
        # tmp = {}
        # for item in status_info_list:
        #     tmp[item]='Nan'
        # d['Status']=[tmp]

    kin_info_list = ["KinPersonId", "KinPersonName", "KinCode", "KinRel", "KinRelName"]
    if data['Package']['PersonAuthority']['PersonInfo']['Person']["PersonKinshipInfo"] is not "":
        kin_info = data['Package']['PersonAuthority']['PersonInfo']['Person']["PersonKinshipInfo"]["Kinship"]
        if isinstance(kin_info, dict):
            d['Kinship'] = [simplify(kin_info,kin_info_list)]
        elif isinstance(kin_info, list):
            l = []
            for i in kin_info:
                l.append(simplify(i,kin_info_list))
            d['Kinship']=l
    else:
        d['Kinship'] = []
        # tmp = {}
        # for item in kin_info_list:
        #     tmp[item]='Nan'
        # d['Kinship']=[tmp]

    social_info_list = ["AssocPersonId", "AssocPersonName", "AssocCode", "AssocName"]
    if data['Package']['PersonAuthority']['PersonInfo']['Person']["PersonSocialAssociation"] is not "":
        social_info = data['Package']['PersonAuthority']['PersonInfo']['Person']["PersonSocialAssociation"]["Association"]
        if isinstance(social_info, dict):
            d['SocialAssociation'] = [simplify(social_info, social_info_list)]
        elif isinstance(social_info, list):
            l = []
            for i in social_info:
                l.append(simplify(i,social_info_list))
            d['SocialAssociation'] = l
    else:
        d['SocialAssociation']=[]
        # tmp = {}
        # for item in kin_info_list:
        #     tmp[item]='Nan'
        # d['SocialAssociation']=[tmp]

    # d['BasicInfo']={"PersonId":bi["PersonId"], "EngName":bi["EngName"], "ChName":bi["ChName"],
    #                 "IndexYear":bi["IndexYear"], "Gender":bi["Gender"], "YearBirth":bi["YearBirth"],
    #                 "YearDeath":bi["YearDeath"], "Dynasty":bi["Dynasty"]}
    #
    return d




def simplify(data,list):
    d = {}
    for item in list:
        if (item in data.keys()) and (data[item] is not 0 or "未知" or "未詳" or None or ""):
            d[item]=data[item]
        else:
            d[item]='Nan'
    return d


path = os.path.abspath('..')
f = open(path+"/data/raw/1762.json",'r')
d = load_json(f)
print(d['Package']['PersonAuthority']['PersonInfo']['Person']['BasicInfo']['ChName'])
f.close()
d = dump_dict(d)
with open(path+"/data/valid/1762.json", 'w') as f:
    json.dump(d, f,indent=4)
f.close()
