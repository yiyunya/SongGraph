# coding: utf-8
import json
from urllib import request
import urllib.error
import json.decoder
import os


def get_json(id, step_counter):
    url = "http://cbdb.fas.harvard.edu/cbdbapi/person.php?id="+str(id)+"&o=json"
    path = os.path.abspath('..')
    datapath = path + "/data/raw_" + str(step_counter) + "/"+str(id)+".json"
    f = request.urlretrieve(url, datapath)

def load_json(data):
    data = json.load(data)
    return data

def check_exist(rel_id, step_counter):
    path = os.path.abspath('..')
    for i in range(step_counter + 1):
        if os.path.exists(path + "/data/raw_" + str(i) + "/" + rel_id + ".json"):
            return True
    return False

def check_list(rel_id, check_list):
    if rel_id in check_list():
        return True
    return False


def check_valid_exist(rel_id, step_counter):
    path = os.path.abspath('..')
    for i in range(step_counter + 1):
        if os.path.exists(path + "/data/valid_" + str(i) + "/" + rel_id + ".json"):
            return True
    return False

def step(id, step_counter, index_year, min_rel, min_social_rel, female):
    path = os.path.abspath('..')
    check_list = []
    for i in range(step_counter+1):
        check_list.extend(step_full_list(i))
    all = []
    valid = []
    f = open(path+"/data/valid_"+str(step_counter-1)+"/"+str(id)+".json",'r')
    data = load_json(f)
    f.close()
    valid_kin = []
    for rel in data['Kinship']:
        rel_id = rel['KinPersonId']
        if (rel_id is not 'Nan') and \
                (check_exist(rel_id, step_counter) is False) and rel_id != '9999' and rel_id != '0':
            try:
                get_json(int(rel_id), step_counter)
                all.append(int(rel_id))
                check_list.append(rel_id)
                f = open(path + "/data/raw_" + str(step_counter) + "/" + rel_id + ".json", 'r')

                d = load_json(f)
                f.close()
                if d['Package']['PersonAuthority']['PersonInfo'] != "":
                    d = dump_dict(d)
                    if check_valid(d,index_year, min_rel, min_social_rel, female) is True:
                        valid.append(int(rel_id))
                        print("Dump No."+d["BasicInfo"]["PersonId"]+" "+d["BasicInfo"]["ChName"])
                        with open(path + "/data/valid_" + str(step_counter) + "/" + rel_id + ".json", 'w') as f:
                            json.dump(d, f, indent=4, ensure_ascii=False)
                        valid_kin.append(rel)
            except json.decoder.JSONDecodeError as decodeerror:
                print("Invalid json, skip " + rel_id)
            except TimeoutError as timeout:
                print("Timeout, skip " + rel_id)
            except urllib.error.URLError as urlerror:
                print("Url error, skip " + rel_id)


        if check_valid_exist(rel_id, step_counter):
            valid_kin.append(rel)
    data['ValidKinship']=valid_kin

    valid_social = []
    for rel in data['SocialAssociation']:
        rel_id = rel["AssocPersonId"]
        if (rel_id is not 'Nan') and (check_exist(rel_id, step_counter) is False) and rel_id != '9999' and rel_id != '0':
            try:
                get_json(int(rel_id), step_counter)
                all.append(int(rel_id))
                check_list.append(rel_id)
                f = open(path + "/data/raw_" + str(step_counter) + "/" + rel_id + ".json", 'r')
                d = load_json(f)
                f.close()
                if d['Package']['PersonAuthority']['PersonInfo'] != "":
                    d = dump_dict(d)
                    if check_valid(d,index_year, min_rel, min_social_rel, female) is True:
                        valid.append(int(rel_id))
                        print("Dump No." + d["BasicInfo"]["PersonId"] + " " + d["BasicInfo"]["ChName"])
                        with open(path + "/data/valid_" + str(step_counter) + "/" + rel_id + ".json", 'w') as f:
                            json.dump(d, f, indent=4, ensure_ascii=False)
                        valid_social.append(rel)

            except json.decoder.JSONDecodeError as decodeerror:
                print("Invalid json, skip " + rel_id)
            except TimeoutError as timeout:
                print("Timeout, skip " + rel_id)
            except urllib.error.URLError as urlerror:
                print("Url error, skip " + rel_id)
        elif rel_id == '9999':
            status = {"StatusName":rel["AssocName"], "StatusCode":rel["AssocCode"]}
            data['Status'].append(status)

        if check_valid_exist(rel_id, step_counter):
            valid_social.append(rel)
    data['ValidSocialAssociation']=valid_social
    with open(path+"/data/valid_"+str(step_counter-1)+"/"+str(id)+".json", 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    f.close()
    return all, valid






def check_valid(data, index_year, min_rel, min_social_rel, female):
    if data['BasicInfo']['IndexYear'] is 'Nan' or '':
        return False
    elif int(data['BasicInfo']['IndexYear']) > index_year:
        return False
    elif int(data['BasicInfo']['IndexYear']) < 1048:
        return False
    elif len(data['Kinship'])+len(data['SocialAssociation']) < min_rel:
        return False
    elif len(data['SocialAssociation']) < min_social_rel:
        return False
    elif female is False:
        if data['BasicInfo']['Gender'] is '1':
            return False
    elif data['BasicInfo']["Dynasty"] == "宋":
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
                d['Address'] = {}
                d['Address'][item] = 'Nan'
            flag = 1
        if flag == 0:
            for item in address_info_list:
                d['Address'] = {}
                d['Address'][item] = 'Nan'
            flag = 1
    else:
        for item in address_info_list:
            d['Address'] = {}
            d['Address'][item] = 'Nan'

    entry_info_list = ["RuShiDoor", "RuShiType", "RuShiYear"]
    if data['Package']['PersonAuthority']['PersonInfo']['Person']["PersonEntryInfo"] is not "":
        entry_info = data['Package']['PersonAuthority']['PersonInfo']['Person']["PersonEntryInfo"]["Entry"]

        if isinstance(entry_info,dict):
            d['Entry']=simplify(entry_info,entry_info_list)
        else:
            for item in entry_info_list:
                d['Entry'] = {}
                d['Entry'][item]='Nan'
    else:
        for item in entry_info_list:
            d['Entry'] = {}
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
                l.append(simplify(i,kin_info_list,social=True))
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
                l.append(simplify(i,social_info_list,social=True))
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




def simplify(data,list,social=False):
    d = {}
    if social == False:
        for item in list:
            if (item in data.keys()) and data[item]!='0' and data[item]!= "未知" and data[item]!="未詳" and data[item]!='':
                d[item]=data[item]
            elif item == "Gender":
                d[item] = "0"
            else:
                d[item]='Nan'
    else:
        for item in list:
            if (item in data.keys()) and data[item]!='':
                d[item]=data[item]
            else:
                d[item]='Nan'
    return d

def step_list(step_counter):
    list = []
    path = os.path.abspath('..')
    dir = path+"/data/valid_"+str(step_counter)+"/"
    files = os.listdir(dir)
    for name in files:
        if (name.endswith(".json")):
            list.append(int(name[:-5]))
    return list


def step_full_list(step_counter):
    list = []
    path = os.path.abspath('..')
    dir = path+"/data/raw_"+str(step_counter)+"/"
    files = os.listdir(dir)
    for name in files:
        if (name.endswith(".json")):
            list.append(int(name[:-5]))
    return list



path = os.path.abspath('..')
f = open(path+"/data/raw_0/1762.json",'r')
d = load_json(f)
f.close()
d = dump_dict(d)
with open(path+"/data/valid_0/1762.json", 'w') as f:
    json.dump(d, f,indent=4,ensure_ascii=False)
f.close()
