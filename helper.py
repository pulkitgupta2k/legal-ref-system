from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re
import json
import textract
from emailer import send_email
import glob
import os, os.path
from datetime import date
import time

def getHTML(link):
    headers = {'User-agent': 'Mozilla/5.0'}
    req = requests.get(link, headers=headers)
    html = req.content
    return html

# def get_all_judgements():
#     links = ["https://legalref.judiciary.hk/lrs/common/ju/newjudgments.jsp", "https://legalref.judiciary.hk/lrs/common/ju/newjudgments.jsp?datesel=20052020", "https://legalref.judiciary.hk/lrs/common/ju/newjudgments.jsp?datesel=19052020", "https://legalref.judiciary.hk/lrs/common/ju/newjudgments.jsp?datesel=18052020", "https://legalref.judiciary.hk/lrs/common/ju/newjudgments.jsp?datesel=15052020", "https://legalref.judiciary.hk/lrs/common/ju/newjudgments.jsp?datesel=14052020"]
#     doc_links = []
#     for link in links:
#         doc_links = doc_links + getJudgements(link)
#     return doc_links

def getJudgements():
    link = "https://legalref.judiciary.hk/lrs/common/ju/newjudgments.jsp"
    html = str(getHTML(link))
    doc_links = []
    for doc_link in re.findall("<a\s+(?:[^>]*?\s+)?href=/(.*?) ", html):
        doc_link = "https://legalref.judiciary.hk/" + doc_link
        doc_links.append(doc_link)
    return doc_links

def download_file(link):
    name = "download_files/"+link.split('/')[-1]
    d_file = requests.get(link)
    open(name, "wb").write(d_file.content)

def check_keyword(keyword, text):
    text = str(text.lower())
    keyword = keyword.lower()
    # keyword = " {}".format(keyword)
    key_present = text.find(keyword)
    if key_present < 0:
        return False
    return True

def del_files():
    for file in os.scandir("download_files/"):
        if file.name.endswith(".doc") or file.name.endswith(".docx"):
            os.unlink(file.path)

def add_sent(d_file):
    sent = {}
    with open("sent.json" , "r") as f:
        sent = json.load(f)
    sent["done"].append(d_file)
    with open("sent.json" , "w") as fw:
        json.dump(sent, fw)



def driver(keywords_list, to_address):
    d_files = glob.glob("download_files/*.*")
    for d_file in d_files:
        print(d_file)
        try:
            d_file_text = textract.process(d_file)
        except:
            d_file_text = ""
        for keyword in keywords_list:
            with open("sent.json") as f:
                sent = json.load(f)
            if check_keyword(keyword, d_file_text) > 0 and d_file not in sent:
                print("Match found. Sending email.")
                add_sent(d_file)
                send_email(d_file, to_address, keyword)
            sent = sent["done"]


def day_driver(keywords, to_address):
    while True:
        today = str(date.today())
        with open("today.json" , "r") as f:
            d = json.load(f)
        d = d["date"]
        if not today == d:
            t = {}
            t["date"] = today
            with open("today.json" , "w") as fw:
                json.dump(t, fw)
            del_files()
        links = getJudgements()
        for link in links:
            print(link)
            download_file(link)
        driver(keywords, to_address)
        print('.')
        time.sleep(3600)