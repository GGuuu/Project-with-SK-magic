#!/usr/bin/env python
# coding: utf-8

# In[26]:


import numpy as np
import pandas as pd
import pickle
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests


# In[101]:


columns = ["user", "date", "product_name", "product_type", "review", "rate", "source"]


# In[ ]:


def fun():
    return 0


# ### 하이마트(source=5) / ERA-F212M / 2구

# In[134]:


# use selenium and chromedriver
url = "http://www.e-himart.co.kr/app/goods/goodsDetail?goodsNo=0000064244"
executable_path = "C://Users/YooJehun/PythonProjects/chromedriver_win32/chromedriver.exe"

product_name = "ERA-F212M"
product_type = 2
source = 5

# options = Options()
# options.headless = True
# driver = webdriver.Chrome(executable_path=executable_path, options=options)
driver = webdriver.Chrome(executable_path=executable_path)
# driver.implicitly_wait(3)
driver.get(url)

length = len(driver.find_element_by_class_name("paging").find_elements_by_tag_name("a")) # 4
count = int(driver.find_element_by_class_name("detailTab").find_elements_by_tag_name("a")[2].text[4:6]) # 40

# create DataFrame
himart_era_f212m = pd.DataFrame(columns=columns, index=range(count))
himart_era_f212m["product_name"] = [product_name] * count
himart_era_f212m["product_type"] = [product_type for _ in range(count)]
himart_era_f212m["source"] = [source for _ in range(count)]
display(himart_era_f212m)

idx = 0
for i in range(length):
    pages = driver.find_element_by_class_name("paging").find_elements_by_tag_name("a")
    pages[i].click()
    time.sleep(3)
    users = driver.find_elements_by_class_name("idArea")
    dates = driver.find_elements_by_class_name("dateArea")
#     product_names = driver.find_elements_by_class_name("")
#     product_types = driver.find_elements_by_class_name("")
    reviews = driver.find_elements_by_class_name("new_userCon")
    rates = driver.find_elements_by_class_name("score")
#     sources = driver.find_elements_by_class_name("")
#     time.sleep(3)
    for user, date, review, rate in zip(users, dates, reviews, rates):
        himart_era_f212m.loc[idx ,"user"] = user.text.split("\n")[0] if user.text.split("\n")[0] != '' else np.nan
        himart_era_f212m.loc[idx ,"date"] = date.text.split("\n")[0] if date.text.split("\n")[0] != '' else np.nan
        himart_era_f212m.loc[idx ,"review"] = review.text.split("\n")[0] if review.text.split("\n")[0] != '' else np.nan
        himart_era_f212m.loc[idx ,"rate"] = int(rate.text.split("\n")[0][0]) if rate.text.split("\n")[0] != '' else np.nan
        idx += 1
        print(user.text.split("\n"), date.text.split("\n"), review.text.split("\n"), rate.text.split("\n"))
#         print(user.text.split("\n")[0], date.text.split("\n")[0], review.text.split("\n")[0], rate.text.split("\n")[0])
#         print(type(user.text.split("\n")[0]), type(date.text.split("\n")[0]), type(review.text.split("\n")[0]),\
#               type(rate.text.split("\n")[0]))
display(himart_era_f212m)
himart_era_f212m.to_pickle("data/himart_era_f212m.pkl")
himart_era_f212m.to_csv("data/himart_era_f212m.csv", index=False)


# ### 신세계몰(source=6) / IHR-102 / 1구

# In[133]:


# use selenium and chromedriver
url = "http://www.ssg.com/item/itemView.ssg?itemId=0000010547223&siteNo=6004&salestrNo=6005&tildSrchwd=IHR-102&srchPgNo=1&src_area=ssglist"
executable_path = "C://Users/YooJehun/PythonProjects/chromedriver_win32/chromedriver.exe"

product_name = "IHR-102"
product_type = 1
source = 6

driver = webdriver.Chrome(executable_path=executable_path)
driver.get(url)

length = len(driver.find_elements_by_class_name("cdtl_paginate")[1].find_elements_by_tag_name("a")) + 1 # 2
count = int(driver.find_element_by_id("postngNlistCnt").text) # 12

# create DataFrame
ssgmall_ihr_102 = pd.DataFrame(columns=columns, index=range(count))
ssgmall_ihr_102["product_name"] = [product_name] * count
ssgmall_ihr_102["product_type"] = [product_type for _ in range(count)]
ssgmall_ihr_102["source"] = [source for _ in range(count)]
display(ssgmall_ihr_102)

