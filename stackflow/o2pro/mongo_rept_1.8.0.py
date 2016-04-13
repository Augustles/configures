import os
import time
from datetime import datetime, timedelta
from pymongo import MongoClient
import csv
from collections import OrderedDict
from bson.code import Code
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
except:
    raise

db = MongoClient(dbhost).rpdb.rpinfo
depcl = MongoClient(dbhost).rpdb.allinone
rpdb = MongoClient(dbhost)


def pct_divid(a,b):
    if b != 0:
        return float(a)/b *100
    else:
        return "-"
def fmt_pct_divid(a,b):
    if b != 0:
        return "%.10f%%" % (float(a)/b *100)
    else:
        return "-"
def pct_divid_num(a,b):
    if b== 0:
        return 0
    else:
        return float(a)/b *100
def divid(a,b):
    if b!= 0:
        return float(a)/b
    else:
        return "-"
def calc_cost_fund(a,b):
    if b == 0:
        return "-"
    else:
        return "$%.10f" % (a * coef_cost_fund / b)
def calc_cpdl(a,b):
    if b == 0:
        return "-"
    elif type(b) == type("-"):
        return "-"
    else:
        return coef_cost_fund*a/b*100
def formatdoller(a):
    if type(a) == type("a"):
        return "-"
    else:
        return "$%.10f" % a
def formatpct(a):
    if type(a) == type("a"):
        return "-"
    else:
        return "%.10f%%" % a
def sorted_lineassgin(k,sort,tmp_list):
    if k == "lineassign":
        def funs(k):
            key = k[0]
            if key.find("$") != -1:
                return int(key.split(".")[0].replace(",","").replace("$",""))
            try:
                key = int(key)
            except:
                pass
            return key
        return sorted(tmp_list,key=funs)
    else:
        return tmp_list
        
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

