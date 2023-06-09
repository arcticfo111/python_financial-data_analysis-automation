import pandas as pd
import numpy as np
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
okt = Okt()

naver_shopping_review_url = 'https://raw.githubusercontent.com/bab2min/corpus/master/sentiment/naver_shopping.txt'
naver_shopping_review_df = pd.read_table(naver_shopping_review_url, names=['ratings', 'reviews'])

# 20만개 정도 샘플 중 100개만 추출해서 진행
naver_shopping_review_df = naver_shopping_review_df.loc[1:100]

# 중복값 제거
naver_shopping_review_df.drop_duplicates(subset=['reviews'], inplace=True)

# 데이터프레임에 tokenized 열 추가, 형태소 분석기_명사만 추출해서 할당
naver_shopping_review_df['tokenized'] = naver_shopping_review_df['reviews'].apply(okt.nouns)

# 워드 클라우드_1~5점의 ratings 열의 데이터로 긍정/부정 리뷰를 분리하기(3점 초과시 1, 아니라면 0), 근정/부정 리뷰별로 많이 쓰인 단어 그래프 시각화
naver_shopping_review_df['likeorhate'] = np.select([naver_shopping_review_df.ratings > 3], [1], default=0)
positive_reviews = np.hstack(naver_shopping_review_df[naver_shopping_review_df['likeorhate'] == 1]['tokenized'].values)
negative_reviews = np.hstack(naver_shopping_review_df[naver_shopping_review_df['likeorhate'] == 0]['tokenized'].values)
positive_reviews_word_count = Counter(positive_reviews)
negative_reviews_word_count = Counter(negative_reviews)

# 긍정 리뷰 분리하여 시각화하기
"""
likeorhate열의 행 값이 1인 데이터 프레임의 tokenized열(행 값은 리스트)을
인덱스 리셋하고 -> np.concatenate()로 합치기 -> 공백 한칸을 사이에 두고 하나의 문자열로 합치기
"""
temp_data = ' '.join(np.concatenate(naver_shopping_review_df[naver_shopping_review_df['likeorhate']==1].tokenized.reset_index(drop=True)))
wordcloud = WordCloud(max_words = 2000 , width = 1600 , height = 800, font_path = '/Library/Fonts/THE_HongChawangjanemo.ttf').generate(temp_data)
plt.figure(figsize = (15, 15))
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.show()
