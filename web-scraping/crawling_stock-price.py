import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import mplfinance as mpf
from bs4 import BeautifulSoup as bs

# 셀트리온 주가 정보 가져오기, 1~3 페이지까지 
# 네이버 금융 사이트에서 셀트리온 검색해서 나온 주소
url_celltrion = 'https://finance.naver.com/item/sise_day.nhn?code=068270'
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
dataframe_celltrion = pd.DataFrame()
for page in range(1, 4):
    page_url = '{}&page={}'.format(url_celltrion, page)
    
    res = requests.get(url_celltrion, headers=headers) # 유저가 아니면 사이트가 접속을 차단할 수 있기 때문에 유저정보 같이 전달
    res_text = res.text # res.text로 해당 url의 html을 받아올 수 있다. 

    html = bs(res_text, 'html.parser')
    html_table = html.select('table')
    table = pd.read_html(str(html_table))   # html 문자열 전달 -> 테이블 추출하여 데이터프레임이 들어있는 배열 반환

    # 첫 번째 테이블만 필요하므로 첫 번째 테이블 변수에 할당, 결측값 삭제
    target_table = table[0].dropna()
    # 데이터 프레임 변수에 누적하기
    # dataframe_celltrion = dataframe_celltrion.append(target_table)
    dataframe_celltrion = pd.concat([dataframe_celltrion, target_table])

# 최근 데이터 15개만 사용하기. 인덱스 재설정, 날짜기준 오름차순 정렬
dataframe_celltrion = dataframe_celltrion.iloc[0:15]
dataframe_celltrion = dataframe_celltrion.sort_values(by='날짜')
dataframe_celltrion = dataframe_celltrion.reset_index(drop=True)

# 셀트리온 종가 시각화 하기
plt.figure(figsize=(15,5))
plt.title = 'Celltrion close price'
plt.xticks(rotation=45)
# co는 좌표를 청록색 원으로, -는 각 좌표를 실선으로 표현
plt.plot(dataframe_celltrion['날짜'], dataframe_celltrion['종가'], 'co-')
plt.grid(color='gray', linestyle='--')
# plt.show()

# 캔들차트로 시각화 하기
# candlestick_dataframe_celltrion()에서 요구하는 형식으로 변경
ohlc = dataframe_celltrion[['날짜','시가','고가','저가','종가']]
ohlc = ohlc.rename(columns = {'날짜' : 'Date', '시가' : 'Open', '고가' : 'High', '저가' : 'Low', '종가' : 'Close'})
ohlc = ohlc.sort_values(by = 'Date')
ohlc.index = pd.to_datetime(ohlc.Date)
ohlc = ohlc[['Open', 'High', 'Low', 'Close']]

keywords_arguments = dict(title = 'Celltrion candle chart', type='candle')
mc = mpf.make_marketcolors(up='r', down='b', inherit=True)
s  = mpf.make_mpf_style(marketcolors = mc)
mpf.plot(ohlc, **keywords_arguments, style=s)