idx = 0
for i in range(length):
    time.sleep(3)
    users = [string               for sometag in driver.find_element_by_id("cdtl_cmt_tbody").find_elements_by_class_name("user")               for string in sometag.find_elements_by_class_name("in")]
    dates = [string               for sometag in driver.find_element_by_id("cdtl_cmt_tbody").find_elements_by_class_name("date")               for string in sometag.find_elements_by_class_name("in")]
    reviews = [string               for sometag in driver.find_element_by_id("cdtl_cmt_tbody").find_elements_by_class_name("desc_txt")               for string in sometag.find_elements_by_class_name("desc")]
    rates = [string               for sometag in driver.find_element_by_id("cdtl_cmt_tbody").find_elements_by_class_name("star")               for string in sometag.find_elements_by_class_name("blind")]
#     time.sleep(3)
    for user, date, review, rate in zip(users, dates, reviews, rates):
        a = user.text.split("\n")[0]
        b = date.text.split("\n")[0]
        c = review.text.split("\n")[0]
        d = rate.text.split("\n")[0][-2]
        
        ssgmall_ihr_102.loc[idx ,"user"] = a if a != '' else np.nan
        ssgmall_ihr_102.loc[idx ,"date"] = b if b != '' else np.nan
        ssgmall_ihr_102.loc[idx ,"review"] = c if c != '' else np.nan
        ssgmall_ihr_102.loc[idx ,"rate"] = int(d) if d != '' else np.nan
        idx += 1
        
        print(user.text.split("\n")[0], date.text.split("\n")[0], review.text.split("\n")[0], int(rate.text.split("\n")[0][-2]))
    if i != length-1:
        pages = driver.find_elements_by_class_name("cdtl_paginate")[1].find_elements_by_tag_name("a")
        pages[i].click()

display(ssgmall_ihr_102)
ssgmall_ihr_102.to_pickle("data/ssgmall_ihr_102.pkl")
ssgmall_ihr_102.to_csv("data/ssgmall_ihr_102.csv", index=False)


# ### CJmall(source=7) / ERA-BTS33 / 하이브리드

# In[175]:


# use selenium and chromedriver
url = "http://display.cjmall.com/p/item/57628765?channelCode=30001001&k=sk%20%EB%A7%A4%EC%A7%81%20%EC%A0%84%EA%B8%B0%EB%A0%88%EC%9D%B8%EC%A7%80&shop_id=2002112507"
executable_path = "C://Users/YooJehun/PythonProjects/chromedriver_win32/chromedriver.exe"

product_name = "ERA-BTS33"
product_type = 0
source = 7

driver = webdriver.Chrome(executable_path=executable_path)
driver.get(url)

time.sleep(3)
length1 = len(driver.find_element_by_class_name("review_line").find_element_by_class_name("pagination_inner").find_elements_by_tag_name("a")) # 2
length2 = len(driver.find_element_by_class_name("review_premium").find_element_by_class_name("pagination_inner").find_elements_by_tag_name("a")) # 0
count = int(driver.find_element_by_class_name("count").text) # 10

length1 = length1 if length1 else 1
length2 = length2 if length2 else 1

# create DataFrame
# cjmall_era_bts33 = pd.DataFrame(columns=columns, index=range(count))
# cjmall_era_bts33["product_name"] = [product_name] * count
# cjmall_era_bts33["product_type"] = [product_type for _ in range(count)]
# cjmall_era_bts33["source"] = [source for _ in range(count)]
# display(cjmall_era_bts33)

idx = 0
for i in range(length1):
    time.sleep(3)
    users = [string               for sometag in driver.find_element_by_class_name("review_line").find_elements_by_class_name("review_info")               for string in sometag.find_elements_by_tag_name("em")]
    dates = driver.find_element_by_class_name("review_line").find_elements_by_class_name("review_info")
    reviews = driver.find_element_by_class_name("review_line").find_elements_by_class_name("review_scr")
    rates = driver.find_element_by_class_name("review_line").find_elements_by_class_name("star_score")

    for user, date, review, rate in zip(users, dates, reviews, rates):
        a = user.text.split("\n")[0]
        b = date.text.split("\n")[0][-10:]
        c = review.text.split("\n")[0]
        d = rate.text.split("\n")

