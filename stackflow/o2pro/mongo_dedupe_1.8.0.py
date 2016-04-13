import os
import time
from datetime import datetime, date, timedelta
from pymongo import MongoClient
import csv
import os
import re
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read(r"C:\mongo\source\report.cfg")
try:
    dbhost = config.get("base","dbhost")
    pre_path = config.get("base","pre_path")
except:
    raise

db = MongoClient(dbhost).rpdb.rpinfo
aiodb = MongoClient(dbhost).rpdb.allinone
rpdb = MongoClient(dbhost)

perf_name = r"o2_report_data.csv"
perf_file = os.path.join(r"C:\SFTP\o2user1\SPVI_Data_Reporting", perf_name)

def rep_stat(appl, loan,req_due_date):
    if appl=="D":
        return {"accepted":0,"converte":0,"due":0,"fpd":0}
    if loan in "NODBCPR":
        if isbusiday(req_due_date, datetime.now()):
            if loan in "BCPR":
                return {"accepted":1,"converte":1,"due":1,"fpd":1}
            else:
                return {"accepted":1,"converte":1,"due":1,"fpd":0}
        else:
            return {"accepted":1,"converte":1,"due":0,"fpd":0}
    else:
        return {"accepted":1,"converte":0,"due":0,"fpd":0}
def isbusiday(dt1, dt2):
    DELT_DAY = 4
    delt = (dt2-dt1).days
    count = 0
    mid = dt1
    for i in range(delt):
        mid = mid + timedelta(days=1)
        if date.isoweekday(mid) not in [6,7]:
            count += 1
            if count >= DELT_DAY:
                return True
        else:
            continue
    return False 
