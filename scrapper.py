# TODO: NaN exceptions

import requests
import numpy as np
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from datetime import datetime
import re
import json

def clean_text(raw_text):
    """Clean the text withing the Main Content"""
    text = raw_text.replace('\xa0', ' ').replace('\t', ' ').replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)  # collapse multiple spaces
    return text.strip()

for i in range(1,2306):
    # page: 1-2305
    webpage_link = "https://www.business-standard.com/latest-news/page-{}".format(i)

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
    driver.get(webpage_link)
    webpage_source = driver.page_source
    driver.quit()

    latest_news = BeautifulSoup(webpage_source, 'lxml')

    articles = latest_news.find_all("div", class_ = "listingstyle_cardlistlist__dfq57 cardlist")

    for article in articles:
        article_link = article.find("a", class_ = "smallcard-title")
        article_link = article_link["href"]

        try:

            is_premium = article.find("span", class_ = "premium_categorytext__IqxZz")

        except:

            is_premium = np.nan

        driver = uc.Chrome(version_main=137)
        driver.get(article_link)
        article_source = driver.page_source
        driver.quit()

        soup = BeautifulSoup(article_source, 'lxml')


        is_live = soup.find("span", class_ = "d-flex LiveButton_livetitle___zRer")

        if not is_live:

            if is_premium:
                premium = "True"
            else:
                premium = "False"

            try:
                # Heading
                title = soup.find("h1").text.strip()
            except:
                title = np.nan


            try:
                # path on bs website
                path = soup.find("div", class_ = "breadcrum").text.strip()
                category = path.split("/")[1].strip()
            except:
                path = np.nan
                category = np.nan

            try:
                # Link to website
                link = article_link
            except:
                link = np.nan


            try:
                # tldr
                tldr = soup.find("h2", class_ = re.compile(r"MainStory.*")).text.strip()
            except:
                tldr = np.nan

            try:
                # Date and Time
                meta_info = soup.find("div", class_ = "meta-info")
                date_time = meta_info["data-expandedtime"]
                date , time = date_time.split("|")
                date = date.strip()         # Date
                time = time.strip()         # Time
                time = time.replace("IST", "").strip()
                datetime_str = f"{date} {time}"
                datetime = datetime.strptime(datetime_str, "%b %d %Y %I:%M %p")     # DateTime Object
            except:
                date = np.nan
                time = np.nan
                datetime = np.nan

            try:
                # Author
                author = soup.find("span", class_ = "MainStory_dtlauthinfo__u_CUx")
                author = author.find("a").text.strip()
            except:
                author = np.nan

            try:
                # Topics
                topics = soup.find("div", class_ = "MainStory_topiclisting__Pomc9")
                topics = topics.find("span").find_all("span")
                topics[:] = [topic.text.strip() for topic in topics]
            except:
                topics = np.nan

            try:
                # Content
                content = soup.find("div", id = "parent_top_div")

                latest_read = content.find("div", class_="mb-20")
                if latest_read:
                    latest_read.decompose()

                read_more = content.find_all("strong", class_ = "read_more")
                for read in read_more:
                    read.decompose()

                content = clean_text(content.text)
            except:
                content = np.nan



            data = {
                "title": title,
                "path": path,
                "category": category,
                "link": link,
                "tldr": tldr,
                "content": content,
                "date": date,
                "time": time,
                "datetime": datetime.isoformat(),  # convert datetime object to string
                "topics": topics,
                "author": author,
                "premium": premium
            }


            print(data)


            with open("articles.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(data, ensure_ascii=False) + "\n")

    print("\033[92m Successfully Done Page {} \033[0m\n".format(i))





