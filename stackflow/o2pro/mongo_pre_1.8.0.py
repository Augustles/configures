import os
import time
from datetime import datetime
from pymongo import MongoClient
import ConfigParser


config = ConfigParser.RawConfigParser()
config.read(r"C:\mongo\source\report.cfg")
def ConfigSectionMap(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        dict1[option] = config.get(section, option)
    return dict1
try:
    dbhost = config.get("base","dbhost")
    pre_path = config.get("base","pre_path")
except:
    raise

indexmap = ConfigSectionMap("index")
db = MongoClient(dbhost).rpdb.rpinfo


if __name__ == "__main__":
    print datetime.now(), " start pre"
    st = time.time()

    maillist = []
    for i in db.find().sort("index",1):
        maillist.append(i["file"])
    for i in  os.listdir(pre_path):
        i = i.lower()
        data = {}
        finfo = os.stat(os.path.join(pre_path, i))
        size = finfo.st_size/1024/1024
        mod_time = finfo.st_mtime
        if size > 10:
            if db.find({"file":i}).count() != 0:
                info = db.find({"file":i})[0]
                info_mod_time = info["modify_time"]
                if info_mod_time != mod_time:
                    _id = info.pop("_id")
                    info["modify_time"] = mod_time
                    db.update({"_id":_id},{"$set":info})
                    print "update modify time %s" % info["index"]
                continue
            new_tag = indexmap.get(i,None)
            if not new_tag:
                continue
            data["index"] = int(new_tag)
            data["file"] = i
            data["modify_time"] = mod_time
            print i, new_tag
            db.insert(data)
    delt = time.time() - st
    if delt > 60:
        print "%.1fmin" % delt/60.0
    else:
        print "%ds" % delt
