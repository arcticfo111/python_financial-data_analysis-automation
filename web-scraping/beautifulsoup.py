from bs4 import BeautifulSoup

with open('index.html', 'r') as htmlfile:
    html = htmlfile.read()
print(type(html))
# BeautifulSoup 인스턴스 생성. 두번째 매개변수는 분석할 분석기(parser)의 종류.
soup = BeautifulSoup(html, 'html.parser')
# print(soup.select('body'))
print(soup.select('h1 .name .menu'))


