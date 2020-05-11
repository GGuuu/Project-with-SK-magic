#!/usr/bin/env python
# coding: utf-8

# In[4]:


#리뷰 데이터 크롤링
# 1) user: 리뷰 작성자 아이디
# 2) date: 리뷰 작성 날짜
# 3) product_name: 제품명 (IHR-102, IHR-105, ERA-F210M, ERA-F211M, ERA-F212M, ERA-B382E, ERA-BTS33 중 택1)
# 4) product_type: 제품 종류, 0-3 중 택1 (0: 하이브리드, 1: 1구, 2: 2구, 3: 3구)
# 5) review: 상품평
# 6) rate: 평점
# 7) source: 소스 이름, 0-7 중 택1 (0: 11번가, 1: g마켓, 2: 옥션, 3: 네이버쇼핑, 4: 쿠팡, 5: 하이마트, 6:신세계몰, 7: CJmall)
# - 변수 자료형: string (user, date, product_name, review) & numeric (product_type, rate, source)


from __future__ import annotations

import re
from enum import Enum
from typing import Generator, List

import requests
from bs4 import BeautifulSoup, Tag

import pandas as pd


class CoupangReviewSort(Enum):
    최신순 = 'DATE_DESC'
    베스트순 = 'ORDER_SCORE_ASC'


class CoupangReviewSurvey:
    question: str
    answer: str

    @staticmethod
    def from_soup_dom(survey_dom: Tag) -> CoupangReviewSurvey:
        item = CoupangReviewSurvey()

        question_dom: Tag = survey_dom.find_all(class_='sdp-review__article__list__survey__row__question')[0]
        item.question = question_dom.get_text().strip()

        answer_dom: Tag = survey_dom.find_all(class_='sdp-review__article__list__survey__row__answer')[0]
        item.answer = answer_dom.get_text().strip()

        return item


class CoupangReview:
    author_id: int
    author_name: str
    rating: int
    attachment_urls: List[str]
    reg_date: str
    product_name: str
    headline: str
    content: str
    surveys: List[CoupangReviewSurvey]
    helpful_count: int
    id: int
    

    @staticmethod
    def from_soup_dom(article_dom: Tag) -> CoupangReview:
        item = CoupangReview()

        user_info_dom: Tag = article_dom.find_all(class_='sdp-review__article__list__info__user__name')[0]
        item.author_id = int(user_info_dom['data-member-id'])
        item.author_name = user_info_dom.get_text().strip()

        rating_dom: Tag = article_dom.find_all(class_='sdp-review__article__list__info__product-info__star-orange')[0]
        item.rating = int(rating_dom['data-rating'])

        attachment_image_doms = article_dom.find_all(class_='sdp-review__article__list__attachment__img')
        attachments = []
        for attachment_dom in attachment_image_doms:
            attachments.append(attachment_dom['src'])

        reg_date_dom: Tag = article_dom.find_all(class_='sdp-review__article__list__info__product-info__reg-date')[0]
        item.reg_date = reg_date_dom.get_text().strip()

        product_dom: Tag = article_dom.find_all(class_='sdp-review__article__list__info__product-info__name')[0]
        item.product_name = product_dom.get_text().strip()
        

        try:
            headline_dom: Tag = article_dom.find_all(class_='sdp-review__article__list__headline')[0]
            item.headline = headline_dom.get_text().strip()
        except IndexError:
            item.headline = ''

        try:
            content_dom: Tag = article_dom.find_all(class_='sdp-review__article__list__review__content')[0]
            item.content = content_dom.get_text().strip()
        except IndexError:
            item.content = ''

        survey_doms = article_dom.find_all(class_='sdp-review__article__list__survey__row')
        surveys = []
        for survey_dom in survey_doms:
            surveys.append(CoupangReviewSurvey.from_soup_dom(survey_dom))
        item.surveys = surveys

        helpful_dom = article_dom.find_all(class_='sdp-review__article__list__help')[0]
        item.helpful_count = int(helpful_dom['data-count'])
        item.id = int(helpful_dom['data-review-id'])

        return item


class CoupangReviewPage:
    product_id: int
    sort_by: CoupangReviewSort
    size: int
    index: int

    _raw_content: str

    def __init__(
            self,
            product_id: int,
            sort_by: CoupangReviewSort = CoupangReviewSort.최신순,
            index: int = 1,
            size: int = 10,
    ):
        self.product_id = product_id
        self.sort_by = sort_by
        self.index = index
        self.size = size

        self._download()

    def _download(self):
        response = requests.get(
            'https://www.coupang.com/vp/product/reviews',
            params={
                'productId': self.product_id,
                'page': self.index,
                'size': self.size,
                'sortBy': self.sort_by.value,
                'viRoleCode': 3,
            },
            headers={
                'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            }
        )
        self._raw_content = response.text

    @property
    def total_count(self):
        meta_pattern = re.compile(
            r'<div class="sdp-review__article__list__hidden-rating js_reviewArticleTotalCountHiddenValue" data-review-total-count="(\d*?)" data-total-count="(\d*?)"></div>'
        )
        _, data_total_count = meta_pattern.findall(self._raw_content)[0]
        return int(data_total_count)

    @property
    def has_next(self):
        retrieved_count = self.size * self.index
        left_count = self.total_count - retrieved_count
        return left_count > 0

    def items(self) -> Generator[CoupangReview, None, None]:
        soup = BeautifulSoup(self._raw_content, 'html.parser')
        article_doms = soup.find_all(class_='sdp-review__article__list')
        for article_dom in article_doms:
            yield CoupangReview.from_soup_dom(article_dom)

    def go_next(self):
        self.index += 1
        self._download()

        
if __name__ == '__main__':
    
    product_name_dic = {'IHR-102':[341393330, '1'], 'IHR-105':[3264177, '1'], 'ERA-F210M':[15375858, '2'], 'ERA-F211M':[15375860, '2'],
                'ERA-F212M':[15375863, '2'], 'ERA-B382E':[59661943, '3']}

    user_list = []
    date_list = []
    product_name_list = []
    product_type_list = []
    review_list = []
    rate_list = []
    source_list = []
    
    for key, val in product_name_dic.items():
        page = CoupangReviewPage(val[0])

        while True:
#             print(f">>> Page {page.index}")
#             print(f"Total: {page.total_count}")
#             print(f"HasNext: {page.has_next}")
            for review in page.items():
                user_list.append(review.id)
                date_list.append(review.reg_date)
                product_name_list.append(key)
                product_type_list.append(val[1])
                review_list.append(review.content)
                rate_list.append(review.rating)
                source_list.append('4')
                
#                 print(f"#{review.id}(by {review.author_name}) Score {review.rating} @{review.reg_date} and {review.content}")

            if not page.has_next:
                break

            page.go_next()
    
    data = {'user':user_list,'date':date_list,'product_name':product_name_list,'product_type':product_type_list,
            'review':review_list,'rate':rate_list,'source':source_list}
    coupang_df = pd.DataFrame(data)
    coupang_df.to_csv('coupang_df.csv', index = False, encoding = 'utf8')
    coupang_df.to_pickle('coupang_df.p')


# In[5]:


coupang_df


# In[ ]:




