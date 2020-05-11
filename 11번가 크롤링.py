#!/usr/bin/env python
# coding: utf-8

# # 11번가 후기 크롤링

# ## IH인덕션 1구 터치식 전기레인 IHR-102
#  - 화구: 1
#  - 리뷰 개수: 230

# In[72]:


import urllib.request
import requests
from bs4 import BeautifulSoup

list_href = []

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

from selenium import webdriver

user_list = []
review_list = []
date_list = []
rate_list = []
total_list = []

for i in range(1,24):
    if(i%10==0):
        print(i)
    url = "http://www.11st.co.kr/product/SellerProductDetail.tmall?method=getProductReviewList&prdNo=1513213158&page=" + str(i) + "&pageTypCd=first&reviewDispYn=Y&isPreview=false&reviewOptDispYn=Y&optSearchBtnAndGraphLayer=Y&reviewBottomBtn=Y&openDetailContents=Y&pageSize=10&isIgnoreAuth=false&lctgrNo=1001434&leafCtgrNo=1009310&groupProductNo=77874&groupFirstViewPrdNo=1513213158&selNo=42673992#this"
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    page_source = ""
    driver.get(url)

    page_source = driver.page_source

    driver.close()

    bsoup = BeautifulSoup(page_source, 'html.parser')
    
    _text = bsoup.find_all('strong', class_='name')
    user = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('span', class_='summ_conts')
    review = [i.get_text().replace('\n','').replace('\t','') for i in _text]
    
    _text = bsoup.find_all('span', class_='date')
    date = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('div', class_='selr_wrap')
    rate = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    for i, r in enumerate(rate):
        if '판매자 평점 별5개 중 5개' in r:
            rate[i] = 5
        elif '판매자 평점 별5개 중 4개' in r:
            rate[i] = 4
        elif '판매자 평점 별5개 중 3개' in r:
            rate[i] = 3
        elif '판매자 평점 별5개 중 2개' in r:
            rate[i] = 2
        else:
            rate[i] = 1
    
    total = []
    for j in range(len(user)):
        total.append([user[j], date[j], 'IHR-102', 1, review[j], rate[j+5], 0])
    
    total_list += total


# In[83]:


import pandas as pd
import numpy as np

IHR = pd.DataFrame(total_list, columns = ['user', 'date', 'product_name', 'product_type', 'review', 'rate', 'source'])


# In[81]:


IHR.to_csv('11번가 IHR-102.csv', encoding = 'utf-8', index = False)


# In[130]:


data = pd.read_csv('11번가 IHR-102.csv', encoding = 'utf-8')
data.tail()


# -----------------------------------------------------------------------------------------------------------------------------------
# ## 포터블 1구 인덕션 전기레인지 IHR-105
#  - 화구: 1
#  - 리뷰 개수: 36

# In[84]:


import urllib.request
import requests
from bs4 import BeautifulSoup

list_href = []

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

from selenium import webdriver

user_list = []
review_list = []
date_list = []
rate_list = []
total_list = []

for i in range(1,5):
    if(i%10==0):
        print(i)
    url = "http://www.11st.co.kr/product/SellerProductDetail.tmall?method=getProductReviewList&prdNo=1504693113&page=" +str(i) +"&pageTypCd=first&reviewDispYn=Y&isPreview=false&reviewOptDispYn=Y&optSearchBtnAndGraphLayer=Y&reviewBottomBtn=Y&openDetailContents=Y&pageSize=10&isIgnoreAuth=false&lctgrNo=1001434&leafCtgrNo=0&groupProductNo=0&groupFirstViewPrdNo=0&selNo=41963331#this"
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    page_source = ""
    driver.get(url)

    page_source = driver.page_source

    driver.close()

    bsoup = BeautifulSoup(page_source, 'html.parser')
    
    _text = bsoup.find_all('strong', class_='name')
    user = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('span', class_='summ_conts')
    review = [i.get_text().replace('\n','').replace('\t','') for i in _text]
    
    _text = bsoup.find_all('span', class_='date')
    date = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('div', class_='selr_wrap')
    rate = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    for i, r in enumerate(rate):
        if '판매자 평점 별5개 중 5개' in r:
            rate[i] = 5
        elif '판매자 평점 별5개 중 4개' in r:
            rate[i] = 4
        elif '판매자 평점 별5개 중 3개' in r:
            rate[i] = 3
        elif '판매자 평점 별5개 중 2개' in r:
            rate[i] = 2
        else:
            rate[i] = 1
    
    total = []
    for j in range(len(user)):
        total.append([user[j], date[j], 'IHR-105', 1, review[j], rate[j+5], 0])
    
    total_list += total
    
