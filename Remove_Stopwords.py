#!/usr/bin/env python
# coding: utf-8

# # 불용어 제거

with open('./preprocessd_data/checked_review_data.p', 'rb') as a:
    data = pickle.load(a)

stopwords = pd.read_csv('./korean_stopwords.csv', engine='python', encoding='cp949')
stopwords = list(stopwords['stopwords'])

stopwords = [i.split(' ') for i in stopwords]
stopwords = [j for i in stopwords for j in i]

custom_stopwords = ['합니다', '있어서', '있는', '거', '듯', '더']
stopwords += custom_stopwords

for i in range(len(data)):
    review = data['review'][i]
    review = review.split(' ')
    new_token = [i for i in review if i not in stopwords]
    
    data['review'][i] = ' '.join(new_token)

with open('./preprocessd_data/checked_stopwords_review_data.pkl', 'wb') as f:
    pickle.dump(data, f)

