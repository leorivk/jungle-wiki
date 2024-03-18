import random
import requests

from bs4 import BeautifulSoup
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost',27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbjungle                      # 'dbjungle'라는 이름의 db를 만듭니다.


def insert_all():
    # URL을 읽어서 HTML를 받아오고,
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://krafton-jungle-essay.tistory.com/search/pint', headers=headers)

    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    soup = BeautifulSoup(data.text, 'html.parser')

    # select를 이용해서, li들을 불러오기pip
    tistory = soup.select('div.list_content')
    # print(len(articles))

    # articles (li들) 의 반복문을 돌리기
    for article in tistory:
        # article 안에 a 가 있으면,
        # (조건을 만족하는 첫 번째 요소, 없으면 None을 반환한다.)
        tag_element = article.select_one('strong.tit_post')
        if not tag_element:
            continue
        title = tag_element.text  # a 태그 사이의 텍스트를 가져오기
        print(title)

        tag_element = article.select_one('p.txt_post')
        if not tag_element:
            continue
        txt = tag_element.text  # a 태그 사이의 텍스트를 가져오기
        # print(txt)
        
        tag_element = article.select_one('div.detail_info > a')
        if not tag_element:
            continue
        category = tag_element.text  # a 태그 사이의 텍스트를 가져오기
        print(category)
        
        tag_element = article.select_one('span.txt_date')
        if not tag_element:
            continue
        date = tag_element.text  # a 태그 사이의 텍스트를 가져오기
        print(date)
       
        
        tag_element = article.select_one('div.list_content > a > img')['src']
        if not tag_element:
            continue
        
        poster_url_a = tag_element
        poster_url = 'https:' + poster_url_a 
        
        print(poster_url)

        tag_element = article.select_one('div.list_content > a.thumbnail_post')
        if not tag_element:
            continue
        info_url_a = tag_element['href']
        info_url = 'https://krafton-jungle-essay.tistory.com/' + info_url_a
        print(info_url)


        doc = {
            'title': title,
            'txt': txt,
            'category': category,
            'date' : date,
            'poster_url': poster_url,
            'info_url': info_url,
        }
        db.tistory.insert_one(doc)
        print('완료: ', title, txt, category, date, poster_url, info_url)


if __name__ == '__main__':
    # 기존의 articles 콜렉션을 삭제하기
    db.tistory.drop()

    # 영화 사이트를 scraping 해서 db 에 채우기
    insert_all()