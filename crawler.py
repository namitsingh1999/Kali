#!/usr/bin/env python

import re
import requests

target_url = "https://erp.psit.in"
target_links = []

def extract_links_from(url):
    response = requests.get(target_url)
    return re.findall('(?:href=")(.*?)"', response.content)

def crawl(url):
    href_links = extract_links_from(target_url)
    for link in href_links:

        if "#" in link:
            link = link.split("#")[0]

        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)

crawl(target_url)