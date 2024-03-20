import requests

from bs4 import BeautifulSoup

def scrap_image(url):
    response = requests.get(url)
    html = response.content

    # HTML을 파싱
    soup = BeautifulSoup(html, 'html.parser')

    # 'og:image' 메타 태그 찾기
    og_image = soup.find('meta', property='og:image')

    # 'content' 속성의 값을 출력
    if og_image:
        return og_image["content"]
    else:
        return None