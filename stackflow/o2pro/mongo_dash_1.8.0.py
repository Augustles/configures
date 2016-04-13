from pymongo import MongoClient
import ConfigParser
import csv
from datetime import datetime
from datetime import timedelta
from bson.code import Code
import time

config = ConfigParser.RawConfigParser()
config.read(r"C:\mongo\source\report.cfg")

try:
    dbhost = config.get("base","dbhost")
    pre_path = config.get("base","pre_path")
except:
    raise
    
db = MongoClient(dbhost).rpdb.rpinfo
rpdb = MongoClient(dbhost)
home_date = None
dep_index = None
dep_homedate = None
depcl = MongoClient(dbhost).rpdb.allinone

def divid(a,b):
    if b!= 0:
        return float(a)/b
    else:
        return "-"
def formatpct(a):
    if type(a) == type("a"):
        return "-"
    else:
        return "%.10f%%" % a
def fmt_pct_divid(a,b):
    if b != 0:
        return "%.10f%%" % (float(a)/b *100)
    else:
        return "-"        
def formatdoller(a):
    if type(a) == type("a"):
        return "-"
    else:
        return "$%.10f" % a
def calc_cpdl(volume,prin_issu):
    if prin_issu == 0:
        return "-"
    elif type(prin_issu) == type("-"):
        return "-"
    else:
        return coef_cost_fund*volume/prin_issu*100        
def pct_divid(a,b):
    if b != 0:
        return float(a)/b *100
    else:
        return "-"

def calc_cost_fund(volume,converted):
    if converted == 0:
        return "-"
    else:
        return "$%.10f" % (volume * coef_cost_fund / converted)        
        
def generate_data(select=None,sumLoan=False):
    depkey = []
    end_date = home_date + timedelta(days=50)
    if depcl:
        rt = depcl.find({"appl":{"$gte":home_date},"order":{"$eq":index}},{"key":1,"_id":0})
        #rt = depcl.find({"order":{"$eq":index}},{"key":1,"_id":0})
        for i in rt:
            depkey.append(i["key"])
    if select:
        total_volume = mailcl.find({"modelvalue":select}).count()
    else:
        total_volume = mailcl.find().count()
    query_resp = {"appl":{"$gte":home_date,"$lte":end_date},"key":{"$in":depkey}}
    if select:
        query_resp["modelvalue"] = select
    Responded = perfcl.find(query_resp).count()
    resp_pct = fmt_pct_divid(Responded, total_volume)
    query_accp = {"accepted":1,"appl":{"$gte":home_date},"key":{"$in":depkey}}
    if select:
        query_accp["modelvalue"] = select
    Accepted = perfcl.find(query_accp).count()
    accpt_pct = fmt_pct_divid(Accepted, Responded)
    query_convt = {"converte":1,"appl":{"$gte":home_date},"key":{"$in":depkey}}
    if select:
        query_convt["modelvalue"] = select
    Converted = perfcl.find(query_convt).count()
    convt_pct = fmt_pct_divid(Converted,Accepted)
    query_due = {"due":1,"appl":{"$gte":home_date},"key":{"$in":depkey}}
    if select:
        query_due["modelvalue"] = select
    Due = perfcl.find(query_due).count()
    query_fpd = {"fpd":1,"appl":{"$gte":home_date},"key":{"$in":depkey}}
    if select:
        query_fpd["modelvalue"] = select
    Fpd = perfcl.find(query_fpd).count()
    fpd_pct = fmt_pct_divid(Fpd, Due)
    cost_funded = calc_cost_fund(total_volume,Converted)
    query_statis = {"appl":{"$gte":home_date},"converte":1,"key":{"$in":depkey}}
    if select:
        query_statis["modelvalue"] = select
    loan = 0
    for data in perfcl.find(query_statis):
        exec("loan += %f" % (data["mount"]))
    _avg_loan = divid(loan,Converted)
    avg_loan = formatdoller(_avg_loan)
    _prin_issued = _avg_loan * Converted
    prin_issued = formatdoller(_prin_issued)
    _cpdl = calc_cpdl(total_volume,_prin_issued)
    cpdl = formatpct(_cpdl)
    if sumLoan:
        return [total_volume,Responded,resp_pct,Accepted,accpt_pct,Converted,convt_pct,\
    cost_funded,Due,Fpd,fpd_pct,loan,prin_issued,cpdl]
    else:
        return [total_volume,Responded,resp_pct,Accepted,accpt_pct,Converted,convt_pct,\
    cost_funded,Due,Fpd,fpd_pct,avg_loan,prin_issued,cpdl]
    
