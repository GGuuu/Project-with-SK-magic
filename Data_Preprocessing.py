#!/usr/bin/env python
# coding: utf-8

# # 데이터 전처리

# data 통합

# In[ ]:


files = [f for f in os.listdir('./raw_data') if f.endswith('.csv')]
files


# In[ ]:


cp949_files = ['navershopping.csv', 'auction.csv', 'skmagicmall.csv']
no_rate_files = ['gmarket.csv']
data = pd.DataFrame()

for file in files:
    if file in cp949_files:
        _data = pd.read_csv('./raw_data/' + file, engine='python', encoding='cp949')
    else:
        _data = pd.read_csv('./raw_data/' + file, engine='python')
        if file in no_rate_files:
            _data['rate'] = '-'
            
    data = pd.concat([data, _data], axis=0, ignore_index=True)


# 결측치 제거 (리뷰 없는 것)

# In[ ]:


data = data.sort_values(['product_name'])
data = data.reset_index(drop=True)
# data = data.fillna('')
data = data.dropna()
data


# 반복 리뷰 삭제

# In[ ]:


counts = data.groupby('review').size()
remove_reviews = list(counts.index[counts > 10])
remove_reviews


# In[ ]:


mask = data['review'].isin(remove_reviews)
data = data[~mask]
data = data.reset_index(drop=True)
data


# 길이 10이하 리뷰 제거

# In[ ]:


mask = [len(i) > 10 for i in data['review']]
data = data[mask]
data = data.reset_index(drop=True)
data


# ID & 리뷰 중복 제거

# In[ ]:


data.drop_duplicates(["user", "review"], keep=False)
data


# In[ ]:


data.to_csv('./raw_data/review_data.csv', index=False)


# In[ ]:


with open('./raw_data/review_data.p', 'wb') as f:
    pickle.dump(data, f)


# In[ ]:




