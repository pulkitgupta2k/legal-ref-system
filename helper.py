from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re
import textract
from emailer import send_email
import glob
import os, os.path

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

def driver(keyword, to_address):
    links = getJudgements()
    for link in links:
        download_file(link)
    d_files = glob.glob("download_files/*.*")
    for d_file in d_files:
        if check_keyword(keyword, d_file):
            print("Found. Sending Email...")
            send_email(d_file, to_address)
    del_files()