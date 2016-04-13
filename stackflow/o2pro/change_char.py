# coding=utf-8

import os
import time
import shutil


def delete_old_file(day):
    os.chdir(r'E:\DailyImport')
    files = [file for file in os.listdir(".") if file.endswith('.csv')]
    for file in files:
        stat = os.stat(file)
        if time.time() - stat.st_mtime > day * 24 * 60 * 60:
            print 'delete ==> ' + file
            os.remove(file)
delete_old_file(5)


def change_char(file):
    new_file = file[:-4] + time.strftime('_%Y_%m_%d') + file[-4:]
    shutil.copy2(file, new_file)
    with open(file, 'rb') as f:
        with open(r'E:\DailyImport\o2_data_report.csv', 'wb') as w:
            for x in f.readlines():
                if '\x00' in x:
                    w.write(x.replace('\x00', ''))
                else:
                    w.write(x)
change_char(r'E:\DailyImport\O2_report_data_UnifyLMS.csv')
