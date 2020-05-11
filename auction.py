import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import urllib.parse
import csv
import datetime
from selenium import webdriver
import re
import time

driver = webdriver.Chrome()

# user:아이디 date:리뷰작성날짜 product_name:제품명 
# product_type:제품종류(0:하이브리드,1:1구,2:2구,3:3구) 
# review:상품평 rate:평점 
# source:소스이름 0-7(0:11번가, 1:g마켓, 2:옥션, 3:네이버쇼핑, 4:쿠팡, 5:하이마트, 6:신세계몰, 7:CJmall)
# 내가 할 소스 2,3


#auction 2
auction = "http://itempage3.auction.co.kr/DetailView.aspx?itemno=B331881752"
item = ['B331881752','B312618405','B393854791','B386973333','B388203846','B392240802','B392241044','B396385061','B346113909','B703787712']

user = []
date = []
_name = ['IHR-102','IHR-105','ERA-F210M','ERA-F210M','ERA-F210M','ERA-F211M','ERA-F212M','ERA-F212M','ERA-B382E','ERA-BTS33']
_type = [1,1,2,2,2,2,2,2,3,0]
product_name = []
product_type = []
review = []
rate = []
r = []
source = [2]

for idx,i in enumerate(item):
    link = auction + i
    driver.get(link)
    driver.find_element_by_xpath('//*[@id="tap_moving_2"]/a').click()
    html = driver.page_source
    soup = BeautifulSoup(html,features='lxml')
    last_page = soup.select_one('span.text__total > em.text').text
    n = 0
    
    #page2일때 box,div 어떻게 되는지 보기
    for p in range(0, int(last_page)):
        # pages = driver.find_element_by_class_name('box__pagination').find_elements_by_tag_name('a')
        # pages[p].click()
        # box = soup.select('.list__review')
        # time.sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html,features='lxml')
        div = soup.select('.box__content')
        for di in div:
            try:
                txt = di.select_one('.text').text
            except:
                continue
            txt = txt.replace('\t','').replace('\n','')
            if(len(txt)==0):
                continue
            else:
                review.append(txt)
                print(txt)
            
            user.append(di.select_one('.text__writer').text)
            date.append(di.select_one('.text__date').text)
            rate.append(di.select_one('.sprite__vip.image__star-fill')['style'])
            n = n + 1
            # r = list(map(int,re.findall('\d+',di.select_one('.sprite__vip.image__star-fill')['style'])))
        try:
            driver.find_element_by_class_name('link__page-move.link__page-next').click()
            time.sleep(10)
        except:
            print('page끝')
    print('idx',idx+1,'page',p,'numofreview',n,'\n')
    if(n!=0):
        product_name.extend([_name[idx]]*(n))
        product_type.extend([_type[idx]]*(n))

for idx,i in enumerate(rate):
    i = i.replace('width: ','').replace('%','')
    i = int(i)//20
    rate[idx] = i
source = source*len(user)
data = {'user':user, 'date':date, 'product_name':product_name, 'product_type':product_type, 'review':review, 'rate':rate, 'source':source}
print('user:',len(user),'date:',len(date),'product_name',len(product_name),'product_type:',len(product_type),'review:',len(review),'rate:',len(rate),'source:',len(source))
df = pd.DataFrame(data,columns=['user','date','product_name','product_type','review','rate','source'])
df.set_index(df['user'],inplace=False)
df.to_pickle('auction.p')
df.to_csv('auction.csv')
print('Done')
driver.quit()