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

def check_keyword(keyword, file):
    text = textract.process(file)
    text = str(text.lower())
    keyword = keyword.lower()
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



def driver(keyword, to_address):
    d_files = glob.glob("download_files/*.*")
    for d_file in d_files:
        keywords = keyword.split(" ")
        match = 0
        total = len(keywords)
        for k in keywords:
            if check_keyword(k, d_file):
                match = match + 1
        
        with open("sent.json") as f:
            sent = json.load(f)
        sent = sent["done"]

        if match/total >0.6 and d_file not in sent:
            print("Match found. Sending email.")
            add_sent(d_file)
            send_email(d_file, to_address)

def day_driver(keyword, to_address):
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
            download_file(link)
        driver(keyword, to_address)
        print('.')
        time.sleep(3600)