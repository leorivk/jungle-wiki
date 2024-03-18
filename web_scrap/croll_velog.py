import random
import requests

from bs4 import BeautifulSoup
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost',27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbjungle                      # 'dbjungle'라는 이름의 db를 만듭니다.


def insert_all():
    # URL을 읽어서 HTML를 받아오고,
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    data = requests.get('https://velog.io/search?q=%EB%B2%88%EC%97%AD&username=typo', headers=headers)

    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    soup = BeautifulSoup(data.text, 'html.parser')

    # select를 이용해서, li들을 불러오기pip
    velog = soup.select('#root > div:nth-child(2) > div:nth-child(3) > div:nth-child(3) > div')
    # print(len(velog))

    # articles (li들) 의 반복문을 돌리기
    for article in velog:
        # article 안에 a 가 있으면,
        # (조건을 만족하는 첫 번째 요소, 없으면 None을 반환한다.)
        tag_element = article.select_one('h2')
        if not tag_element:
            continue
        title = tag_element.text  # a 태그 사이의 텍스트를 가져오기
        # print(title)

        tag_element = article.select_one('p')
        if not tag_element:
            continue
        txt = tag_element.text  # a 태그 사이의 텍스트를 가져오기
        # print(txt)
        
        tag_element = article.select_one('#root > div:nth-child(2) > div:nth-child(3) > div:nth-child(3) > div > div > a')
        if not tag_element:
            continue
        category = tag_element.text  # a 태그 사이의 텍스트를 가져오기
        # print(category)
        
        tag_element = article.select_one('div.subinfo > span')
        if not tag_element:
            continue
        date = tag_element.text  # a 태그 사이의 텍스트를 가져오기
        # print(date)
       
        
        tag_element = article.select_one('img')['src']
        if not tag_element:
            continue
        
        poster_url = tag_element
        # print(poster_url)

        tag_element = article.select_one('a')
        if not tag_element:
            continue
        info_url_a = tag_element['href']
        info_url = 'https://velog.io' + info_url_a
        print(info_url)


        doc = {
            'title': title,
            'txt': txt,
            'category': category,
            'date' : date,
            'poster_url': poster_url,
            'info_url': info_url,
        }
        db.velog.insert_one(doc)
        print('완료: ', title, txt, category, date, poster_url, info_url)


if __name__ == '__main__':
    # 기존의 articles 콜렉션을 삭제하기
    db.velog.drop()

    # 영화 사이트를 scraping 해서 db 에 채우기
    insert_all()