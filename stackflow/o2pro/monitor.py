import smtplib
import logging
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import email
import os
from datetime import datetime, timedelta
import sys
import time

log = logging.getLogger("O2batch")
log.setLevel(logging.DEBUG)
fh = logging.FileHandler(r"C:\mongo\source\reportlog.txt")
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)
log.addHandler(fh)


def sendmail(msg):
    msg = MIMEText(msg)
    msg["From"] = "o2@cloud-88.com"
    msg["To"] = "1927064778@qq.com"
    msg["Subject"] = "o2 report moniter"
    msg['Date'] = email.Utils.formatdate(localtime=True)
    server = smtplib.SMTP("mail.cloud-88.com")
    server.login('o2@cloud-88.com', 'o2cloud88')
    server.sendmail('o2@cloud-88.com', '1927064778@qq.com', msg.as_string())
    server.sendmail('o2@cloud-88.com', 'Bruce@cloud-88.com', msg.as_string())
    server.quit()


def sendmailattach(send_to):
    msg = MIMEMultipart()
    msg['From'] = 'o2@cloud-88.com'
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "SPVI Direct Mail Reporting"
    msg.attach(MIMEText(" "))

    part = MIMEBase("application", "octet-stream")
    part.set_payload(open(i, "rb").read())
    Encoders.encode_base64(part)
    part.add_header("Content-Disposition",
                    "attachment;filename=%s" % os.path.basename(i))
    msg.attach(part)
    smtp = smtplib.SMTP("mail.cloud-88.com")
    smtp.login('o2@cloud-88.com', 'o2cloud88')
    smtp.sendmail('o2@cloud-88.com', send_to, msg.as_string())
    smtp.close()
if __name__ == "__main__":
    #i  = r"C:\mongo\source\report.xls"
    day = datetime.now()
    day = day + timedelta(days=-1)
    i = r"C:\mongo\source\Report-%d-%d-%d.xls" % (day.month, day.day, day.year)
    if not os.path.exists(i):
        print "file %s not found" % i
        sendmail("report file %s not generats" % i)
        sys.exit()
    stinfo = os.stat(i)
    if time.time() - stinfo.st_mtime > 86400:
        print "file  %s not updated" % i
        sendmail("report file %s not updated" % i)
        sys.exit()
    if stinfo.st_size < 45912:
        print "file %s not big " % i
        sendmail("report file %s not updates" % i)
        os.system(r'C:\mongo\source\mongo_rept_1.81.py')
        os.system(r'C:\mongo\source\mongo_to_excel_1.8.1.py')
        os.system(r'C:\mongo\source\monitor.py')
        sys.exit()
    try:
        sendmailattach(
            ['jamesd@bellicosecapital.com',
             'mattm@bellicosevi.com',
             'tolzer@lendingsciencedm.com',
             'JustinM@bellicosevi.com',
             'BrianM@bellicosevi.com',
             'JohnN@bellicosecapital.com',
             'kkieffer@lendingsciencedm.com',
             'apietra@lendingsciencedm.com',
             'alan@cloud-88.com',
             'Bruce@cloud-88.com',
             'august@cloud-88.com',
             'z.zhang@lendingsciencedm.com',
             'd.daniel@lendingsciencedm.com'])
    except:
        sendmail("report file not sned")
        sys.exit()
    print "send email"
    log.debug("send email")
# if os.path.exists(old_file):
# os.remove(old_file)
# sendmailattach(["jimmy@cloud-88.com"])