def generate_appl_date(field=None, value=None):
    row_total = []
    map_statis_field["mount"] = 0
    end_date = home_date + timedelta(days=50)
    sort_map = OrderedDict(sorted(map_statis_field.items(), key=lambda x: x[1]))
    head_list = []
    for i in sort_map.keys():
        exec("head_list.append('avg_%s')" % i)
    row_total.append(["application_date","Responded","daily_resp_pct","cum_resp_pct","accepted","accept_pct",\
                      "converte","converted_pct","due","fpd","fpd_pct"]+head_list+["prin_issued","Total Volumn",\
                      "Cost/Funded","CPDL"])
    depkey = []
    rt = depcl.find({"appl":{"$gte":home_date,"$lte":end_date},"order":{"$eq":index}},{"key":1,"_id":0})
    for i in rt:
        depkey.append(i["key"])
    queryall = {}
    if field:
        queryall[field] = value
    total_volume = mailcl.find(queryall).count()
    query_resp = {"appl":{"$gte":home_date,"$lte":end_date},"key":{"$in":depkey}}
    if field:
        query_resp[field] = value
    Responded = perfcl.find(query_resp).count()
    query_accp = {"accepted":1,"appl":{"$gte":home_date},"key":{"$in":depkey}}
    if field:
        query_accp[field] = value
    Accepted = perfcl.find(query_accp).count()
    accpt_pct = pct_divid(Accepted, Responded)
    query_convt = {"converte":1,"appl":{"$gte":home_date},"key":{"$in":depkey}}
    if field:
        query_convt[field] = value
    Converted = perfcl.find(query_convt).count()
    convt_pct = pct_divid(Converted,Accepted)
    query_due = {"due":1,"appl":{"$gte":home_date},"key":{"$in":depkey}}
    if field:
        query_due[field] = value
    Due = perfcl.find(query_due).count()
    query_fpd = {"fpd":1,"appl":{"$gte":home_date},"key":{"$in":depkey}}
    if field:
        query_fpd[field] = value
    Fpd = perfcl.find(query_fpd).count()
    fpd_pct = pct_divid(Fpd, Due)
    for i in sort_map.keys():
        exec("%s = 0" % i)
    query_statis = {"appl":{"$gte":home_date},"converte":1,"key":{"$in":depkey}}
    if field:
        query_statis[field] = value
    for data in perfcl.find(query_statis):
        for i in sort_map.keys():
            exec("%s += %f" % (i, data[i]))
    statis_list = []
    for i in sort_map.keys():
        exec("avg_%s = divid(%s,Converted)" % (i,i))
        exec("statis_list.append(avg_%s)" % i)
    _prin_issued = statis_list[0] * Converted
    prin_issued = formatdoller(_prin_issued)
    statis_list[0] = formatdoller(statis_list[0])
    statis_list.append(prin_issued)
    statis_list.append(total_volume)
    cost_funded = calc_cost_fund(total_volume,Converted)
    statis_list.append(cost_funded)
    _cpdl = calc_cpdl(total_volume,_prin_issued)
    cpdl = formatpct(_cpdl)
    statis_list.append(cpdl)
    if value:
        head_name = value
    else:
        head_name = "ALL"
    row_total.append([head_name,Responded,0,0,Accepted,accpt_pct,Converted,convt_pct,\
                      Due,Fpd,fpd_pct] + statis_list)
    delt = (datetime.now()-home_date).days
    cum_resp_pct = 0
    for i in range(delt):
        datetag = home_date + timedelta(days=i)
        query_resp["appl"] = datetag
        Responded = perfcl.find(query_resp).count()
        query_accp["appl"] = datetag
        Accepted = perfcl.find(query_accp).count()
        accpt_pct = pct_divid(Accepted, Responded)
        query_convt["appl"] = datetag
        Converted = perfcl.find(query_convt).count()
        convt_pct = pct_divid(Converted,Accepted)
        query_due["appl"] = datetag
        Due = perfcl.find(query_due).count()
        query_fpd["appl"] = datetag
        Fpd = perfcl.find(query_fpd).count()
        fpd_pct = pct_divid(Fpd, Due)
        for i in sort_map.keys():
            exec("%s = 0" % i)
        query_statis["appl"] = datetag
        for data in perfcl.find(query_statis):
            for i in sort_map.keys():
                exec("%s += %f" % (i, data[i]))
        statis_list = []
        for i in sort_map.keys():
            exec("avg_%s = divid(%s,Converted)" % (i,i))
            exec("statis_list.append(avg_%s)" % i)
        _prin_issued = statis_list[0] * Converted
        prin_issued = formatdoller(_prin_issued)
        statis_list[0] = formatdoller(statis_list[0])
        statis_list.append(prin_issued)
        statis_list.append("")
        statis_list.append("")
        daily_resp_pct = pct_divid_num(Responded,total_volume)
        cum_resp_pct += daily_resp_pct
        appldate = "%s/%s/%s" %(datetag.year,datetag.month,datetag.day)
        row_total.append([appldate,Responded,daily_resp_pct,cum_resp_pct,Accepted,accpt_pct,Converted,convt_pct,\
                          Due,Fpd,fpd_pct] +statis_list)
    daily_resp_list = [a[2] for a in row_total[1:]]
    pct_daily_resp = sum(daily_resp_list)/len(daily_resp_list)
    row_total[1][2] = pct_daily_resp
    row_total[1][3] = cum_resp_pct
    for a in row_total[1:]:
        a[2] = formatpct(a[2])
        a[3] = formatpct(a[3])
        a[5] = formatpct(a[5])
        a[7] = formatpct(a[7])
        a[10] = formatpct(a[10])
    row_total.append([])
    return row_total

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

