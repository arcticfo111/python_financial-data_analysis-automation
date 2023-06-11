import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import pandas as pd

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 다우존스지수와 코스피지수 로드
dow = fdr.DataReader('DJI', '2010-06-01')
# print(f'다우존스 {dow.head()} {dow.tail()} {dow.describe()}')
kospi = fdr.DataReader('KS11', '2010-06-01')
# print(f'코스피 {kospi.head()} {kospi.tail()} {kospi.describe()}')

# # 다우조스 지수와 코스피 지수 시각화
plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
plt.plot(dow.index, dow.Close, 'r--', label='Dow Jones Industrial')
plt.title('dowjones')
plt.legend(loc='best')
plt.subplot(1, 2, 2)
plt.plot(kospi.index, kospi.Close, 'b', label='KOSPI')
plt.title('kospi')
plt.legend(loc='best')

plt.figure(figsize=(7, 7))
plt.plot(dow.index, dow.Close, 'r--', label='Dow Jones Industrial')
plt.plot(kospi.index, kospi.Close, 'b', label='KOSPI')
plt.title('dowjones and kospi')
plt.grid(True)
plt.legend(loc='best')

# # 다우존스 지수와 코스피 지수 변동률 시각화
d = (dow.Close / dow.Close.loc['2010-06-01']) * 100
k = (kospi.Close / kospi.Close.loc['2010-06-01']) * 100
plt.figure(figsize=(7, 7))
plt.plot(d.index, d, 'r--', label='Dow Jones Industrial')
plt.plot(k.index, k, 'b', label='KOSPI')
plt.title('fluctuation_dowjones and kospi')
plt.grid(True)
plt.legend(loc='best')

# 다우존스와 코스피 지수 산점도로 시각화하기
# print(len(dow), len(kospi)) # 산점도를 그리려면 종속변수와 독립변수 크기(개수)가 같아야 한다. -> 각각 인덱스 기준으로 두 개의 시리즈를 하나의 데이터 프레임으로 만들기
dow_and_kospi_close_df = pd.DataFrame({'DOW' : dow['Close'], 'KOSPI' : kospi['Close']}) 
# print(dow_close_df.isnull().sum(), kospi_close_df.isnull().sum())#결측 값 확인
dow_and_kospi_close_df = dow_and_kospi_close_df.fillna(method='bfill')
dow_close_df = dow_and_kospi_close_df['DOW']
kospi_close_df = dow_and_kospi_close_df['KOSPI']
plt.figure(figsize=(8, 10))
plt.scatter(dow_close_df, kospi_close_df)
plt.title('Dow Jonse Industrial Average - KOSPI Chart')
plt.xlabel('Dow Jonse Industrial Average')
plt.ylabel('KOSPI')

# 다우존스와 코스피 지수 regression 선형회귀_scipy 패키지 사용
'''
<선형회귀 regression 요약>
y=wx+b
- 독립변수는 x, 종속변수는 y, 머신러닝에서 기울기는 w, y절편은 b
- 독립변수는 종속변수의 값에 영향을 주고 변하게 한다.
- 독립변수는 독립적으로 변할 수 있지만, 종속변수는 독립변수에 의해 종속적으로 결정된다.
- 주어진 데이터로부터 데이터를 가장 잘 표현하는 직선을 찾는 다는 것은 적절한 w, b 값을 찾는 다는 것이다. 
    -> 데이터를 반영한 적절한 직선을 찾고나면 그 후 임의의 값에 대해서도 예측할 수 있다. 
    -> 1시간 공부 → 21점, 2시간 공부 → 41점, 3시간 공부 → 61점 이라면 w는 20, b는 1
<상관계수 coefficient of correlation 요약>
- 독립변수와 종속변수 사이의 상관관계 정도를 나타내는 수치이다.
- 상관계수 r은 항상 -1 ≤ r ≤ 1을 만족시킨다. 양의 상관관계가 가장 강하면 1, 음의 상관관계가 가장 강하면 -1 이다.
- A 자산과 B 자산의 상관계수가 1이면 A자산 가치가 x% 상승시 B자신도 x만큼 상승한다. 만약 상관계수가 -1이면 A자산 가치가 x% 상승시 B자신도 x만큼 하락한다.(반비례)
- 만약 상관계수가 0이면 두 자산은 연관성 X
'''
# Y는 코스피 지수, X는 다우존스 지수
dow_and_kospi_r_value = dow_close_df.corr(kospi_close_df) # 다우지수와 코스피 지수의 상관계수 시리즈의 corr()함수로  구하기
dow_and_kospi_r_squared = dow_and_kospi_r_value ** 2 # 결정계수 구하기
dow_and_kospi_linregress = stats.linregress(dow_close_df, kospi_close_df) # 선형회귀 모델
dow_and_kospi_regr_line = f'Y = {dow_and_kospi_linregress.slope:.2f} * X + {dow_and_kospi_linregress.intercept:.2f}' # 선형회귀직선 구하기
plt.figure(figsize=(7,7))
plt.plot(dow_close_df, kospi_close_df, '.')
plt.plot(dow_close_df, dow_and_kospi_linregress.slope * dow_close_df + dow_and_kospi_linregress.intercept, 'r')
plt.legend(['DOW x KOSPI', dow_and_kospi_regr_line])
plt.title(f'DOW x KOSPI (R = {dow_and_kospi_linregress.rvalue:.2f})')
plt.xlabel('Dow Jones Industrial Average')
plt.ylabel('KOSPI')
plt.show()
