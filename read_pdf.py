#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import pdfplumber
import chardet
import pandas as pd
import os
import sys
import json
from collections import deque
import re
from datetime import datetime, timedelta
import glob

class Employee:
    def __init__(self, name, code, date, url):
        self.name = name
        self.code = code
        self.date = date
        self.url = url

def traverse_json(data, my_list):
    queue = deque([(data, '')])
    name = ""
    code = ""
    date = ""
    url = ""
    while queue:
        value, prefix = queue.popleft()
        if isinstance(value, dict):
            for key, val in value.items():
                queue.append((val, prefix + f'["{key}"]'))
        elif isinstance(value, list):
            for i, val in enumerate(value):
                queue.append((val, prefix + f'[{i}]'))
        else:
            # print(prefix, ':', value)
            if (prefix.find("data")!= -1):
                if (prefix.find("SECURITY_CODE")!= -1):
                    code = value + ".SH"
                if (prefix.find("SECURITY_NAME")!= -1):
                    name = value
                if (prefix.find("SSEDATE")!= -1):
                    date = value
                if (prefix.find("URL")!= -1):
                    url = value
                    empl = Employee(name, code, date, url)
                    my_list.append(empl)

def write_csv_from_url(url, code, name,fo):
    # print(url)
    pdf_files = glob.glob('pdf_file/*.pdf')
    print(pdf_files)
    std_code = code[1:6]
    for file_name in pdf_files:
        if file_name.find(std_code) != -1:
            print(f"Processing file: {file_name}")
            pdf =  pdfplumber.open(file_name)
            num_pages = len(pdf.pages)
            print(f"Number of pages: {num_pages}")

            total_num = 0
            for page in pdf.pages:
                table = page.extract_table()
                print("page index: %d" % page.page_number)
                if table:
                    for row in table:
                        if ((row[len(row) - 1] == "A") or (row[len(row) - 1] == "A类")) :
                            if (len(row) == 8) :
                                # print(row, "length: ", len(row))
                                accout = str(row[2]).replace(",", "").replace("\n", "")
                                volume = str(row[5]).replace(",", "").replace("\n", "")
                                amount = str(row[6]).replace(",", "").replace("\n", "")
                                result = code + "," + name + "," + accout + "," + volume + "," + amount
                                fo.write(str(result).replace(" ", "").replace("\n", "") + "\n")
                                total_num += 1
                            elif (len(row) == 10) :
                                # print(row, "length: ", len(row))
                                accout = str(row[2]).replace(",", "").replace("\n", "")
                                volume = str(row[5]).replace(",", "").replace("\n", "")
                                amount = str(row[8]).replace(",", "").replace("\n", "")
                                result = code + "," + name + "," + accout + "," + volume + "," + amount
                                fo.write(str(result).replace(" ", "").replace("\n", "") + "\n")
                                total_num += 1
            print("code: %s, records: %d" % (code,total_num))


os.system('clear')

# 上交所最多支持90天的查询间隔
today = datetime.now()
pre_day = today + timedelta(days=-60)
str_today = datetime.now().strftime('%Y-%m-%d')
str_pre_date = pre_day.strftime('%Y-%m-%d')
if (str_pre_date < "2025-01-01") :
    str_pre_date = "2025-01-01"
print("pre_date: %s, today: %s" % (str_pre_date, str_today))

sh_Referer = "http://www.sse.com.cn"
url = 'http://query.sse.com.cn/security/stock/queryCompanyBulletinNew.do'
params = {
    "BULLETIN_TYPE": "",
    "START_DATE": str_pre_date,
    "END_DATE": str_today,
    # "START_DATE": "2024-11-24",
    # "END_DATE": "2025-02-24",
    "SECURITY_CODE": "",
    "TITLE": "网下初步配售结果及网上中签结果",
    "beginDate": "",
    "endDate": "",
    "isNew": False,
    "isPagination": "true",
    "jsonCallBack": "jsonpCallback75011929",
    "keyWord": "",
    "stockType": "",
    "pageHelp.pageSize": 25,
    "pageHelp.cacheSize": 1,
    "pageHelp.pageNo": 1,
    "pageHelp.beginPage": 1,
    "pageHelp.endPage": 1
}
headers = {
    "Host": "query.sse.com.cn",
    "Referer": sh_Referer,
    "Cookie": "JSESSIONID=4D6B407A317E85E54ED16A98F2933388; ba17301551dcbaf9_gdp_session_id=a35713cf-6eaa-4513-83b9-5647ff0e9899; gdp_user_id=gioenc-7c564284%2Cd861%2C5c4c%2Ccb9g%2Cc4ec1aegggg9; ba17301551dcbaf9_gdp_session_id_sent=a35713cf-6eaa-4513-83b9-5647ff0e9899; acw_sc__v2=684a4271a5fc444698a81af2dd7a5e128f6dd734; ba17301551dcbaf9_gdp_sequence_ids={%22globalKey%22:78%2C%22VISIT%22:2%2C%22PAGE%22:10%2C%22VIEW_CLICK%22:55%2C%22VIEW_CHANGE%22:7%2C%22CUSTOM%22:8}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

file_name = 'downloaded_pdf.pdf'
save_name = '新股网下发行获配明细表.csv'
#save_name = 'aaa.csv'
my_dict = {}


exit_flag = os.path.exists(save_name)
print(exit_flag)
if (exit_flag):
    with open(save_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            result = line[0:4]
            if (result != "code") :
                my_dict[line[0:9]] = 1
    print(my_dict)

fo = open(save_name, "a+") 
if (exit_flag == False):
    fo.write("code,name,配售对象名称,初步配售数量（股), 获配金额（元)\n")

r = requests.get(url=url, params=params, headers=headers)
print(r.status_code)
if r.status_code == 200:
    print("请求成功！")
    result = r.text
    start = result.find("({")
    json_data = r.text[start + 1 : len(result) - 1]
    print("\n")
    format_data = json.loads(json_data)
    my_list = []
    traverse_json(format_data, my_list)
    for value in my_list:
        print(value.name, value.code, value.date, sh_Referer + value.url)
        if value.code in my_dict:
            print("code: %s 存在，不写入" % value.code)
        else:
            print("code: %s 不存在，写入" % value.code)
            write_csv_from_url(sh_Referer + value.url, value.code, value.name, fo)
        #break
fo.close()