import pandas as pd
import numpy as np

IHR = pd.DataFrame(total_list, columns = ['user', 'date', 'product_name', 'product_type', 'review', 'rate', 'source'])


# In[85]:


IHR.to_csv('11번가 IHR-105.csv', index = False, encoding = 'utf-8')


# -------------------------------------------------------------------------------------------------------------------------------
# ## ERA-F210M 2구 하이라이트 전기렌지
#  - 화구: 2
#  - 리뷰 개수: 97

# In[92]:


import urllib.request
import requests
from bs4 import BeautifulSoup

list_href = []

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

from selenium import webdriver

user_list = []
review_list = []
date_list = []
rate_list = []
total_list = []

for i in range(1,11):
    if(i%10==0):
        print(i)
    url = "http://www.11st.co.kr/product/SellerProductDetail.tmall?method=getProductReviewList&prdNo=1660981606&page=" +str(i)+"&pageTypCd=first&reviewDispYn=Y&isPreview=false&reviewOptDispYn=Y&optSearchBtnAndGraphLayer=Y&reviewBottomBtn=Y&openDetailContents=Y&pageSize=10&isIgnoreAuth=false&lctgrNo=1001434&leafCtgrNo=0&groupProductNo=0&groupFirstViewPrdNo=0&selNo=10789766#this"
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    page_source = ""
    driver.get(url)

    page_source = driver.page_source

    driver.close()

    bsoup = BeautifulSoup(page_source, 'html.parser')
    
    _text = bsoup.find_all('strong', class_='name')
    user = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('span', class_='summ_conts')
    review = [i.get_text().replace('\n','').replace('\t','') for i in _text]
    
    _text = bsoup.find_all('span', class_='date')
    date = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('div', class_='selr_wrap')
    rate = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    for i, r in enumerate(rate):
        if '판매자 평점 별5개 중 5개' in r:
            rate[i] = 5
        elif '판매자 평점 별5개 중 4개' in r:
            rate[i] = 4
        elif '판매자 평점 별5개 중 3개' in r:
            rate[i] = 3
        elif '판매자 평점 별5개 중 2개' in r:
            rate[i] = 2
        else:
            rate[i] = 1
    
    total = []
    for j in range(len(user)):
        total.append([user[j], date[j], 'ERA-F210M', 2, review[j], rate[j+5], 0])
    
    total_list += total
    
import pandas as pd
import numpy as np

ERA = pd.DataFrame(total_list, columns = ['user', 'date', 'product_name', 'product_type', 'review', 'rate', 'source'])


# In[93]:


ERA.to_csv('11번가 ERA-F210M(1).csv', index = False, encoding = 'utf-8')


# In[95]:


data = pd.read_csv('11번가 ERA-F210M(1).csv', encoding = 'utf-8')
data.tail()


# --------------------------------------------------------------------------------------------------------------------------------
# ## ERA-F210M 2구 전기렌지
#  - 화구: 2
#  - 리뷰 개수: 107

# In[96]:


import urllib.request
import requests
from bs4 import BeautifulSoup

list_href = []

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

from selenium import webdriver

user_list = []
review_list = []
date_list = []
rate_list = []
total_list = []

for i in range(1,12):
    if(i%10==0):
        print(i)
    url = "http://www.11st.co.kr/product/SellerProductDetail.tmall?method=getProductReviewList&prdNo=1685089483&page="+str(i)+"&pageTypCd=first&reviewDispYn=Y&isPreview=false&reviewOptDispYn=Y&optSearchBtnAndGraphLayer=Y&reviewBottomBtn=Y&openDetailContents=Y&pageSize=10&isIgnoreAuth=false&lctgrNo=1001434&leafCtgrNo=0&groupProductNo=0&groupFirstViewPrdNo=0&selNo=10789766#this"
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    page_source = ""
    driver.get(url)

    page_source = driver.page_source

    driver.close()

    bsoup = BeautifulSoup(page_source, 'html.parser')
    
    _text = bsoup.find_all('strong', class_='name')
    user = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('span', class_='summ_conts')
    review = [i.get_text().replace('\n','').replace('\t','') for i in _text]
    
    _text = bsoup.find_all('span', class_='date')
    date = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('div', class_='selr_wrap')
    rate = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    for i, r in enumerate(rate):
        if '판매자 평점 별5개 중 5개' in r:
            rate[i] = 5
        elif '판매자 평점 별5개 중 4개' in r:
            rate[i] = 4
        elif '판매자 평점 별5개 중 3개' in r:
            rate[i] = 3
        elif '판매자 평점 별5개 중 2개' in r:
            rate[i] = 2
        else:
            rate[i] = 1
    
    total = []
    for j in range(len(user)):
        total.append([user[j], date[j], 'ERA-F210M', 2, review[j], rate[j+5], 0])
    
    total_list += total
    
