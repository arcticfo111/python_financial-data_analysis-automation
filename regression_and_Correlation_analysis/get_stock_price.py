import FinanceDataReader as fdr
import datetime
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 종목 리스트 가져오기
df_krx = fdr.StockListing('KRX')

# GS글로벌 종목의 가격 가져오기
GSglobal_price = fdr.DataReader('001250', '2018') # fdr.DataReader(str형으로종목단축코드여섯자리, str형으로년도4자리)

# APPLE 종목의 가격 가져오기
Apple_price = fdr.DataReader('AAPL', '2018')

# 비트코인 원화 가격 (빗썸)
btcoin_price = fdr.DataReader('BTC/KRW', '2018')

# 가장 최근 종가 출력
currentDateTime = datetime.datetime.now()
today_ymd = currentDateTime.date()
thismonth = today_ymd.strftime("%Y-%m")
today = today_ymd.strftime("%d")
ago7days = thismonth + '-' +str(int(today) -7)

def print_today_price (stock):
    stock_code = str(stock)
    df_price = fdr.DataReader(stock_code, ago7days)
    last_close_price = df_price['Close'].tail(1).values[0]
    last_close_price_day = df_price['Close'].tail(1).index.values[0]
    print(f'{stock} last close price: {last_close_price} {last_close_price_day}')

print_today_price('AAPL')