def gengrate_mult_monthes(indexs):
    t_volume = 0
    t_Responded = 0
    t_Accepted = 0
    t_Converted = 0
    t_Due = 0
    t_Fpd = 0
    t_loan = 0
    t_cst_fund = 0
    for i in db.find().sort("index",-1):
        global index
        index = i["index"]
        name = i["file"]
        if index in indexs:
            global mailcl
            global perfcl
            global home_date
            global coef_cost_fund
            try:
                home_date = config.get("base",name)
            except:
                #print "mul %s not found homedate" % name
                continue
            mailcl = eval("rpdb.mail%d.mail" % index)
            perfcl = eval("rpdb.mail%d.perf" % index)
            home_date = datetime.strptime(home_date,r"%Y/%m/%d")
            if name.lower().find("remail") != -1:
                coef_cost_fund = 0.325
            else:
                coef_cost_fund = 0.38
            i = generate_data(None,True)
            volume = i[0]
            Responded = i[1]
            Accepted = i[3]
            Converted = i[5]
            Due = i[8]
            Fpd = i[9]
            loan = i[11]
            t_volume += volume
            t_Responded += Responded
            t_Accepted += Accepted
            t_Converted += Converted
            t_Due += Due
            t_Fpd += Fpd
            t_loan += loan
            t_cst_fund += volume * coef_cost_fund
    resp_pct = fmt_pct_divid(t_Responded, t_volume)
    accpt_pct = fmt_pct_divid(t_Accepted, t_Responded)
    convt_pct = fmt_pct_divid(t_Converted,t_Accepted)
    fpd_pct = fmt_pct_divid(t_Fpd, t_Due)
    cost_funded = "$%.10f" %  (t_cst_fund/t_Converted)
    _avg_loan = t_loan/t_Converted
    avg_loan = formatdoller(_avg_loan)
    _prin_issued = _avg_loan * t_Converted
    prin_issued = formatdoller(_prin_issued)
    _cpdl = t_cst_fund/_prin_issued*100
    cpdl = formatpct(_cpdl)
    return [t_volume,t_Responded,resp_pct,t_Accepted,accpt_pct,t_Converted,\
        convt_pct,cost_funded,t_Due,t_Fpd,fpd_pct,avg_loan,prin_issued,cpdl]
        
def map_reduce(param,query=None):
    map_func = Code("""function () {
                  emit(this.%s,1)
                }""" % param)
    reduce_func = Code("""function(key,values){
                    var total=0;
                    for (var i=0;i<values.length;i++){
                             total += values[i];
                    }
                    return total;
                    }""")
    if query:
        result = mailcl.map_reduce(map_func,reduce_func,"test",query=query)
    else:
        result = mailcl.map_reduce(map_func,reduce_func,"test")
    return result
    
def reduce_ttt(rt_list):
    tmp = {}
    for t in rt_list:
        for i in t.keys():
            try:
                c = tmp[i]
                for n in range(len(c)):
                    c[n] = c[n] + t[i][n]
            except:
                tmp[i] = t[i]
    return tmp
        
