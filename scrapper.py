# TODO: NaN exceptions
# FIX: Hit all sites together
# ! What to do with premium reads

import requests
import numpy as np
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from datetime import datetime
import re

def clean_text(raw_text):
    """Clean the text withing the Main Content"""
    text = raw_text.replace('\xa0', ' ').replace('\t', ' ').replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)  # collapse multiple spaces
    return text.strip()


# page: 1-2305
site = "https://www.business-standard.com/markets/news/hdfc-amc-uti-amc-nippon-amc-rise-in-sip-mutual-fund-flows-turn-analysts-bullish-on-amc-stocks-125071000543_1.html"

# title = []
# path = []
# link = []
# tldr = []
# content = []
# date = []
# time = []
# datetime = [] #datetime object
# topics = []
# author = []



driver = uc.Chrome(version_main=137)        # WARNING: Do not change VERSION_MAIN
driver.get(site)
webpage = driver.page_source
driver.quit()

soup = BeautifulSoup(webpage, 'lxml')


# Heading
title = soup.find_all("h1")

# Path on BS website
path = soup.find("div", class_ = "breadcrum").text.strip()

# Link to website
link = site

# tldr
tldr = soup.find("h2", class_ = re.compile(r"MainStory.*")).text.strip()

# Date and Time
meta_info = soup.find("div", class_ = "meta-info")
date_time = meta_info["data-expandedtime"]
date , time = date_time.split("|")
date = date.strip()         # Date
time = time.strip()         # Time
time = time.replace("IST", "").strip()
datetime_str = f"{date} {time}"
datetime = datetime.strptime(datetime_str, "%b %d %Y %I:%M %p")     # DateTime Object

# Author
author = soup.find("span", class_ = "MainStory_dtlauthinfo__u_CUx")
author = author.find("a").text.strip()

# Topics
topics = soup.find("div", class_ = "MainStory_topiclisting__Pomc9")
topics = topics.find("span").find_all("span")
topics[:] = [topic.text.strip() for topic in topics]

# Content
content = soup.find("div", id = "parent_top_div")

latest_read = content.find("div", class_="mb-20")
if latest_read:
    latest_read.decompose()

read_more = content.find_all("strong", class_ = "read_more")
for read in read_more:
    read.decompose()

content = clean_text(content.text)


print(content)




