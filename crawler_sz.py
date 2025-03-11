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
import random
import logging


class Employee:
    def __init__(self, name, code, date, url):
        self.name = name
        self.code = code
        self.date = date
        self.url = url

def traverse_json(data, my_list):
    # 打开一个pdf文档， 看到的地址
    referer = "https://disc.static.szse.cn/download"
    name = ""
    code = ""
    queue = deque([(data, '')])
    while queue:
        value, prefix = queue.popleft()
        if isinstance(value, dict):
            for key, val in value.items():
                queue.append((val, prefix + f'["{key}"]'))
        elif isinstance(value, list):
            for i, val in enumerate(value):
                queue.append((val, prefix + f'[{i}]'))
        else:
            print(prefix, ':', value)
            if (prefix.find("data")!= -1):
                if (prefix.find("secCode")!= -1):
                    code = value + ".SZ"
                if (prefix.find("secName")!= -1):
                    name = value
                    empl = Employee(name, code, "", "")
                    my_list.append(empl)
   
    
    date = ""
    url = ""
    index = 0    
    queue = deque([(data, '')])
    while queue:
        value, prefix = queue.popleft()
        if isinstance(value, dict):
            for key, val in value.items():
                queue.append((val, prefix + f'["{key}"]'))
        elif isinstance(value, list):
            for i, val in enumerate(value):
                queue.append((val, prefix + f'[{i}]'))
        else:
            print(prefix, ':', value)
            if (prefix.find("data")!= -1):
                if (prefix.find("publishTime")!= -1):
                    date = value
                if (prefix.find("attachPath")!= -1):
                    url = value                
                    my_list[index].date = date
                    my_list[index].url = referer + url
                    index+=1
    for value in my_list:
        print(value.name, value.code, value.date, value.url)
    print("\n\n\n")                  
                
def write_csv_from_url(url, code, name,fo):
    print(url)

    response = requests.get(url)
    if response.status_code == 200:
        print("请求成功！")

        with open('downloaded_pdf.pdf', 'wb') as f:
            f.write(response.content)
            f.close()

        pdf =  pdfplumber.open(file_name)
        num_pages = len(pdf.pages)
        print(f"Number of pages: {num_pages}")

        total_num = 0
        for page in pdf.pages:
            table = page.extract_table()
            print("page index: %d" % page.page_number)
            if table:
                for row in table:
                    if (row[len(row) - 1] == "A") :
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


referer = "https://www.szse.cn/disclosure/listed/notice/index.html"
url = 'https://www.szse.cn/api/disc/announcement/annList?random=%s' % random.random()

headers = {'Accept': 'application/json, text/javascript, */*; q=0.01'
    ,'Accept-Encoding': 'gzip, deflate'
    ,'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    ,'Content-Type': 'application/json'
    ,'Host': 'www.szse.cn'
    ,'Origin': 'http://www.szse.cn'
    ,'Proxy-Connection': 'close'
    ,'Referer': 'https://www.szse.cn/disclosure/listed/notice/index.html'
    ,'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/74.0.3729.169 Safari/537.36'
    ,'X-Request-Type': 'ajax'
    ,'X-Requested-With': 'XMLHttpRequest'
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

today = datetime.now()
pre_day = today + timedelta(days=-90)
str_today = datetime.now().strftime('%Y-%m-%d')
str_pre_date = pre_day.strftime('%Y-%m-%d')
if (str_pre_date < "2025-01-01") :
    str_pre_date = "2025-01-01"
print("pre_date: %s, today: %s" % (str_pre_date, str_today))
# payload = {"seDate":["2021-01-01","2025-01-31"],"channelCode":["listedNotice_disc"],"searchKey":["网下发行初步配售结果公告"],"pageSize":50,"pageNum":1}
payload = {"seDate":[str_pre_date, str_today],"channelCode":["listedNotice_disc"],"searchKey":["网下发行初步配售结果公告"],"pageSize":50,"pageNum":1}
r = requests.post(url,headers =headers,data = json.dumps(payload))
print(r.status_code)
if r.status_code == 200:
    print("请求成功！")
    result = r.text
    format_data = json.loads(result)
    my_list = []
    traverse_json(format_data, my_list)
    for value in my_list:
        print(value.name, value.code, value.date, value.url)
        if value.code in my_dict:
            print("code: %s 存在，不写入" % value.code)
        else:
            print("code: %s 不存在，写入" % value.code)
            write_csv_from_url(value.url, value.code, value.name, fo)
        # break


# code = "001395.SZ"
# name = "亚联机械"
# pdf_url = "https://disc.static.szse.cn/download/disc/disk03/finalpage/2025-01-20/9403955d-0c63-4754-b2b2-705671e24669.PDF"

# # write_csv_from_url(pdf_url, code, name, fo)


# # response = requests.get(pdf_url)
# # if response.status_code == 200:
# #     print("请求成功！")

# #     with open('downloaded_pdf.pdf', 'wb') as f:
# #         f.write(response.content)
# #         f.close()

# pdf =  pdfplumber.open(file_name)
# num_pages = len(pdf.pages)
# print(f"Number of pages: {num_pages}")


# total_num = 0
# for page in pdf.pages:
#     table = page.extract_table()
#     # table = pdf.pages[200].extract_table()
#     print("page index: %d" % page.page_number)
#     if table:
#         for row in table:
#             if (row[len(row) - 1] == "A") :
#                 if (len(row) == 8) :
#                     # print(row, "length: ", len(row))
#                     accout = str(row[2]).replace(",", "").replace("\n", "")
#                     volume = str(row[5]).replace(",", "").replace("\n", "")
#                     amount = str(row[6]).replace(",", "").replace("\n", "")
#                     result = code + "," + name + "," + accout + "," + volume + "," + amount
#                     fo.write(str(result).replace(" ", "").replace("\n", "") + "\n")
#                     total_num += 1
#                 elif (len(row) == 10) :
#                     # print(row, "length: ", len(row))
#                     accout = str(row[2]).replace(",", "").replace("\n", "")
#                     volume = str(row[5]).replace(",", "").replace("\n", "")
#                     amount = str(row[8]).replace(",", "").replace("\n", "")
#                     result = code + "," + name + "," + accout + "," + volume + "," + amount
#                     fo.write(str(result).replace(" ", "").replace("\n", "") + "\n")
#                     total_num += 1
# print("code: %s, records: %d" % (code,total_num))                

