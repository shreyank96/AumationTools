# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 13:27:54 2020

@author: shrey
"""

import json
import re
from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver

api_key = "AIzaSyDk4rAJT5cIWiox7KlfRcLPf9YWSOKvXqk"

class Helper:
    def __init__(self):
        pass

    def title_to_underscore_title(self, title: str):
        title = re.sub('[\W_]+', "_", title)
        return title.lower()

    def id_from_url(self, url: str):
        return url.rsplit("=", 1)[1]

class YouTubeStats:
    def __init__(self, url: str):
        #self.json_url = urllib.request.urlopen(url)
        self.json_url = request.urlopen(url)
        self.data = json.loads(self.json_url.read())
        
    def print_data(self):
        print(self.data)

    def get_video_title(self):
        return self.data["items"][0]["snippet"]["title"]

    def get_video_description(self):
        return self.data["items"][0]["snippet"]["description"]
    
def get_links(description: str):
    link_indexes = [m.start() for m in re.finditer('https://amzn.to/', description)]
    links = []
    a=0
    for i in link_indexes:
        split_str = description[i:]
        links.insert(a,split_str.split()[0])
        a=a+1
    return links

def print_answers(sortedObj: list):
    for t in sortedObj:
        print(t[1][0])
        print("price: ", end='')
        print(t[1][1], end='')
        print("link: ", end='')
        print(t[0])
        print("count: ", end='')
        print(t[1][2])
        print("***************************************************************************************************************************************************************")

link_file = r"C:\Users\shrey\OneDrive\Desktop\links.csv"

with open(link_file, "r") as f:
    content = f.readlines()

content = list(map(lambda s: s.strip(), content))
content = list(map(lambda s: s.strip(','), content))

helper = Helper()
links = []
total_links = []
for youtube_url in content:
    video_id = helper.id_from_url(youtube_url)
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
    yt_stats = YouTubeStats(url)
    
    title = yt_stats.get_video_title()
    title = helper.title_to_underscore_title(title)

    description = yt_stats.get_video_description()
    
    links = get_links(description)
    total_links.append(links)


items_dict = {}
driver=webdriver.Firefox()

flat_list = []
for lists in total_links:
    for items in lists:
        flat_list.append(items)

for url in flat_list:
    print(url)
    get=driver.get(url)
    html=driver.page_source  
    soup=BeautifulSoup(html,'html.parser')
    price=soup.find('span',id="priceblock_ourprice")
    title=soup.find(id="productTitle")
    if title is not None and price is not None:
        title_txt = title.text.strip('\n')
        price_txt = price.text.strip('\n')
        if url in items_dict:
            count = items_dict.get(url)
            count[2] = count[2]+1
            items_dict.update(url = count)
            print("same link found: " + count[0] + ", count changed to " + str(count[2]))
        else:
            items_dict[url] = [title_txt, price_txt, 1]
            
sortedObj = sorted(items_dict.items(), key=lambda e: e[1][2], reverse=True)

print_answers(sortedObj)