def generate_sort_data(field=None,value=None):
    row_total = []
    end_date = home_date + timedelta(days=50)
    for k,v  in one_sort_field.iteritems():
        map_statis_field["mount"] = 0
        sort_map = OrderedDict(sorted(map_statis_field.items(), key=lambda x: x[1]))
        head_list = []
        for i in sort_map.keys():
            exec("head_list.append('avg_%s')" % i)
        depkey = []
        rt = depcl.find({"appl":{"$gte":home_date,"$lte":end_date},"order":{"$eq":index}},{"key":1,"_id":0})
        for i in rt:
            depkey.append(i["key"])
        row_total.append([k,"count","responded","state_coderesp","accepted","accept_pct","converted",\
                          "converted_pct","due","fpd","fpd_pct"]+head_list+["print_issued","cost_funded","cpdl"])
        queryall = {}
        if field:
            queryall[field] = value
        total_volume = mailcl.find(queryall).count()
        query_resp = {"appl":{"$gte":home_date,"$lte":end_date},"key":{"$in":depkey}}
        if field:
            query_resp[field] = value
        Responded = perfcl.find(query_resp).count()
        resp_pct = fmt_pct_divid(Responded, total_volume)
        query_accp = {"accepted":1,"appl":{"$gte":home_date},"key":{"$in":depkey}}
        if field:
            query_accp[field] = value
        Accepted = perfcl.find(query_accp).count()
        accpt_pct = fmt_pct_divid(Accepted, Responded)
        query_convt = {"converte":1,"appl":{"$gte":home_date},"key":{"$in":depkey}}
        if field:
            query_convt[field] = value
        Converted = perfcl.find(query_convt).count()
        convt_pct = fmt_pct_divid(Converted,Accepted)
        query_due = {"due":1,"appl":{"$gte":home_date},"key":{"$in":depkey}}
        if field:
            query_due[field] = value
        Due = perfcl.find(query_due).count()
        query_fpd = {"fpd":1,"appl":{"$gte":home_date},"key":{"$in":depkey}}
        if field:
            query_fpd[field] = value
        Fpd = perfcl.find(query_fpd).count()
        fpd_pct = fmt_pct_divid(Fpd, Due)
        for i in sort_map.keys():
            exec("%s = 0" % i)
        query_statis = {"appl":{"$gte":home_date},"converte":1,"key":{"$in":depkey}}
        if field:
            query_statis[field] = value
        for data in perfcl.find(query_statis):
            for i in sort_map.keys():
                exec("%s += %f" % (i, data[i]))
        statis_list = []
        for i in sort_map.keys():
            exec("avg_%s = divid(%s,Converted)" % (i,i))
            exec("statis_list.append(avg_%s)" % i)
        _prin_issued = statis_list[0] * Converted
        prin_issued = formatdoller(_prin_issued)
        statis_list[0] = formatdoller(statis_list[0])
        statis_list.append(prin_issued)
        cost_funded = calc_cost_fund(total_volume,Converted)
        statis_list.append(cost_funded)
        _cpdl = calc_cpdl(total_volume,_prin_issued)
        cpdl = formatpct(_cpdl)
        statis_list.append(cpdl)
        if value:
            head_name = value
        else:
            head_name = "ALL"
        row_total.append([head_name,total_volume,Responded,resp_pct,Accepted,accpt_pct,Converted,convt_pct,\
                          Due,Fpd,fpd_pct] + statis_list)
        result = map_reduce(k,queryall)
        tmp_result = []
        for i in result.find():
            count = i["value"]
            sort = i["_id"]
            query_resp = {"appl":{"$gte":home_date,"$lte":end_date},k:sort,"key":{"$in":depkey}}
            if field:
                query_resp[field] = value
            Responded = perfcl.find(query_resp).count()
            if Responded == 0:
                continue
            resp_pct = fmt_pct_divid(Responded, count)
            query_accp = {"accepted":1,k:sort,"appl":{"$gte":home_date},"key":{"$in":depkey}}
            if field:
                query_accp[field] = value
            Accepted = perfcl.find(query_accp).count()
            accp_pct = fmt_pct_divid(Accepted, Responded)
            query_convt = {"appl":{"$gte":home_date},"converte":1,k:sort,"key":{"$in":depkey}}
            if field:
                query_convt[field] = value
            Converted = perfcl.find(query_convt).count()
            convt_pct = fmt_pct_divid(Converted, Accepted)
            query_due = {"appl":{"$gte":home_date},"due":1,k:sort,"key":{"$in":depkey}}
            if field:
                query_due[field] = value
            Due = perfcl.find(query_due).count()
            query_fpd = {"appl":{"$gte":home_date},"fpd":1,k:sort,"key":{"$in":depkey}}
            if field:
                query_fpd[field] = value
            Fpd = perfcl.find(query_fpd).count()
            fpd_pct = fmt_pct_divid(Fpd, Due)

            for i in sort_map.keys():
                exec("%s = 0" % i)
            query_statis = {"appl":{"$gte":home_date},"converte":1,k:sort,"key":{"$in":depkey}}
            if field:
                query_statis[field] = value
            for data in perfcl.find(query_statis):
                for i in sort_map.keys():
                    exec("%s += %f" % (i, data[i]))
            statis_list = []
            for i in sort_map.keys():
                exec("avg_%s = divid(%s,Converted)" % (i,i))
                exec("statis_list.append(avg_%s)" % i)
            _prin_issued = statis_list[0] * Converted
            prin_issued = formatdoller(_prin_issued)
            statis_list[0] = formatdoller(statis_list[0])
            statis_list.append(prin_issued)
            cost_funded = calc_cost_fund(count,Converted)
            statis_list.append(cost_funded)
            _cpdl = calc_cpdl(count,_prin_issued)
            cpdl = formatpct(_cpdl)
            statis_list.append(cpdl)
            tmp_result.append([sort, count,Responded,resp_pct,Accepted,accp_pct,Converted,convt_pct,\
                              Due,Fpd,fpd_pct] + statis_list)
        tmp_result = sorted_lineassgin(k,sort,tmp_result)
        row_total.extend(tmp_result)
        row_total.append([])
    return row_total