def generate_mult_lineassignment(indexs=None,kort="lineassign"):
    list_result = []
    for i in db.find().sort("index",-1):
        map_rt = {}
        index = i["index"]
        if indexs:
            if index not in indexs:
                continue
        name = i["file"]
        global mailcl
        global perfcl
        global home_date
        global coef_cost_fund
        try:
            home_date = config.get("base",name)
        except:
            continue
        mailcl = eval("rpdb.mail%d.mail" % index)
        perfcl = eval("rpdb.mail%d.perf" % index)
        home_date = datetime.strptime(home_date,r"%Y/%m/%d")
        if name.lower().find("remail") != -1:
            coef_cost_fund = 0.325
        else:
            coef_cost_fund = 0.38
        depkey = []
        end_date = home_date + timedelta(days=50)
        rt = depcl.find({"appl":{"$gte":home_date},"order":{"$eq":index}},{"key":1,"_id":0})
        for i in rt:
            depkey.append(i["key"])
        result = map_reduce(kort)
        map_result = {}
        for i in result.find():
            count = i["value"]
            sort = i["_id"]
            query_resp = {"appl":{"$gte":home_date,"$lte":end_date},kort:sort}
            Responded = perfcl.find(query_resp).count()
            if Responded == 0:
                continue

            query_accp = {"accepted":1,kort:sort,"appl":{"$gte":home_date},"key":{"$in":depkey}}
            Accepted = perfcl.find(query_accp).count()

            query_convt = {"appl":{"$gte":home_date},"converte":1,kort:sort,"key":{"$in":depkey}}
            Converted = perfcl.find(query_convt).count()
            
            query_due = {"appl":{"$gte":home_date},"due":1,kort:sort,"key":{"$in":depkey}}
            Due = perfcl.find(query_due).count()
            
            query_fpd = {"appl":{"$gte":home_date},"fpd":1,kort:sort,"key":{"$in":depkey}}
            Fpd = perfcl.find(query_fpd).count()
            
            query_statis = {"appl":{"$gte":home_date},"converte":1,kort:sort,"key":{"$in":depkey}}
            loan = 0
            for data in perfcl.find(query_statis):
                exec("loan += %f" % (data["mount"]))
            if sort:
                sort = sort.split(".")[0].replace("$","").replace(",","")
                try:
                    sort = int(sort)
                except:
                    pass
                map_result[sort] = [count,Responded,Accepted,Converted,Due,Fpd,loan,coef_cost_fund*count]
            else:
                pass
            
        list_result.append(map_result)
    reduce_map = reduce_ttt(list_result)
    all_count = 0
    all_Responded = 0
    all_Accepted = 0
    all_Converted = 0
    all_Due = 0
    all_Fpd = 0
    all_loan = 0
    all_csf_fund = 0
    for v,k in sorted(reduce_map.items()):
        count = k[0] 
        Responded = k[1]
        Accepted = k[2]
        Converted = k[3]
        Due = k[4]
        Fpd = k[5]
        loan = k[6]
        tmp_csf_fund = k[7]
        all_count += count
        all_Responded += Responded
        all_Accepted += Accepted
        all_Converted += Converted
        all_loan += loan
        all_Due += Due
        all_Fpd += Fpd
        resp_pct = fmt_pct_divid(Responded, count)
        accpt_pct = fmt_pct_divid(Accepted, Responded)
        convt_pct = fmt_pct_divid(Converted,Accepted)
        fpd_pct = fmt_pct_divid(Fpd, Due)
        all_csf_fund += tmp_csf_fund
        if Converted!=0:
            cost_funded = "$%.10f" % (tmp_csf_fund/Converted)
        else:
            cost_funded = "$0"
        _avg_loan = divid(loan,Converted)
        avg_loan = formatdoller(_avg_loan)
        if _avg_loan != "-":
            _prin_issued = _avg_loan * Converted
        else:
            _prin_issued = "-"
        prin_issued = formatdoller(_prin_issued)
        if _prin_issued != 0 and _prin_issued != "-":
            _cpdl = tmp_csf_fund/_prin_issued*100
        else:
            _cpdl = 0
        cpdl = formatpct(_cpdl)
        yield [v,count,Responded,resp_pct,Accepted,accpt_pct,Converted,convt_pct,\
        cost_funded,Due,Fpd,fpd_pct,avg_loan,prin_issued,cpdl]
    if kort=="lineassign":
        all_resp_pct = fmt_pct_divid(all_Responded,all_count)
        all_accp_pct = fmt_pct_divid(all_Accepted,all_Responded)
        all_conv_pct = fmt_pct_divid(all_Converted,all_Accepted)
        all_fpd_pct = fmt_pct_divid(all_Fpd,all_Due)
        all_cost_fund = "$%.10f" % (all_csf_fund/all_Converted)
        _all_avg_loan = divid(all_loan,all_Converted)
        all_avg_loan = formatdoller(_all_avg_loan)
        _all_prin_issu = _all_avg_loan*all_Converted
        all_prin_issu = formatdoller(_all_prin_issu)
        _all_cpdl = all_csf_fund/_all_prin_issu*100
        all_cpdl = formatpct(_all_cpdl)
        yield ["ALL",all_count,all_Responded,all_resp_pct,all_Accepted,all_accp_pct,\
        all_Converted,all_conv_pct,all_cost_fund,all_Due,all_Fpd,all_fpd_pct,all_avg_loan,\
        all_prin_issu,all_cpdl]
        
