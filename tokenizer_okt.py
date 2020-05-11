#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from konlpy.tag import Okt, Hannanum, Kkma, Komoran
import pickle


# In[2]:


okt = Okt()


# In[3]:


def keywords(pos, tags=['Noun', 'Verb', 'Adjective']):
    words = []
    for p in pos:
        if p[1] in tags:
            words.append(p[0])
    return words


# In[4]:


print(okt.morphs("배송도 빠르고, 좋아요!!!많이 파세요!!!"))
print(okt.nouns("배송도 빠르고, 좋아요!!!많이 파세요!!!"))
print(okt.phrases("배송도 빠르고, 좋아요!!!많이 파세요!!!"))
print(okt.pos("배송도 빠르고, 좋아욬ㅋㅋ!!!많이 파세요!!!"))
print(okt.pos("배송도 빠르고, 좋아욬ㅋㅋ!!!많이 파세요!!!", norm=True))
print(okt.pos("배송도 빠르고, 좋아욬ㅋㅋ!!!많이 파세요!!!", norm=True, stem=True))
print(keywords(pos=okt.pos("배송도 빠르고, 좋아욬ㅋㅋ!!!많이 파세요!!!", norm=True, stem=True)))


# In[6]:


# df = pd.read_csv("data/checked_review_data.csv")
df = pd.read_pickle("data/checked_stopwords_review_data.pkl")
token = []
for i in df.review.index:
    try:
#         print(i, df.review[i])
#         print("okt: ", okt.morphs(df.review[i]))
        token.append(keywords(pos=okt.pos(df.review[i], norm=True, stem=True)))
    except:
        token.append([])

#     okt.morphs(df.review[i])
#     print("hannanum: ", hannanum.morphs(df.review[i]))
#     print("kkma: ", kkma.morphs(df.review[i]))

#     print("okt: ", okt.nouns(df.review[i]))
#     print("hannanum: ", hannanum.nouns(df.review[i]))
#     print("kkma: ", kkma.nouns(df.review[i]))

#     print(komoran.morphs(df.review[i]))
#     df.review[i] = okt.morphs(df.review[i])
#     print(df.review[i])
# df.to_csv("data/okt_checked_review_data.csv", index=False)
print(token)
with open('data/okt_token.pkl', 'wb') as f:
    pickle.dump(token, f)


# In[43]:


df.review[0]

