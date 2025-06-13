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

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import json
 
# 设置Selenium WebDriver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver = webdriver.Chrome()
 
# 访问目标网页
url = 'https://www.hkex.com.hk/Mutual-Market/Stock-Connect?sc_lang=en'  # 替换为实际的URL

response = requests.get(url)
html_content = response.text

# 解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 获取元素
# 通过标签名
titles = soup.find_all('h1')

# 通过class
elements = soup.find_all(class_='row southbound')

# 通过id
element = soup.find(id='some-id')

# 通过属性
links = soup.find_all('a', href=True)

for element in elements:
    print(element.text)

# print(response.text)

# # 使用BeautifulSoup解析页面内容
# soup = BeautifulSoup(response.text, 'html.parser')

# title = soup.find('title').text


# print(f'Title: {title}')

# desired_element = soup.find('div', class_='menu_container_in')
# print(desired_element.text)

# print(soup)

# # 查找指定元素
# element = soup.find('div', class_='section_scroll_tabs')  # 根据需要修改选择器

# # 提取元素内容
# if element:
#     content = element.text
#     print(content)
# else:
#     print('未找到指定元素')


# # 解析HTML内容
# soup = BeautifulSoup(response.text, 'html.parser')

# # 提取数据
# title = soup.title.text
# print(f'网页标题: {title}')

# # 提取所有链接
# links = soup.find_all('a')
# for link in links:
#     print(link.get('href'))

