import os
import time
from datetime import datetime
from pymongo import MongoClient
import csv
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read(r"C:\mongo\source\report.cfg")
try:
    dbhost = config.get("base","dbhost")
    pre_path = config.get("base","pre_path")
    statis_field = eval(config.get("base","statis_field"))
    key_field = eval(config.get("base","key_field"))
    sort_field = eval(config.get("base","sort_field"))
    sub_field = eval(config.get("base","sub_field"))
    addl_field = eval(config.get("base","addl_field"))
except:
    raise

db = MongoClient(dbhost).rpdb.rpinfo

cl = MongoClient(dbhost)

def read_header_file(filename):
    with open(filename, "rb") as cf:
        reader = csv.reader(cf)
        header = reader.next()
        for i in header:
            if i in statis_field:
                map_statis_field[i]= header.index(i)
            elif i in key_field:
                map_key_field[i] = header.index(i)
            elif i in sort_field:
                map_sort_field[i] = header.index(i)
            elif i in sub_field:
                map_sub_field[i] = header.index(i)
            elif i in addl_field:
                map_addl_field[i] = header.index(i)

def read_mail_file(filename, maildb):
    maildb.mail.drop()
    with open(filename, "rb") as cf:
        reader = csv.reader(cf)
        reader.next()
        count = 0
        for row in reader:
            count += 1
            data = {}
            key = ""
            for i in key_field:
                if i in map_key_field.keys():
                    index = map_key_field[i]
                    value = row[index]
                    if i in ["zip_code","zip5"]:
                        if len(value) != 5:
                            if len(value) == 4:
                                value = "0" + value
                            else:
                                continue
                    elif i in ["ssn","SSN","social_security_number"]:
                        if len(value) != 8:
                            continue
                        value = str(int(value))
                    elif i in ["lname","last_name"]:
                        value = value.replace(" ","").lower()
                    key += value
            key = key.decode("unicode_escape")
            data["key"] = key
            for n, ind in map_statis_field.iteritems():
                if n in ["scores1","scores2","scores3","scores4"]:
                    try:
                        data[n] = float(row[ind])
                    except:
                        continue
                else:
                    try:
                        data[n] = int(row[ind])
                    except:
                        try:
                            data[n] = int(row[ind].split(".")[0])
                        except:
                            continue
            for n, ind in map_sort_field.iteritems():
                data[n] = row[ind]
            for n, ind in map_sub_field.iteritems():
                data[n] = row[ind]
            for n, ind in map_addl_field.iteritems():
                data[n] = row[ind]
            maildb.mail.insert(data)

if __name__ == "__main__":
    print datetime.now(), " start entry"
    st = time.time()

    for i in db.find().sort("index",1):
        name = i["file"]
        index = i["index"]
        try:
            deltag = i["deleted"]
            if deltag:
                continue
        except:
            pass
        try:
            home_date = config.get("base",name)
        except:
            print "%s not found homedate" % name
            continue
        try:
            entry_time = i["entry_time"]
        except:
            entry_time = 0
        exec("maildb = cl.mail%d" % index)
        if entry_time == 0 or i["modify_time"] > entry_time:
            print "entry data", i["index"]
            filename = os.path.join(pre_path,name)
            map_statis_field = {}
            map_key_field = {}
            map_sort_field = {}
            map_sub_field = {}
            map_addl_field = {}
            read_header_file(filename)
            read_mail_file(filename,maildb)
            i["entry_time"] = time.time()
            _id = i.pop("_id")
            db.update({"_id":_id},{"$set":i})
        maildb.mail.create_index("key")
    delt = time.time() - st
    if delt > 60:
        print "%.1fmin" % (delt/60.0)
    else:
        print "%ds" % delt