if __name__ == "__main__":
    print datetime.now()
    st = time.time()
    with open(r"C:\mongo\source\dash1.csv", "wb") as pf:
        spaw = csv.writer(pf)
        spaw.writerow(["campaign id","Selection","Total Volume","Responded","cum_resp_pct",\
                       "accepted","accept_pct","converted","converted_pct","Cost/Funded","due",\
                       "fpd","fpd_pct","avg_loan","prin_issued","CPDL"])
        for i in db.find().sort("index",1):
            try:
                i["entry_time"]
            except:
                continue
            name = i["file"]
            global index
            index = i["index"]
            try:
                home_date = config.get("base",name)
            except:
                continue
            home_date = datetime.strptime(home_date,r"%Y/%m/%d")
            if name.lower().find("remail") != -1:
                coef_cost_fund = 0.325
            else:
                coef_cost_fund = 0.38
            print "dash1  process %d" % index
            exec("mailcl = rpdb.mail%d.mail" % index)
            exec("perfcl = rpdb.mail%d.perf" % index)
            if name == "feb_mar_main1_15.csv":
                name = "feb_mar_main(a)_.csv"
            elif name == "feb_mar_main2_15.csv":
                name = "feb_mar_main(b)_.csv"
            elif name == "jan_feb_remail1_15.csv":
                name = "jan_feb_remail1(a)_.csv"
            elif name == "jan_feb_remail2_15.csv":
                name = "jan_feb_remail1(b)_.csv"
            
            lisf = name.split("_")
            campaign = "%s_%s %s" % (lisf[0],lisf[1],lisf[2])
            selection = "ALL"
            result = generate_data(None)
            reuslt = [campaign,selection] + result
            spaw.writerow(reuslt)
            result = generate_data("BC")
            reuslt = [" ","BC"] + result
            spaw.writerow(reuslt)
            result = generate_data("O2")
            reuslt = [" ","O2"] + result
            spaw.writerow(reuslt)
    with open(r"C:\mongo\source\dash2.csv","wb") as pf:
        spaw = csv.writer(pf)
        spaw.writerow(["campaign id","Campaign Drop","Selection","Total Volume","Responded","cum_resp_pct",\
                       "accepted","accept_pct","converted","converted_pct","Cost/Funded","due",\
                       "fpd","fpd_pct","avg_loan","prin_issued","CPDL"])
        print "dash2  start"
        row = gengrate_mult_monthes([7,8,9])
        row = ["Oct/Nov","in home Dec 1","ALL"] + row
        spaw.writerow(row)
        row = gengrate_mult_monthes([10,11,12,13])
        row = ["Nov/Dec","in home Dec 30","ALL"] + row
        spaw.writerow(row)
        row = gengrate_mult_monthes([14,15,16])
        row = ["Jan/Feb","in home Feb 20","ALL"] + row
        spaw.writerow(row)
        spaw.writerow([])
        spaw.writerow(["Current month"])
        spaw.writerow(["line assignment","count","Responded","cum_resp_pct","accepted","accept_pct","converted","converted_pct","Cost/Funded","due","fpd","fpd_pct","avg_loan","prin_issued","CPDL"])
        for i in  generate_mult_lineassignment([14,15,16]):
            spaw.writerow(i)
        spaw.writerow([])
        spaw.writerow(["state","count","Responded","cum_resp_pct","accepted","accept_pct","converted","converted_pct","Cost/Funded","due","fpd","fpd_pct","avg_loan","prin_issued","CPDL"])
        for i in  generate_mult_lineassignment([14,15,16],"state"):
            spaw.writerow(i)
        spaw.writerow([])
        spaw.writerow(["ALL month"])
        spaw.writerow(["line assignment","count","Responded","cum_resp_pct","accepted","accept_pct","converted","converted_pct","Cost/Funded","due","fpd","fpd_pct","avg_loan","prin_issued","CPDL"])
        for i in  generate_mult_lineassignment():
            spaw.writerow(i)
        spaw.writerow([])
        spaw.writerow(["state","count","Responded","cum_resp_pct","accepted","accept_pct","converted","converted_pct","Cost/Funded","due","fpd","fpd_pct","avg_loan","prin_issued","CPDL"])
        for i in  generate_mult_lineassignment(None,"state"):
            spaw.writerow(i)
    delt = time.time() - st
    if delt > 60:
        print "%.1fmin" % (delt/60.0)
    else:
        print "%ds" % delt    
