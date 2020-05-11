#!/usr/bin/env python
# coding: utf-8

# # G마켓 크롤링
# ## Magic 터치식 1구 IH인덕션 전기렌지 IHR-102
#  - 화구: 1
#  - 프리미엄 리뷰: 30
#  - 일반 리뷰: 178

# In[ ]:


from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-div-shm-usage')

## premium review
print('premium review:', end = ' ')
premium_list = []
for i in range(1,7):
    print(i, end = ' ')
    url = 'http://item.gmarket.co.kr/Item?goodscode=811274431'
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    driver.get(url)
    
    selector = "#premium-pagenation-wrap > div.board_pagenation > ul > li:nth-child("+str(i)+") > a"
    element = driver.find_element_by_css_selector(selector)
    driver.execute_script("arguments[0].click()", element)
    time.sleep(3)

    page_source = driver.page_source
    driver.close()

    bsoup = BeautifulSoup(page_source, 'html.parser')

    _text = bsoup.find_all('p', class_='con')
    btext = [i.get_text().replace('\t', '').replace('\n', '') for i in _text]
    premium_review = btext[:5]
    
    _text = bsoup.find_all('dl', class_='writer-info')
    btext = [i.find_all('dd')[0].get_text() for i in _text]
    user = btext[:5]
    
    btext = [i.find_all('dd')[1].get_text() for i in _text]
    date = btext[:5]
    
    _list = []
    for j in range(len(date)):
        _list.append([user[j], date[j], 'IHR-102', 1, premium_review[j], None, 1])
    
    premium_list += _list
    
## text review
print(' ')
print('text review:', end = ' ')
text_review = []
for i in range(1,19):
    print(i, end = ' ')
    url = 'http://item.gmarket.co.kr/Item?goodscode=811274431'
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    driver.get(url)
    
    if(i>10):
        selector = "#text-pagenation-wrap > div.board_pagenation > a.next"
        element = driver.find_element_by_css_selector(selector)
        driver.execute_script("arguments[0].click()", element)
        time.sleep(3)
        selector = "#text-pagenation-wrap > div.board_pagenation > ul > li:nth-child("+str(i%10)+") > a"
    else:
        selector = "#text-pagenation-wrap > div.board_pagenation > ul > li:nth-child("+str(i)+") > a"
    
    element = driver.find_element_by_css_selector(selector)
    driver.execute_script("arguments[0].click()", element)
    time.sleep(3)

    page_source = driver.page_source
    driver.close()

    bsoup = BeautifulSoup(page_source, 'html.parser')

    _text = bsoup.find_all('p', class_='con')
    btext = [i.get_text().replace('\t', '').replace('\n', '') for i in _text]
    premium_review = btext[5:]

    _text = bsoup.find_all('dl', class_='writer-info')
    btext = [i.find_all('dd')[0].get_text() for i in _text]
    user = btext[5:]

    btext = [i.find_all('dd')[1].get_text() for i in _text]
    date = btext[5:]

    _list = []
    for j in range(len(date)):
        _list.append([user[j], date[j], 'IHR-102', 1, premium_review[j], None, 1])

    text_review += _list


# In[ ]:


total_review = premium_list + text_review
for i in range(len(total_review)):
    total_review[i][1] = total_review[i][1].replace('.', '-')

total_review[:5]


# In[ ]:


import pandas as pd

gmarket = pd.DataFrame(total_review, columns = ['user', 'date', 'product_name', 'product_type', 'review', 'rate', 'source'])
gmarket.head()


# In[ ]:


gmarket.to_csv('G마켓 IHR-102.csv', index = False, encoding = 'utf-8')