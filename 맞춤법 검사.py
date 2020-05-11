#!/usr/bin/env python
# coding: utf-8

from hanspell import spell_checker
result = spell_checker.check(u'안녕 하세요')
print(result.checked)


# import pandas as pd
#
# data = pd.read_csv('review_data.csv', encoding = 'utf-8')
# for i in range(len(data)):
#     try:
#         review = data['review'][i]
#         if len(review) <= 500:
#             checked = spell_checker.check(review)
#             data['review'][i] = checked.checked
#         else:
#             iteration = len(review)//500 + 1
#             checked = ''
#             for i in range(iteration):
#                 _checked = spell_checker.check(review[i*500:(i+1)*500])
#                 checked += _checked.checked
#             data['review'][i] = checked
#     except:
#         print(i)
#
#
# # In[ ]:
#
#
# data.to_csv('checked_review_data.csv', index=False, encoding='utf-8')
#
#
# # In[ ]:
#
#
# import pickle
#
# data.to_pickle('checked_review_data.p')