def generate_resp_risk(x,y):
    end_date = home_date + timedelta(days=50)
    depkey = []
    rt = depcl.find({"appl":{"$gte":home_date,"$lte":end_date},"order":{"$eq":index}},{"key":1,"_id":0})
    for i in rt:
        depkey.append(i["key"])
    for i in range(len(resprange)+1):
        for j in range(len(riskrange)+1):
            exec("resp%d_risk%d_lead = 0" % (i,j))
            exec("resp%d_risk%d_Responded = 0" % (i,j))
            exec("resp%d_risk%d_Accepted = 0" % (i,j))
            exec("resp%d_risk%d_Funded = 0" % (i,j))
            exec("resp%d_risk%d_Due = 0" % (i,j))
            exec("resp%d_risk%d_Fpd = 0" % (i,j))
    for data in perfcl.find({"appl":{"$gte":home_date,"$lte":end_date},"key":{"$in":depkey}}):
        if home_date > data["appl"]:
            continue
        try:
            resp = int(data[x])
            risk = int(data[y])
        except:
            return []
        k_resp = len(resprange)
        k_risk = len(riskrange)
        for i in resprange:
            if resp >= i:
                k_resp =  resprange.index(i)
                break
        for i in riskrange:
            if risk >= i:
                k_risk = riskrange.index(i)
                break
        exec("resp%d_risk%d_Responded += 1" % (k_resp,k_risk))
        if data["accepted"] == 1:
            exec("resp%d_risk%d_Accepted += 1" % (k_resp,k_risk))
        if data["converte"] == 1:
            exec("resp%d_risk%d_Funded += 1" % (k_resp,k_risk))
        if data["due"] == 1:
            exec("resp%d_risk%d_Due += 1" % (k_resp,k_risk))
        if data["fpd"] == 1:
            exec("resp%d_risk%d_Fpd += 1" % (k_resp,k_risk))
    for data in mailcl.find():
        try:
            resp = int(data[x])
            risk = int(data[y])
        except:
            return []
        k_resp = len(resprange)
        k_risk = len(riskrange)
        for i in resprange:
            if resp >= i:
                k_resp =  resprange.index(i)
                break
        for i in riskrange:
            if risk >= i:
                k_risk = riskrange.index(i)
                break
        exec("resp%d_risk%d_lead += 1" % (k_resp,k_risk))
    for i in range(len(resprange)+1):
        exec("resp%d_lead_total = 0" % i)
        exec("resp%d_responded_total = 0" % i)
        exec("resp%d_accepted_total = 0" % i)
        exec("resp%d_funded_total = 0" % i)
        exec("resp%d_due_total = 0" % i)
        exec("resp%d_fpd_total = 0" % i)
        for j in range(len(riskrange)+1):
            exec("resp%d_lead_total += resp%d_risk%d_lead" % (i,i,j))
            exec("resp%d_responded_total += resp%d_risk%d_Responded" % (i,i,j))
            exec("resp%d_accepted_total += resp%d_risk%d_Accepted" % (i,i,j))
            exec("resp%d_funded_total += resp%d_risk%d_Funded" % (i,i,j))
            exec("resp%d_due_total += resp%d_risk%d_Due" % (i,i,j))
            exec("resp%d_fpd_total += resp%d_risk%d_Fpd" % (i,i,j))
            exec("pct_resp%d_risk%d_responded = fmt_pct_divid(resp%d_risk%d_Responded,resp%d_risk%d_lead)" % (i,j,i,j,i,j))
            exec("pct_resp%d_risk%d_accepted = fmt_pct_divid(resp%d_risk%d_Accepted,resp%d_risk%d_Responded)" % (i,j,i,j,i,j))
            exec("pct_resp%d_risk%d_funded = fmt_pct_divid(resp%d_risk%d_Funded,resp%d_risk%d_Accepted)" % (i,j,i,j,i,j))
            exec("pct_resp%d_risk%d_due = fmt_pct_divid(resp%d_risk%d_Due,resp%d_risk%d_Funded)" % (i,j,i,j,i,j))
            exec("pct_resp%d_risk%d_fpd = fmt_pct_divid(resp%d_risk%d_Fpd,resp%d_risk%d_Due)" % (i,j,i,j,i,j))
    for i in range(len(resprange)+1):
        exec("pct_resp%d_responded_total = fmt_pct_divid(resp%d_responded_total,resp%d_lead_total)" % (i,i,i))
        exec("pct_resp%d_accepted_total = fmt_pct_divid(resp%d_accepted_total,resp%d_responded_total)" % (i,i,i))
        exec("pct_resp%d_funded_total = fmt_pct_divid(resp%d_funded_total,resp%d_accepted_total)" % (i,i,i))
        exec("pct_resp%d_due_total = fmt_pct_divid(resp%d_due_total,resp%d_funded_total)" % (i,i,i))
        exec("pct_resp%d_fpd_total = fmt_pct_divid(resp%d_fpd_total,resp%d_due_total)" % (i,i,i))

    for i in range(len(riskrange)+1):
        exec("risk%d_lead_total = 0" % i)
        exec("risk%d_responded_total = 0" % i)
        exec("risk%d_accepted_total = 0" % i)
        exec("risk%d_funded_total = 0" % i)
        exec("risk%d_due_total = 0" % i)
        exec("risk%d_fpd_total = 0" % i)
        for j in range(len(resprange)+1):
            exec("risk%d_lead_total += resp%d_risk%d_lead" % (i,j,i))
            exec("risk%d_responded_total += resp%d_risk%d_Responded" % (i,j,i))
            exec("risk%d_accepted_total += resp%d_risk%d_Accepted" % (i,j,i))
            exec("risk%d_funded_total += resp%d_risk%d_Funded" % (i,j,i))
            exec("risk%d_due_total += resp%d_risk%d_Due" % (i,j,i))
            exec("risk%d_fpd_total += resp%d_risk%d_Fpd" % (i,j,i))
    for i in range(len(riskrange)+1):
        exec("pct_risk%d_responded_total = fmt_pct_divid(risk%d_responded_total,risk%d_lead_total)" % (i,i,i))
        exec("pct_risk%d_accepted_total = fmt_pct_divid(risk%d_accepted_total, risk%d_responded_total)" % (i,i,i))
        exec("pct_risk%d_funded_total = fmt_pct_divid(risk%d_funded_total, risk%d_accepted_total)" % (i,i,i))
        exec("pct_risk%d_due_total = fmt_pct_divid(risk%d_due_total, risk%d_funded_total)" % (i,i,i))
        exec("pct_risk%d_fpd_total = fmt_pct_divid(risk%d_fpd_total, risk%d_due_total)" % (i,i,i))
    all_lead = 0
    all_responded = 0
    all_accepted = 0
    all_funded = 0
    all_due = 0
    all_fpd = 0
    for i in range(len(riskrange)+1):
        exec("all_lead += risk%d_lead_total" % i)
        exec("all_responded += risk%d_responded_total" % i)
        exec("all_accepted += risk%d_accepted_total" % i)
        exec("all_funded += risk%d_funded_total" % i)
        exec("all_due += risk%d_due_total" % i)
        exec("all_fpd += risk%d_fpd_total" % i)
    pct_all_responded = fmt_pct_divid(all_responded,all_lead)
    pct_all_accepted = fmt_pct_divid(all_accepted,all_responded)
    pct_all_funded = fmt_pct_divid(all_funded,all_accepted)
    pct_all_due = fmt_pct_divid(all_due,all_funded)
    pct_all_fpd = fmt_pct_divid(all_fpd,all_due)
    row_total = []
    row = ["High Score Higher Responded",""]
    row.append("%d+" % riskrange[0])
    for p in range(len(riskrange)):
        if p == len(riskrange) -1:
            break
        row.append("%d-%d" % (riskrange[p+1],riskrange[p]-1))
    row.append("Low-%d" % (riskrange[-1]-1))
    row.extend(["Total","","High Score Higher Responded",""])
    row.append("%d+" % riskrange[0])
    for p in range(len(riskrange)):
        if p == len(riskrange) -1:
            break
        row.append("%d-%d" % (riskrange[p+1],riskrange[p]-1))
    row.append("Low-%d" % (riskrange[-1]-1))
    row.append("Total")
    row_total.append(row)
    for p in range(len(resprange)+1):
        if p == 0:
            row = ["%d+" % resprange[p],"# of leads"]
            plant = "%d+" % resprange[p]
        elif p == len(resprange):
            row = ["low-%d" % (resprange[p-1]-1),"# of leads"]
            plant ="low-%d" % (resprange[p-1]-1)
        else:
            row = ["%d-%d" % (resprange[p],resprange[p-1]-1),"# of leads"]
            plant = "%d-%d" % (resprange[p],resprange[p-1]-1)
        for k in range(len(riskrange)+1):
            exec("row.append(resp%d_risk%d_lead)" % (p,k))
        exec("row.append(resp%d_lead_total)" % p)
        row.append("")
        row.extend([plant,"% of lead"])
        for k in range(len(riskrange)+1):
            exec("row.append(resp%d_risk%d_lead)" % (p,k))
        exec("row.append(resp%d_lead_total)" % p)
        row_total.append(row)

        row = ["","# of responded"]
        for k in range(len(riskrange)+1):
            exec("row.append(resp%d_risk%d_Responded)" % (p,k))
        exec("row.append(resp%d_responded_total)" % p)
        row.extend(["","","% of responded"])
        for k in range(len(riskrange)+1):
            exec("row.append(pct_resp%d_risk%d_responded)" % (p,k))
        exec("row.append(pct_resp%d_responded_total)" % p)

        row_total.append(row)
        row = ["","# of accepts"]
        for k in range(len(riskrange)+1):
            exec("row.append(resp%d_risk%d_Accepted)" %(p,k))
        exec("row.append(resp%d_accepted_total)" % p)
        row.extend(["","","% of accepts"])
        for k in range(len(riskrange)+1):
            exec("row.append(pct_resp%d_risk%d_accepted)" % (p,k))
        exec("row.append(pct_resp%d_accepted_total)" % p)
        row_total.append(row)

        row = ["","# funded"]
        for k in range(len(riskrange)+1):
            exec("row.append(resp%d_risk%d_Funded)" % (p,k))
        exec("row.append(resp%d_funded_total)" % p)
        row.extend(["","","% funded"])
        for k in range(len(riskrange)+1):
            exec("row.append(pct_resp%d_risk%d_funded)" % (p,k))
        exec("row.append(pct_resp%d_funded_total)" % p)
        row_total.append(row)

        row = ["","# due"]
        for k in range(len(riskrange)+1):
            exec("row.append(resp%d_risk%d_Due)" % (p,k))
        exec("row.append(resp%d_due_total)" % p)
        row.extend(["","","% due"])
        for k in range(len(riskrange)+1):
            exec("row.append(pct_resp%d_risk%d_due)" % (p,k))
        exec("row.append(pct_resp%d_due_total)" % p)
        row_total.append(row)

        row = ["","# 1st pay default"]
        for k in range(len(riskrange)+1):
            exec("row.append(resp%d_risk%d_Fpd)" % (p,k))
        exec("row.append(resp%d_fpd_total)" % p)
        row.extend(["","","% 1st pay default"])
        for k in range(len(riskrange)+1):
            exec("row.append(pct_resp%d_risk%d_fpd)" % (p,k))
        exec("row.append(pct_resp%d_fpd_total)" % p)
        row_total.append(row)

    row = ["Overall","# of leads"]
    for p in range(len(riskrange)+1):
        exec("row.append(risk%d_lead_total)" % p)
    row.extend([all_lead,"","Overall","% of leads"])
    for p in range(len(riskrange)+1):
        exec("row.append(risk%d_lead_total)" % p)
    row.append(all_lead)
    row_total.append(row)

    row = ["","# of responded"]
    for p in range(len(riskrange)+1):
        exec("row.append(risk%d_responded_total)" % p)
    row.extend([all_responded,"","","% of responded"])
    for p in range(len(riskrange)+1):
        exec("row.append(pct_risk%d_responded_total)" % p)
    row.append(pct_all_responded)
    row_total.append(row)

    row = ["","# of acccepted"]
    for p in range(len(riskrange)+1):
        exec("row.append(risk%d_accepted_total)" % p)
    row.extend([all_accepted,"","","% of accepted"])
    for p in range(len(riskrange)+1):
        exec("row.append(pct_risk%d_accepted_total)" % p)
    row.append(pct_all_accepted)
    row_total.append(row)

    row = ["","# funded"]
    for p in range(len(riskrange)+1):
        exec("row.append(risk%d_funded_total)" % p)
    row.extend([all_funded,"","","% funded"])
    for p in range(len(riskrange)+1):
        exec("row.append(pct_risk%d_funded_total)" % p)
    row.append(pct_all_funded)
    row_total.append(row)

    row = ["","# due"]
    for p in range(len(riskrange)+1):
        exec("row.append(risk%d_due_total)" % p)
    row.extend([all_due,"","","% due"])
    for p in range(len(riskrange)+1):
        exec("row.append(pct_risk%d_due_total)" % p)
    row.append(pct_all_due)
    row_total.append(row)

    row = ["","# 1st pay default"]
    for p in range(len(riskrange)+1):
        exec("row.append(risk%d_fpd_total)" % p)
    row.extend([all_fpd,"","","% 1st pay default"])
    for p in range(len(riskrange)+1):
        exec("row.append(pct_risk%d_fpd_total)" % p)
    row.append(pct_all_fpd)
    row_total.append(row)

    return row_total

