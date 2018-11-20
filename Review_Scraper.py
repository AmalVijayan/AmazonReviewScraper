#!/usr/bin/python
# -*- coding: utf-8 -*-
#import urllib.request
#import urllib.parse
#import urllib.error
from bs4 import BeautifulSoup as bsoup
import ssl
import json
import requests as rq
import re

base_url = '#customer reviews page of any product'
r = rq.get(base_url)
soup = bsoup(r.text)

# Using regular expression to identify page numbers from the page navigation buttons, the one you click on.
page_count_links = soup.find_all("a",href=re.compile(r'.*/..../product-reviews/B....1.*pageNumber=\d')) #edit the regex to match the url

# If only one page then default it to 1
try: 
    no = re.sub('[^0-9]','',page_count_links[-2].get_text()) # [-2] because last button is often the "Next" button pointing to page-2
    num_pages = int(no)
except IndexError:
    num_pages = 1

# Add 1 because Python range.
url_list = ["{}&pageNumber={}".format(base_url, str(page)) for page in range(1, num_pages + 1)]

len(url_list) # prints the total number of pages to be scraped

# For ignoring SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


####SCRAPING
product_json = {}
product_json['short-reviews'] = []
product_json['short-reviews-stars'] = [] 
leng = 0
with open('drive/My Drive/practice/product_colab_seagate.json', 'w+') as outfile:
    for url in url_list:
        print("\n++++++++++++Processing page ",i,"/",len(url_list))
        i=i+1
        #url = url_list[i]
        #html = urllib.request.urlopen(url,timeout=10, context=ctx).read()
        page = rq.get(url)
        html = page.text
        soup = bsoup(html, 'html.parser')
        html = soup.prettify('utf-8')
    
        #code to extract the short reviews of the product
    
        for a_tags in soup.findAll('a',
                                   attrs={'class': 'a-size-base a-link-normal review-title a-color-base a-text-bold'}):
            short_review = a_tags.text.strip()
            product_json['short-reviews'].append(short_review)
        
        #code to extract the star rating associated with each short review of the product
        
        for i_tags in soup.findAll('i',
                                   attrs={'data-hook': 'review-star-rating'}):
            for spans in i_tags.findAll('span', attrs={'class': 'a-icon-alt'}):
                  short_review_stars = spans.text.strip()
                  product_json['short-reviews-stars'].append(short_review_stars)
                  break 
        
        if(len(product_json['short-reviews']) == leng):
          print("\n===============Page ",i-1," skipped--")
        leng = len(product_json['short-reviews'])
        print("\nCollected--------Reviews/Rating = ",len(product_json['short-reviews']),"/",len(product_json['short-reviews-stars']))
                  
    json.dump(product_json, outfile, indent=4)
print ('\n\n----------Extraction of data is complete. Check json file.----------')

import pandas as pd
dataframe = pd.read_json('file.json')
