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
from io import BytesIO
import subprocess
import subprocess

file_name = 'downloaded_pdf.pdf'
url = 'http://www.sse.com.cn/disclosure/listedinfo/announcement/c/new/2025-06-12/603400_20250612_3FYM.pdf'
# url = 'http://static.sse.com.cn/disclosure/listedinfo/announcement/c/new/2025-03-12/603124_20250312_P9MN.pdf'
# url = 'https://disc.static.szse.cn/download/disc/disk03/finalpage/2025-01-20/9403955d-0c63-4754-b2b2-705671e24669.PDF'
print(url)
cmd = "curl " + url + " --output downloaded_pdf.pdf"
# cmd = f"curl -o {file_name} {url}"
print(cmd)
# exit_code = os.system(cmd)
# sleep_time = 5
# print("Exit code:", exit_code)


# exit_code = os.system(f"curl -o {file_name} {url}")
# if exit_code == 0:
#     print(f"PDF文件已下载保存为: {file_name}")
# else:
#     print(f"下载失败，退出码: {exit_code}")

# subprocess.run(["curl", "-o", file_name, url])    

# 执行curl命令并将输出写入文件
with open(file_name, 'w') as f:
    subprocess.run(['curl', '-s', url], stdout=f, text=True)

print(f"内容已写入 {file_name}")



# headers = {
#     "Host": "query.sse.com.cn",
#     "Referer": "http://www.sse.com.cn",
#     "Cookie": "JSESSIONID=4D6B407A317E85E54ED16A98F2933388; ba17301551dcbaf9_gdp_session_id=a35713cf-6eaa-4513-83b9-5647ff0e9899; gdp_user_id=gioenc-7c564284%2Cd861%2C5c4c%2Ccb9g%2Cc4ec1aegggg9; ba17301551dcbaf9_gdp_session_id_sent=a35713cf-6eaa-4513-83b9-5647ff0e9899; acw_sc__v2=684a4271a5fc444698a81af2dd7a5e128f6dd734; ba17301551dcbaf9_gdp_sequence_ids={%22globalKey%22:78%2C%22VISIT%22:2%2C%22PAGE%22:10%2C%22VIEW_CLICK%22:55%2C%22VIEW_CHANGE%22:7%2C%22CUSTOM%22:8}",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
# }

# # response = requests.get(url=url, headers=headers)
# response = requests.get(url)
# if response.status_code == 200:
#     print("请求成功！")
#     print(response.text)

#     with open('downloaded_pdf.pdf', 'wb') as f:
#         f.write(response.content)
#         f.close()

#         pdf =  pdfplumber.open(file_name)
#         num_pages = len(pdf.pages)
#         print(f"Number of pages: {num_pages}")
# else:
#     print("请求失败，状态码:", response.status_code)


# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
#     "Referer": "http://www.sse.com.cn/"
# }

# try:
#     response = requests.get(url, headers=headers, timeout=10)
#     print(response.headers["Content-Type"])
#     if response.status_code == 200 and "application/pdf" in response.headers.get("Content-Type", ""):
#         with open("sse_file.pdf", "wb") as f:
#             f.write(response.content)
#         print("PDF 下载成功")
#     else:
#         print("请求失败:", response.status_code, response.reason)
# except Exception as e:
#     print("发生错误:", e)









