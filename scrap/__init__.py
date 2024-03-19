import requests

from bs4 import BeautifulSoup
from db import db

# 검색 요청 -> 스크랩 메서드
def scrap_tistory(url, keyword):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    
    data = requests.get(url + "search/" + keyword, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    articles = soup.select('div.list_content')
    
    if len(articles) == 0:
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
 
        tag_element = article.select_one('div.detail_info > a')
        if not tag_element:
            continue
        category = tag_element.text  
        # print(category)

        tag_element = article.select_one('span.txt_date')
        if not tag_element:
            continue
        date = tag_element.text  
        # print(date)


        tag_element = article.select_one('div.list_content > a > img')['src']
        if not tag_element:
            continue

        poster_url_a = tag_element
        poster_url = 'https:' + poster_url_a 
        # print(poster_url)

        tag_element = article.select_one('div.list_content > a.thumbnail_post')
        if not tag_element:
            continue
        info_url_a = tag_element['href']
        info_url = 'https://krafton-jungle-essay.tistory.com/' + info_url_a
        # print(info_url)


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

def scrap_velog(user_url, keyword):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    
    username = user_url.split('@')[1]
    url = "https://velog.io/search?q=" + keyword + '&username=' + username
    
    data = requests.get(url, headers=headers)

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
            'poster_url': poster_url,
            'info_url': info_url,
        }
        db.blog.insert_one(doc)
        print('완료: ', title, txt, poster_url, info_url)
        