import pandas as pd
import numpy as np

ERA = pd.DataFrame(total_list, columns = ['user', 'date', 'product_name', 'product_type', 'review', 'rate', 'source'])


# In[97]:


ERA.to_csv('11번가 ERA-F210M(2).csv', index = False, encoding = 'utf-8')


# In[129]:


data = pd.read_csv('11번가 ERA-F210M(2).csv', encoding = 'utf-8')
data.tail()


# ---------------------------------------
# ## 이지쿡 2구 하이라이트 전기렌지 ERA-F211M
#  - 화구: 2
#  - 리뷰 개수: 72

# In[103]:


import urllib.request
import requests
from bs4 import BeautifulSoup

list_href = []

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

from selenium import webdriver

user_list = []
review_list = []
date_list = []
rate_list = []
total_list = []

for i in range(1,9):
    if(i%10==0):
        print(i)
    url = "http://www.11st.co.kr/product/SellerProductDetail.tmall?method=getProductReviewList&prdNo=1687155661&page="+str(i)+"&pageTypCd=first&reviewDispYn=Y&isPreview=false&reviewOptDispYn=Y&optSearchBtnAndGraphLayer=Y&reviewBottomBtn=Y&openDetailContents=Y&pageSize=10&isIgnoreAuth=false&lctgrNo=1001434&leafCtgrNo=1009311&groupProductNo=15179&groupFirstViewPrdNo=1687155661&selNo=42673992#this"
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    page_source = ""
    driver.get(url)

    page_source = driver.page_source

    driver.close()

    bsoup = BeautifulSoup(page_source, 'html.parser')
    
    _text = bsoup.find_all('strong', class_='name')
    user = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('span', class_='summ_conts')
    review = [i.get_text().replace('\n','').replace('\t','') for i in _text]
    
    _text = bsoup.find_all('span', class_='date')
    date = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('div', class_='selr_wrap')
    rate = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    for i, r in enumerate(rate):
        if '판매자 평점 별5개 중 5개' in r:
            rate[i] = 5
        elif '판매자 평점 별5개 중 4개' in r:
            rate[i] = 4
        elif '판매자 평점 별5개 중 3개' in r:
            rate[i] = 3
        elif '판매자 평점 별5개 중 2개' in r:
            rate[i] = 2
        else:
            rate[i] = 1
    
    total = []
    for j in range(len(user)):
        total.append([user[j], date[j], 'ERA-F211M', 2, review[j], rate[j+5], 0])
    
    total_list += total
    
import pandas as pd
import numpy as np

ERA = pd.DataFrame(total_list, columns = ['user', 'date', 'product_name', 'product_type', 'review', 'rate', 'source'])


# In[104]:


ERA.to_csv('11번가 ERA-F211M.csv', index = False, encoding = 'utf-8')


# In[128]:


data = pd.read_csv('11번가 ERA-F211M.csv', encoding = 'utf-8')
data.tail()


# ----------------
# ## 이지쿡 2구 하이라이트 전기렌지 ERA-F212M
#  - 화구: 2
#  - 리뷰 개수: 105

# In[109]:


import urllib.request
import requests
from bs4 import BeautifulSoup

list_href = []

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

from selenium import webdriver

user_list = []
review_list = []
date_list = []
rate_list = []
total_list = []

