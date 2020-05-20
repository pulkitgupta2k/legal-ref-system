from bs4 import BeautifulSoup
import requests
from pprint import pprint
import json
import re

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

def downloadfile(link):
    name = "download_files/"+link.split('/')[-1]
    d_file = requests.get(link)
    open(name, "wb").write(d_file.content)

def driver():
    links = getJudgements()
    for link in links:
        downloadfile(link)