def read_performance_file(mailcl, perfcl):
    perfcl.drop()
    with open(perf_file, "rb") as cf:
        reader = csv.reader(cf)  
        header = reader.next()
        try:
            d_name = header.index("cust_lname")
            d_ssn = header.index("cust_ssn")
            d_appl = header.index("appl_status")
            d_loan = header.index("loan_status")
            d_date = header.index("applicationdate")
            d_zip_code = header.index("cust_zip")
            d_amount = header.index("req_loan_amt")
            d_req_due_date = header.index("req_due_date")
        except Exception, e:
            log.error(e)
            raise
        for row in reader:
            if re.search("\d+\/\d+\/\d+\s+\d+\:\d+\:\d+", row[d_req_due_date]):
                req_due_date = datetime.strptime(row[d_req_due_date],"%Y\%m\%d %H:%M:%S")
            elif re.search("\d+\/\d+\/\d+\s+\d+\:\d+\:\d+.\d+",row[d_req_due_date]):
                req_due_date = datetime.strptime(row[d_req_due_date],"%Y\%m\%d %H:%M:%S.%f")
            elif re.search("\d+\-\d+\-\d+\s+\d+\:\d+\:\d+\.\d+", row[d_req_due_date]):
                req_due_date = datetime.strptime(row[d_req_due_date],"%Y-%m-%d %H:%M:%S.%f")
            elif re.search("\d+\-\d+\-\d+\s+\d+\:\d+\:\d+",row[d_req_due_date]):
                req_due_date = datetime.strptime(row[d_req_due_date],"%Y-%m-%d %H:%M:%S")
            else:
                log.error("datetime format error: %s" % row[d_req_due_date])
                raise
            if re.search("\d+\/\d+\/\d+\s+\d+\:\d+\:\d+", row[d_date]):
                dt = datetime.strptime(row[d_date],"%Y\%m\%d %H:%M:%S")
            elif re.search("\d+\/\d+\/\d+\s+\d+\:\d+\:\d+.\d+",row[d_date]):
                dt = datetime.strptime(row[d_date],"%Y\%m\%d %H:%M:%S.%f")
            elif re.search("\d+\-\d+\-\d+\s+\d+\:\d+\:\d+\.\d+", row[d_date]):
                dt = datetime.strptime(row[d_date],"%Y-%m-%d %H:%M:%S.%f")
            elif re.search("\d+\-\d+\-\d+\s+\d+\:\d+\:\d+",row[d_date]):
                dt = datetime.strptime(row[d_date],"%Y-%m-%d %H:%M:%S")
            else:
                log.error("datetime format error: %s" % row[d_date])
                raise
            t_ssn = row[d_ssn]
            t_name = row[d_name]
            t_appl = row[d_appl]
            t_loan = row[d_loan]
            t_zip = row[d_zip_code]
            mount = int(row[d_amount].split(".")[0])
            if len(t_ssn) == 9:
                t_ssn=t_ssn[1:]
            if len(t_ssn) != 8:
                raise
            t_ssn = str(int(t_ssn))
            t_name = t_name.replace(" ","").lower()
            if len(t_zip) != 5:
                if len(t_zip) == 4:
                    t_zip = "0" + t_zip
                else:
                    continue
            key = t_zip+t_ssn+t_name
            try:
                i = mailcl.find_one({"key":key})
            except:
                continue
            if not i:
                continue
            data = i
            status = rep_stat(t_appl, t_loan, req_due_date)
            data.update(status)
            data['appl'] = datetime(dt.year,dt.month,dt.day)
            if data["appl"] > end_date:
                continue
            if data["appl"] < home_date:
                continue
            data['mount'] = mount
            data.pop("_id")
            
            t = perfcl.find_one({"key":key})
            if not t:
                perfcl.insert(data)
                t = aiodb.find_one({"key":key,"appl":data["appl"]})
                if not t:
                    meta = {"key":key,"appl":data["appl"],"order":index}
                    aiodb.insert(meta)
                else:
                    if t["order"] < index:
                        _id = t["_id"]
                        aiodb.update({"_id":_id},{"$set":{"order":index}})
                continue
            appl = t["appl"]
            old =  t["accepted"]+t["converte"]+t["due"]
            new = data["accepted"]+data["converte"]+data["due"]
            if new > old:
                t.update(data)
                tid = t.pop("_id")
                perfcl.update({"_id":tid},{"$set":t})
                appl = data["appl"]
            elif new == old:
                if data["appl"] < t["appl"]:
                    t.update(data)
                    tid = t.pop("_id")
                    perfcl.update({"_id":tid},{"$set":t})
                    appl = data["appl"]
            t = aiodb.find_one({"key":key,"appl":appl})
            if not t:
                meta = {"key":key,"appl":appl,"order":index}
                aiodb.insert(meta)
            else:
                if t["order"] < index:
                    _id = t["_id"]
                    aiodb.update({"_id":_id},{"$set":{"order":index}})
                    print "all in one update ", index
                    
if __name__ == "__main__":
    print datetime.now(),"start dedupe"
    st = time.time()
    aiodb.drop()
    for i in db.find().sort("index",-1):
        try:
            i["entry_time"]
        except:
            continue
        filename = i["file"]
        index = i["index"]
        try:
            home_date = config.get("base",filename)
        except:
            print "%s not found homedate" % filename
            continue
        home_date = datetime.strptime(home_date,r"%Y/%m/%d")
        exec("mailcl = rpdb.mail%s.mail" % index)
        exec("perfcl = rpdb.mail%s.perf" % index)
        end_date = home_date + timedelta(days=50)
        print "process mail %d" % index
        read_performance_file(mailcl, perfcl)
        i["dedupe_time"] = time.time()
        _id = i.pop("_id")
        db.update({"_id":_id},{"$set":i})
        perfcl.create_index("accepted")
        perfcl.create_index("converte")
        perfcl.create_index("due")
        perfcl.create_index("fpd")
        perfcl.create_index("appl")
    delt = time.time() - st
    if delt > 60:
        print "%.1fmin" % (delt/60.0)
    else:
        print "%ds" % delt
