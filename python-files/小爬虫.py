#爬虫
import os
os.system("cls")
print ("Hello 爬虫世界")

import requests
from bs4 import BeautifulSoup

# 第一步：发送请求
url = "https://www.baidu.com"  # 目标网址
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}  # 模拟浏览器，避开简单反爬
response = requests.get(url, headers=headers)

# 检查响应
if response.status_code == 200:
    print("请求成功！")
else:
    print("请求失败，状态码：", response.status_code)
    exit()  # 退出程序

# 第二步：解析 HTML (手动指定UTF-8解码)
soup = BeautifulSoup(response.content.decode("utf-8"), "lxml") 
# 提取标题
title = soup.title.string
print("页面标题：", title)

# 提取所有链接
links = soup.find_all("a")  # 找所有 <a> 标签
for link in links:
    href = link.get("href")  # 获取 href 属性
    text = link.string       # 获取文本
    if text:  # 过滤空文本
        print(f"链接文本：{text},URL:{href}")

# 第三步：保存数据（可选，存到文件）
with open("baidu_links.txt", "w", encoding="utf-8") as f:
    for link in links:
        if link.string:
            f.write(f"{link.string}: {link.get('href')}\n")
print("数据已保存到 baidu_links.txt")