# konlpy 한국어 형태소 분석기 패키기
from konlpy.tag import Okt
from konlpy.tag import Kkma
from newspaper import Article # newspaper3는 뉴스 데이터를 크롤링 하는 패키지이다.
import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

okt = Okt()
kkma = Kkma()
test_text = '텍스트 분석에서 크롤링 등으로 얻어낸 코퍼스 데이터가 필요에 맞게 전처리되지 않은 상태라면, 해당 데이터를 사용하고자하는 용도에 맞게 토큰화 하는 일을 하게 됩니다.'

"""
morphs : 형태소 추출 (단어 토큰화)
pos : 품사 태깅(Part-of-speech tagging)
nouns : 명사 추출
공통적으로 형태소 추출과 품사 태깅에서 기본적으로 조사를 분리
"""
## okt, kkma 분석기 별로 결과가 들다. 상황에 따라 선택해서 사용하기
# test_text_morphs_okt = okt.morphs(test_text)
# test_text_pos_okt = okt.pos(test_text)
# test_text_nouns_okt = okt.nouns(test_text)
# test_text_morphs_kkma = kkma.morphs(test_text)
# test_text_pos_kkma = kkma.pos(test_text)
# test_text_nouns_kkma = kkma.nouns(test_text)

# 뉴스 본문 추출하기
url = 'https://finance.naver.com/item/news_read.nhn?article_id=0004960169&office_id=018&code=005930&page=10&sm='

article = Article(url, language='ko') # language='ko'로 설정
article.download()
article.parse()
article_content = article.text

# 회사명과 종목코드 얻기_딕셔너리 타입으로 회사명과 종목코드 대응시키기
url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
dfstockcode = pd.read_html(url, header=0)[0]
"""
print(dfstockcode.info()) 
dtypes를 보면 int64 즉 해당열이 정수형 타입, object는 문자열 타입임을 뜻한다. 
non-null은 결측값을 의미한다. 데이터의 갯수

print(dfstockcode.isnull().sum())
각 열에 몇 개의 결측치가 있는지 볼 수 있다. 
"""
stock_to_code = dict(zip(dfstockcode.회사명, dfstockcode.종목코드))
# dfstockcode.회사명과 종목코드 각 행을 zip()매소드에 인자로 제공 -> 각 원소를 튜플타입으로 반환
print(stock_to_code)