for i in range(1,12):
    if(i%10==0):
        print(i)
    url = "http://www.11st.co.kr/product/SellerProductDetail.tmall?method=getProductReviewList&prdNo=1687156145&page="+str(i)+"&pageTypCd=first&reviewDispYn=Y&isPreview=false&reviewOptDispYn=Y&optSearchBtnAndGraphLayer=Y&reviewBottomBtn=Y&openDetailContents=Y&pageSize=10&isIgnoreAuth=false&lctgrNo=1001434&leafCtgrNo=1009311&groupProductNo=15179&groupFirstViewPrdNo=1687156145&selNo=42673992#this"
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    page_source = ""
    driver.get(url)

    page_source = driver.page_source

    driver.close()

    bsoup = BeautifulSoup(page_source, 'html.parser')
    
    _text = bsoup.find_all('strong', class_='name')
    user = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('span', class_='summ_conts')
    review = [i.get_text().replace('\n','').replace('\t','') for i in _text]
    
    _text = bsoup.find_all('span', class_='date')
    date = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('div', class_='selr_wrap')
    rate = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    for i, r in enumerate(rate):
        if '판매자 평점 별5개 중 5개' in r:
            rate[i] = 5
        elif '판매자 평점 별5개 중 4개' in r:
            rate[i] = 4
        elif '판매자 평점 별5개 중 3개' in r:
            rate[i] = 3
        elif '판매자 평점 별5개 중 2개' in r:
            rate[i] = 2
        else:
            rate[i] = 1
    
    total = []
    for j in range(len(user)):
        total.append([user[j], date[j], 'ERA-F212M', 2, review[j], rate[j+5], 0])
    
    total_list += total
    
import pandas as pd
import numpy as np

ERA = pd.DataFrame(total_list, columns = ['user', 'date', 'product_name', 'product_type', 'review', 'rate', 'source'])


# In[110]:


ERA.to_csv('11번가 ERA-F212M.csv', index = False, encoding = 'utf-8')


# In[127]:


data = pd.read_csv('11번가 ERA-F212M.csv', encoding = 'utf-8')
data.tail()


# -------------------------
# ## 3구 하이라이트 전기레인지 ERA-B382E
#  - 화구: 3
#  - 리뷰 개수: 44

# In[140]:


import urllib.request
import requests
from bs4 import BeautifulSoup

list_href = []

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

from selenium import webdriver

total_list = []

for i in range(1,6):
    if(i%10==0):
        print(i)
    url = "http://www.11st.co.kr/product/SellerProductDetail.tmall?method=getProductReviewList&prdNo=1545481669&page="+str(i)+"&pageTypCd=first&reviewDispYn=Y&isPreview=false&reviewOptDispYn=Y&optSearchBtnAndGraphLayer=Y&reviewBottomBtn=Y&openDetailContents=Y&pageSize=10&isIgnoreAuth=false&lctgrNo=1001434&leafCtgrNo=0&groupProductNo=0&groupFirstViewPrdNo=0&selNo=41963331#this"
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    page_source = ""
    driver.get(url)

    page_source = driver.page_source

    driver.close()

    bsoup = BeautifulSoup(page_source, 'html.parser')
    
    _text = bsoup.find_all('strong', class_='name')
    user = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('span', class_='summ_conts')
    review = [i.get_text().replace('\n','').replace('\t','') for i in _text]
    
    _text = bsoup.find_all('span', class_='date')
    date = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('div', class_='selr_wrap')
    rate = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    for i, r in enumerate(rate):
        if '판매자 평점 별5개 중 5개' in r:
            rate[i] = 5
        elif '판매자 평점 별5개 중 4개' in r:
            rate[i] = 4
        elif '판매자 평점 별5개 중 3개' in r:
            rate[i] = 3
        elif '판매자 평점 별5개 중 2개' in r:
            rate[i] = 2
        else:
            rate[i] = 1
    
    total = []
    for j in range(len(user)):
        total.append([user[j], date[j], 'ERA-B382E', 3, review[j], rate[j+5], 0])
    
    total_list += total
    
import pandas as pd
import numpy as np

ERA = pd.DataFrame(total_list, columns = ['user', 'date', 'product_name', 'product_type', 'review', 'rate', 'source'])


# In[141]:


ERA.to_csv('11번가 ERA-B382E.csv', index = False, encoding = 'utf-8')


# In[142]:


data = pd.read_csv('11번가 ERA-B382E.csv', encoding = 'utf-8')
data.tail()


# -------------------------------------------
# ## 3구 하이라이트 전기레인지 ERA-B382E
#  - 화구: 3
#  - 리뷰 개수: 18

