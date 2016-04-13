from xlwt import *
import csv
import os
import time
import logging
import ConfigParser
from pymongo import MongoClient
from datetime import datetime, timedelta

config = ConfigParser.RawConfigParser()
config.read(r"C:\mongo\source\report.cfg")

try:
    dbhost = config.get("base","dbhost")
    
    statis_field = eval(config.get("base","statis_field"))
    key_field = eval(config.get("base","key_field"))
    sort_field = eval(config.get("base","sort_field"))
    sub_field = eval(config.get("base","sub_field"))
except:
    raise

pre_path = r"C:\mongo\source"
log = logging.getLogger("O2batchtest")
log.setLevel(logging.DEBUG)
fh = logging.FileHandler(r"C:\\mongo\\source\\reportlog.txt")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',datefmt="%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)
log.addHandler(fh)

w = Workbook(style_compression=2)
db = MongoClient(dbhost).rpdb.rpinfo



def save_to_excl(table=None):
    index = -1
    for i in outputindex:
        index += 1
        rpt_name = "%s%d.csv" % (table,i)
        pfile = os.path.join(pre_path, rpt_name)
        if not os.path.exists(pfile):
            log.debug("%s not exists" % rpt_name)
            print "%s not exists" % pfile
            raise
        stinfo = os.stat(pfile)
        if stinfo.st_size < 1000:
            log.debug("%s size not updated" % i)
            print "%s size not updated" % pfile
            raise
        if time.time() - stinfo.st_mtime > 86400:
           log.debug("%s size not updated" % i)
           print "%s date not updated" % pfile
           raise
        linx = 0
        index = outputindex.index(i)
        st = outputname[index]
        ws = w.add_sheet(st)
        with open(pfile,"rb") as cf:
            reader = csv.reader(cf)
            for row in reader:
                for colx, value in enumerate(row):
                    if value.find("%") != -1 and value.find("%") != 0:
                        value = float(value[:-1])/100
                        style = XFStyle()
                        style.num_format_str = '0.00%'
                        ws.write(linx, colx,value,style)
                    elif value.find("$") != -1:
                        value = value.replace(",","")
                        value = float(value[1:])
                        style = XFStyle()
                        style.num_format_str = '"$"#,##0.00_);("$"#,##'
                        ws.write(linx, colx,value,style)
                        ws.col(colx).width = 3500
                    elif value.find(".") != -1:
                        value = float(value)
                        style = XFStyle()
                        style.num_format_str = '#,##0'
                        ws.write(linx, colx,value,style)
                    else:
                        try:
                            value = int(value)
                            style = XFStyle()
                            style.num_format_str = '#,##0'
                            ws.write(linx, colx,value,style)
                        except:
                            pass
                            ws.write(linx, colx, value)
                linx += 1
    

if __name__ == "__main__":
    with open(r"C:\\mongo\\source\\report.xls","wb") as pf:
        pass
    outputindex = [1,2]
    outputname = ["campaign dashboard","monthly dashboard"]
    save_to_excl("dash")
    outputindex = []
    outputname = []
    for i in db.find().sort("index",1):
        try:
            i["entry_time"]
        except:
            continue
        filename = i["file"]
        try:
            home_date = config.get("base",filename)
        except:
            print "%s not found homedate" % filename
            continue
        home_date = datetime.strptime(home_date,r"%Y/%m/%d")
        if home_date < datetime(2014,12,16):
            continue
        if home_date > datetime.now():
            continue
        if datetime.now() > home_date + timedelta(days=60):
            continue
        outputindex.append(i["index"])
        if filename == "feb_mar_main1_15.csv":
            filename = "feb_mar_main(a).csv"
        elif filename == "feb_mar_main2_15.csv":
            filename = "feb_mar_main(b).csv"
        elif filename == "jan_feb_remail1_15.csv":
            filename = "jan_feb_remail_1(a).csv"
        elif filename == "jan_feb_remail2_15.csv":
            filename = "jan_feb_remail_1(b).csv"
        outputname.append(filename)
    save_to_excl("rpt_")
    w.save(r"C:\\mongo\\source\\report.xls")
