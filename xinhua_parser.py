import requests
from bs4 import BeautifulSoup
import json

def extract_xinhua_article(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # 제목
    title_tag = soup.select_one('div.mheader.domMobile span.title')
    title = title_tag.get_text(strip=True) if title_tag else None

    # 게시 시간
    published_time = None
    info_div = soup.select_one('div.mheader.domMobile div.info')
    if info_div:
        published_time = info_div.get_text(strip=True)

    # 기자 이름
    author_name = None
    author_span = soup.select_one('div#articleEdit span.editor')
    if author_span:
        author_name = author_span.get_text(strip=True)

    # 본문 문단
    sentences = []
    content_div = soup.select_one('div.main-left span#detailContent')
    if content_div:
        paragraphs = content_div.find_all('p')
        for idx, p in enumerate(paragraphs):
            text = p.get_text(strip=True)
            if text:
                sentences.append({
                    "id": idx + 1,
                    "text": text,
                    "translation": ""
                })

    # JSON 생성
    article_json = {
        "title": title,
        "author": {
            "name": author_name,
            "link": None  # 신화망은 기자 링크 없음
        },
        "published_time": published_time,
        "sentences": sentences
    }

    return article_json


if __name__ == "__main__":
    test_url = "http://www.news.cn/politics/xxjxs/20250520/441ea40542f34d83b1c81352e7c22a9e/c.html"  
    article_data = extract_xinhua_article(test_url)
    print(json.dumps(article_data, indent=2, ensure_ascii=False))