if __name__ == "__main__":
    print datetime.now(), " start report"
    st = time.time()
    for i in db.find().sort("index",-1):
        try:
            i["entry_time"]
        except:
            print "not found entry time"
            continue
        filename = i["file"]
        index = i["index"]
        
        try:
            home_date = config.get("base",filename)
        except:
            print "%s not found homedate" % filename
            continue
        
        home_date = datetime.strptime(home_date,r"%Y/%m/%d")
        if home_date < datetime(2014,12,15):
            continue
        if home_date > datetime.now():
            continue
        print "process index: %d" % index
        filename = os.path.join(pre_path, filename)
        if filename.lower().find("remail") != -1:
            coef_cost_fund = 0.325
        else:
            coef_cost_fund = 0.38
        map_statis_field = {}
        map_key_field = {}
        map_sort_field = {}
        map_sub_field = {}
        read_header_file(filename)
        rpt_file = r"C:\mongo\source\rpt_%d.csv" % index
        exec("mailcl = rpdb.mail%d.mail" % index)
        exec("perfcl = rpdb.mail%d.perf" % index)

        for i in map_sub_field.keys():
            mailcl.create_index(i)
        for i in map_sort_field.keys():
            mailcl.create_index(i)
        sub_value = {}
        for k in map_sub_field.keys():
            for i in perfcl.find():
                sub_value[i[k]] = k
        with open(rpt_file, "wb") as pf:
            spaw = csv.writer(pf)
            dateresult = generate_appl_date()
            spaw.writerow(dateresult[0])
            spaw.writerow(dateresult[1])
            datesubresult = []
            if len(sub_value.keys()) > 1:
                for k,v in sub_value.iteritems():
                    result = generate_appl_date(v,k)
                    spaw.writerow(result[1])
                    dateresult.extend(result)
            spaw.writerow([])

            for key_sort in map_sort_field.keys():
                one_sort_field = {key_sort: map_sort_field[key_sort]}
                result = generate_sort_data()
                for r in result:
                    spaw.writerow(r)
                if key_sort in  ["state","stateflag"]:
                    continue
                    
                if len(sub_value.keys()) > 1:
                    for k,v in sub_value.iteritems():
                        result = generate_sort_data(v, k)
                        for r in result:
                            spaw.writerow(r)

            for r in dateresult:
                spaw.writerow(r)
            for sub in datesubresult:
                for r in sub:
                    spaw.writerow(r)

            resprange = [239,164,123,95,76,60,48,37,25]
            riskrange = [938,921,903,884,850]
            result = generate_resp_risk("resp","risk")
            for r in result:
                spaw.writerow(r)
            spaw.writerow([])
            resprange = [872,832,794,751,700,675,650,600]
            riskrange = [536,428,350,300]
            result = generate_resp_risk("risk_sept","resp_oct")
            for r in result:
                spaw.writerow(r)
    delt = time.time() - st
    if delt > 60:
        print "%.1fmin" % (delt/60.0)
    else:
        print "%ds" % delt