# In[144]:


import urllib.request
import requests
from bs4 import BeautifulSoup

list_href = []

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

from selenium import webdriver

total_list = []

for i in range(1,3):
    if(i%10==0):
        print(i)
    url =  "http://www.11st.co.kr/product/SellerProductDetail.tmall?method=getProductReviewList&prdNo=1469788706&page="+str(i)+"&pageTypCd=first&reviewDispYn=Y&isPreview=false&reviewOptDispYn=Y&optSearchBtnAndGraphLayer=Y&reviewBottomBtn=Y&openDetailContents=Y&pageSize=10&isIgnoreAuth=false&lctgrNo=1001434&leafCtgrNo=0&groupProductNo=0&groupFirstViewPrdNo=0&selNo=41963331#this"
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    page_source = ""
    driver.get(url)

    page_source = driver.page_source

    driver.close()

    bsoup = BeautifulSoup(page_source, 'html.parser')
    
    _text = bsoup.find_all('strong', class_='name')
    user = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('span', class_='summ_conts')
    review = [i.get_text().replace('\n','').replace('\t','') for i in _text]
    
    _text = bsoup.find_all('span', class_='date')
    date = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('div', class_='selr_wrap')
    rate = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    for i, r in enumerate(rate):
        if '판매자 평점 별5개 중 5개' in r:
            rate[i] = 5
        elif '판매자 평점 별5개 중 4개' in r:
            rate[i] = 4
        elif '판매자 평점 별5개 중 3개' in r:
            rate[i] = 3
        elif '판매자 평점 별5개 중 2개' in r:
            rate[i] = 2
        else:
            rate[i] = 1
    
    total = []
    for j in range(len(user)):
        total.append([user[j], date[j], 'ERA-B382E', 3, review[j], rate[j+5], 0])
    
    total_list += total
    
import pandas as pd
import numpy as np

ERA = pd.DataFrame(total_list, columns = ['user', 'date', 'product_name', 'product_type', 'review', 'rate', 'source'])


# In[145]:


ERA.to_csv('11번가 ERA-B382E(2).csv', index = False, encoding = 'utf-8')


# In[147]:


data = pd.read_csv('11번가 ERA-B382E(2).csv', encoding = 'utf-8')
data.tail()


# ------------------------
# ## 하이브리드 빌트인 전기렌지 ERA-BTS33
#  - 화구: 하이브리드
#  - 리뷰 개수: 44

# In[149]:


import urllib.request
import requests
from bs4 import BeautifulSoup

list_href = []

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

from selenium import webdriver

total_list = []

for i in range(1,6):
    if(i%10==0):
        print(i)
    url = "http://www.11st.co.kr/product/SellerProductDetail.tmall?method=getProductReviewList&prdNo=2469202795&page="+str(i)+"&pageTypCd=first&reviewDispYn=Y&isPreview=false&reviewOptDispYn=Y&optSearchBtnAndGraphLayer=Y&reviewBottomBtn=Y&openDetailContents=Y&pageSize=10&isIgnoreAuth=false&lctgrNo=1001434&leafCtgrNo=0&groupProductNo=0&groupFirstViewPrdNo=0&selNo=40143636#this"
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    page_source = ""
    driver.get(url)

    page_source = driver.page_source

    driver.close()

    bsoup = BeautifulSoup(page_source, 'html.parser')
    
    _text = bsoup.find_all('strong', class_='name')
    user = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('span', class_='summ_conts')
    review = [i.get_text().replace('\n','').replace('\t','') for i in _text]
    
    _text = bsoup.find_all('span', class_='date')
    date = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('div', class_='selr_wrap')
    rate = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    for i, r in enumerate(rate):
        if '판매자 평점 별5개 중 5개' in r:
            rate[i] = 5
        elif '판매자 평점 별5개 중 4개' in r:
            rate[i] = 4
        elif '판매자 평점 별5개 중 3개' in r:
            rate[i] = 3
        elif '판매자 평점 별5개 중 2개' in r:
            rate[i] = 2
        else:
            rate[i] = 1
    
    total = []
    for j in range(len(user)):
        total.append([user[j], date[j], 'ERA-BTS33', 0, review[j], rate[j+5], 0])
    
    total_list += total
    
import pandas as pd
import numpy as np

