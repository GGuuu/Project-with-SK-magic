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

driver = webdriver.Chrome('F:/skmagic/driver/chromedriver.exe')

naver = ['https://search.shopping.naver.com/detail/detail.nhn?nv_mid=6885248208&cat_id=50001857&frm=NVSHATC&query=IHR-102&NaPm=ct%3Dk4ic1ix4%7Cci%3D8c860e27a67485d5a6e6815ca85773206add4f90%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3D5333a1f3b7bf77f0df1ecff6bb283cd26e13da48',
'https://search.shopping.naver.com/detail/detail.nhn?nv_mid=9262577005&cat_id=50001857&frm=NVSHATC&query=IHR-105&NaPm=ct%3Dk4ic4pw0%7Cci%3D87082a35e697bef928d761e5124ca5bcb2de00fc%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3Dc55bc54e4d4feec35e70e632a2e9ad5674601cbf',
'https://search.shopping.naver.com/detail/detail.nhn?nv_mid=10138486489&cat_id=50001858&frm=NVSHATC&query=ERA-F210M&NaPm=ct%3Dk4ic5ifs%7Cci%3D54347f6eb10d3027e819b9ff15fa18db9c1fb53b%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3D1e88b1f8e37d00978c4543811b44730b364f9ec7',
'https://search.shopping.naver.com/detail/detail.nhn?nv_mid=10541612002&cat_id=50001858&frm=NVSHATC&query=ERA-F211M&NaPm=ct%3Dk4ic6a7s%7Cci%3D380578252ee4089bb0d5da05d99a9faf3b40bdb5%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3D8e40a3d3806f967e5fa54c844c94f214929200a0',
'https://search.shopping.naver.com/detail/detail.nhn?nv_mid=10577721929&cat_id=50001858&frm=NVSHATC&query=ERA-F212M&NaPm=ct%3Dk4ic6ovk%7Cci%3D713e0ea5dbece2ff732df87f670f3490bc2dffbe%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3Df8fe3fc8f8e2edf3d66db8fcf233689473bd5277',
'https://search.shopping.naver.com/detail/detail.nhn?nv_mid=10124195751&cat_id=50001858&frm=NVSHATC&query=ERA-B382E&NaPm=ct%3Dk4ic7nlk%7Cci%3D64d7518ab880e9b3cddececd668b14d491f1a9f5%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3D3ed36d5ee46370c7291075fab0ffe9908e76c7d8',
'https://search.shopping.naver.com/detail/detail.nhn?nv_mid=20019478644&cat_id=50007109&frm=NVSHATC&query=ERA-BTS33&NaPm=ct%3Dk4ic8aqw%7Cci%3D3f00cad235d6c6789c2f647ffbe602c38674cc06%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3D62185b5e7d419283e8f6678817705b070de26722']

user = []
date = []
_name = ['IHR-102','IHR-105','ERA-F210M','ERA-F211M','ERA-F212M','ERA-B382E','ERA-BTS33']
_type = [1,1,2,2,2,3,0]
product_name = []
product_type = []
review = []
rate = []
r = []
source = [3]

for idx, link in enumerate(naver):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html,features='lxml')
    last_page = 30
    n = 0
    
    for p in range(1,last_page-1):
        html = driver.page_source
        soup = BeautifulSoup(html,features='lxml')
        div = soup.select('.atc_area')
        for di in div:
            user.append(di.select('.info_cell')[1].text)
            date.append(di.select('.info_cell')[2].text)
            rate.append(di.select_one('.curr_avg').text)
            txt = di.select_one('.atc').text
            txt = txt.replace('\t','').replace('\n','')
            review.append(txt)
            n=n+1
            print(txt)
        try:
            if(p>0 and p-1 % 10 == 0):
                driver.find_element_by_css_selector('#_review_paging > a.next').click()
                time.sleep(10)
            elif(p>10):
                driver.find_element_by_css_selector('#_review_paging > a:nth-child('+str((p%10)+1)+')').click()
                time.sleep(10)
            else:
                driver.find_element_by_css_selector('#_review_paging > a:nth-child('+str(p)+')').click()
                time.sleep(10)
            print('p:', p)
        except Exception as e:
            print('page끝')
            print(e)
            break
    print('idx',idx+1,'page',p,'numofreview',n,'\n')
    if(n!=0):
        product_name.extend([_name[idx]]*(n))
        product_type.extend([_type[idx]]*(n))

source = source*len(user)

data = {'user':user, 'date':date, 'product_name':product_name, 'product_type':product_type, 'review':review, 'rate':rate, 'source':source}
print('user:',len(user),'date:',len(date),'product_name',len(product_name),'product_type:',len(product_type),'review:',len(review),'rate:',len(rate),'source:',len(source))
df = pd.DataFrame(data,columns=['user','date','product_name','product_type','review','rate','source'])
df.set_index(df['user'],inplace=False)
df.to_pickle('naver.p')
df.to_csv('naver.csv')
print('Done')
driver.quit()
