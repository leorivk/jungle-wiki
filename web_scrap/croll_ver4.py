import requests

from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

db = client["jg_wiki_db"]  

# 검색 요청 -> 스크랩 메서드
def scrap_tistory(url, keyword):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    
    data = requests.get(url + "search/" + keyword, headers=headers)
    
    soup = BeautifulSoup(data.text, 'html.parser')

    articles = soup.select('div.list_content')
    
    if len(articles) == 0:
        print("길이가 0")
        return
    
    # 길이가 1 이상이면 렌더링

    # 이미지, 제목, 본문의 일부, url, 닐찌?, 태그?
    for article in articles:
        tag_element = article.select_one('strong.tit_post')
        if not tag_element:
            continue
        title = tag_element.text  
        # print(title)

        tag_element = article.select_one('p.txt_post')
        if not tag_element:
            continue
        txt = tag_element.text

        if article.select_one('div.list_content > a > img') is None :
            poster_url = None
        else :
            tag_element = article.select_one('div.list_content > a > img')['src']
            poster_url_a = tag_element
            poster_url = 'https:' + poster_url_a
        
        # tag_element = article.select_one('div.list_content > a > img')['src']
        # if tag_element is not None :
        #     poster_url_a = tag_element
        #     poster_url = 'https:' + poster_url_a 
        # else :
        #     poster_url = (None)
        print(poster_url)

        tag_element = article.select_one('div.list_content > a')
        if not tag_element:
            continue
        info_url_a = tag_element['href']
        info_url = 'https://' + 'krafton-jungle-essay' + '.tistory.com/' + info_url_a
        print(info_url)


        doc = {
            'title': title,
            'txt': txt,
            'poster_url': poster_url,
            'info_url': info_url,
        }
        
        # velog, tistory db를 굳이 나눠야할까?
        # 두 플랫폼 모두에서 같은 json 형식으로 저장할 수 있으면 나누지 않아도 상관 X -> blogs?로 단일화
        db.blog.insert_one(doc)
        print('완료: ', title, txt, poster_url, info_url)

def scrap_velog(url, keyword):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    data = requests.get(url + keyword + '&username=' + 'typo', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    velog = soup.select('#root > div:nth-child(2) > div:nth-child(3) > div:nth-child(3) > div')
    print(len(velog))

    for article in velog:
        tag_element = article.select_one('h2')
        if not tag_element:
            continue
        title = tag_element.text
        # print(title)

        tag_element = article.select_one('p')
        if not tag_element:
            continue
        txt = tag_element.text 
        # print(txt)

        tag_element = article.select_one('img')['src']
        if tag_element is not None :
            poster_url = tag_element
        else :
            poster_url = (None)    
        
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
            'poster_url': poster_url,
            'info_url': info_url,
        }
        db.blog.insert_one(doc)
        print('완료: ', title, txt, poster_url, info_url)
        
scrap_tistory("https://krafton-jungle-essay.tistory.com/", "변화와 비교")
scrap_velog("https://velog.io/search?q=", "품질")