ERA = pd.DataFrame(total_list, columns = ['user', 'date', 'product_name', 'product_type', 'review', 'rate', 'source'])


# In[150]:


ERA.to_csv('11번가 ERA-BTS33.csv', index = False, encoding = 'utf-8')


# In[154]:


data = pd.read_csv('11번가 ERA-BTS33.csv', encoding = 'utf-8')
data.tail()


# -------------------
# ## 하이브리드 3구 전기레인지 ERA-BTS33
#  - 화구: 하이브리드
#  - 리뷰 개수: 16

# In[158]:


import urllib.request
import requests
from bs4 import BeautifulSoup

list_href = []

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

from selenium import webdriver

total_list = []

for i in range(1,3):
    if(i%10==0):
        print(i)
    url = "http://www.11st.co.kr/product/SellerProductDetail.tmall?method=getProductReviewList&prdNo=2469037471&page="+str(i)+"&pageTypCd=first&reviewDispYn=Y&isPreview=false&reviewOptDispYn=Y&optSearchBtnAndGraphLayer=Y&reviewBottomBtn=Y&openDetailContents=Y&pageSize=10&isIgnoreAuth=false&lctgrNo=1001434&leafCtgrNo=0&groupProductNo=0&groupFirstViewPrdNo=0&selNo=40425843#this"
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    page_source = ""
    driver.get(url)

    page_source = driver.page_source

    driver.close()

    bsoup = BeautifulSoup(page_source, 'html.parser')
    
    _text = bsoup.find_all('strong', class_='name')
    user = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('span', class_='summ_conts')
    review = [i.get_text().replace('\n','').replace('\t','') for i in _text]
    
    _text = bsoup.find_all('span', class_='date')
    date = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    
    _text = bsoup.find_all('div', class_='selr_wrap')
    rate = [i.get_text().replace('\n', '').replace('\t', '') for i in _text]
    for i, r in enumerate(rate):
        if '판매자 평점 별5개 중 5개' in r:
            rate[i] = 5
        elif '판매자 평점 별5개 중 4개' in r:
            rate[i] = 4
        elif '판매자 평점 별5개 중 3개' in r:
            rate[i] = 3
        elif '판매자 평점 별5개 중 2개' in r:
            rate[i] = 2
        else:
            rate[i] = 1
    
    total = []
    for j in range(len(user)):
        total.append([user[j], date[j], 'ERA-BTS33', 0, review[j], rate[j+5], 0])
    
    total_list += total
    
import pandas as pd
import numpy as np

ERA = pd.DataFrame(total_list, columns = ['user', 'date', 'product_name', 'product_type', 'review', 'rate', 'source'])


# In[159]:


ERA.to_csv('11번가 ERA-BTS33(2).csv', index = False, encoding = 'utf-8')


# In[161]:


data = pd.read_csv('11번가 ERA-BTS33(2).csv', encoding = 'utf-8')
data.tail()


# -----------------------------------------------

# In[2]:


import pandas as pd
data1 = pd.read_csv('11번가 IHR-102.csv', encoding = 'utf-8')
data2 = pd.read_csv('11번가 IHR-105.csv', encoding = 'utf-8')
data3 = pd.read_csv('11번가 ERA-F210M(1).csv', encoding = 'utf-8')
data4 = pd.read_csv('11번가 ERA-F210M(2).csv', encoding = 'utf-8')
data5 = pd.read_csv('11번가 ERA-F211M.csv', encoding = 'utf-8')
data6 = pd.read_csv('11번가 ERA-F212M.csv', encoding = 'utf-8')
data7 = pd.read_csv('11번가 ERA-B382E.csv', encoding = 'utf-8')
data8 = pd.read_csv('11번가 ERA-B382E(2).csv', encoding = 'utf-8')
data9 = pd.read_csv('11번가 ERA-BTS33.csv', encoding = 'utf-8')
data10 = pd.read_csv('11번가 ERA-BTS33(2).csv', encoding = 'utf-8')

total_data = pd.concat([data1, data2, data3, data4, data5, data6, data7, data8, data9, data10], axis = 0)
total_data.tail()


# In[5]:


total_data.to_csv('11번가 전기레인지 리뷰.csv', encoding = 'utf-8', index = False)


# In[6]:


data = pd.read_csv('11번가 전기레인지 리뷰.csv', encoding = 'utf-8')
data.head()