#         cjmall_era_bts33.loc[idx ,"user"] = a if a != '' else np.nan
#         cjmall_era_bts33.loc[idx ,"date"] = b if b != '' else np.nan
#         cjmall_era_bts33.loc[idx ,"review"] = c if c != '' else np.nan
#         cjmall_era_bts33.loc[idx ,"rate"] = int(d) if d != '' else np.nan
#         idx += 1
        print(a,b,c,d)
    if i != length1-1:
        pages = driver.find_element_by_class_name("review_line").find_element_by_class_name("pagination_inner").find_elements_by_tag_name("a")
        pages[i].click()

length3 = len(driver.find_element_by_class_name("review_premium").find_elements_by_class_name("review_more")) # 2

for i in range(length2):
    for j in range(length3):
        driver.find_element_by_class_name("review_premium").find_elements_by_tag_name("a")[j].click()
        time.sleep(3)
        user = driver.find_element_by_class_name("review_premium").find_elements_by_tag_name("em")[j]
        date = driver.find_element_by_class_name("review_premium").find_elements_by_class_name("review_info")[j]
        review = driver.find_element_by_class_name("review_premium").find_elements_by_class_name("review_scr._brTag")[j]
        rate = driver.find_element_by_class_name("review_premium").find_elements_by_class_name("star_score")[j]

        a = user.text.split("\n")[0]
        b = date.text.split("\n")[0][-10:]
        c = review.text.split("\n")
        d = rate.text.split("\n")

        print(a,b,c,d)
    if i != length2-1:
        pages = driver.find_element_by_class_name("review_premium").find_element_by_class_name("pagination_inner").find_elements_by_tag_name("a")
        pages[i].click()
# display(cjmall_era_bts33)
# cjmall_era_bts33.to_pickle("data/cjmall_era_bts33.pkl")
# cjmall_era_bts33.to_csv("data/cjmall_era_bts33.csv", index=False)


# In[179]:


product_name = "ERA-BTS33"
product_type = 0
source = 7

count = 10
cjmall_era_bts33 = pd.DataFrame(columns=columns, index=range(count))
cjmall_era_bts33["product_name"] = [product_name] * count
cjmall_era_bts33["product_type"] = [product_type for _ in range(count)]
cjmall_era_bts33["source"] = [source for _ in range(count)]

temp_user = ["jjol***", "nasay***", "daumks***", "hyunmohae***", "leso1***", "swh700***", "luzer***", "worud9***", "nasay***", "worud9***"]
temp_date = ["2019-12-22", "2019-12-17", "2019-12-03", "2019-11-26", "2019-11-19", "2019-10-31", "2019-10-04", "2019-08-01", "2019-12-17", "2019-08-01"]
temp_review = [
"감사합니다",
"맘에 들어요",
"최신제품 싸게 구매합니다 배송도 지방인데 1주일 안걸렸네요",
"지정일에 사은품과 함께 설치 잘 받았어요~기사님 친절하시고 설명도 잘해주셨어요.감사합니다",
"만족합니다",
"강추합니다~",
"부모님께서 아주 만족하시네요 사은품도 아주 좋습니다",
"잘받았습니다.",
"설치도 엄청 빠르게 해주셨고 설치비나 프레임이나 추가금액 없어요 기사분들도 무척 친절하셨고 설명도 잘 해주셨어요 사은품으로 주신 냄비도 예쁘네요 아직 사용전이지만 좋을 것 같아요^^ 전기세가 조금 걱정이지만 저렴한 가격에 잘 산 것 같고 고장없이 잘 쓰면 좋겠어요",
"이사 날짜에 맞춰 미리 주문했고 직장인이라 주말 설치 부탁드린다고 말씀드렸는데 설치하는데 15일 걸렸고 월요일에 오셨네요. 선물로 주문한 건데 받는 분이 마음에 든다고 합니다. 같이 온 냄비랑 후라이팬도 유용하게 사용할것 같습니다. 배송요청 사항을 조금 더 참고해 주시고 설치 기간을 단축시켜 주시면 좋을것 같습니다. 많이 파세요."
]
cjmall_era_bts33["user"] = temp_user
cjmall_era_bts33["date"] = temp_date
cjmall_era_bts33["review"] = temp_review

display(cjmall_era_bts33)

cjmall_era_bts33.to_pickle("data/cjmall_era_bts33.pkl")
cjmall_era_bts33.to_csv("data/cjmall_era_bts33.csv", index=False)


# In[ ]:




