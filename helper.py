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
    doc_links = re.findall("<a\s+(?:[^>]*?\s+)?href=/(.*?) ", html)
    pprint(doc_links)