import pandas as pd

# 테마 종목을 알려주는 사이트에서 2차 전지 테마주 링크 페이지의 테이블 가져오기
theme_stock_tables = pd.read_html('http://m.infostock.co.kr/sector/sector_detail.asp?code=64&theme=2%uCC28%uC804%uC9C0&mode=w')
tables_len = len(theme_stock_tables)

# 두번째 테이블이 원하는 테이블이다. 
theme_stock_table = theme_stock_tables[1]
theme_stock_table = theme_stock_table[3:] # 상위 3개의 행(테마명, 테마개요, 테마 히스토리) 제거

# theme_stock_table.iloc[인덱스]로 특정 행 추출 -> 첫 번째 행을 데이터 프레임의 열 제목으로 쓰기
theme_stock_table.columns = theme_stock_table.iloc[0].to_list()
theme_stock_table = theme_stock_table[1:]

# 행 4개 삭제하여 인덱스가 4부터 시작하는 문제 수정
theme_stock_table = theme_stock_table.reset_index(drop=True)
print(theme_stock_table)