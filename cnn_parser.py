import requests
from bs4 import BeautifulSoup
import json

def extract_cnn_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 제목
    title_tag = soup.find(class_='headline__text')
    title = title_tag.get_text(strip=True) if title_tag else None

    # 기자 정보
    author_tag = soup.find(class_='byline__names')
    if author_tag:
        author_name = author_tag.find('span').get_text(strip=True) if author_tag.find('span') else None
        author_link = author_tag.find('a')['href'] if author_tag.find('a') else None
    else:
        author_name = None
        author_link = None

    # 게시 시간
    timestamp_tag = soup.find(class_='timestamp')
    published_time = timestamp_tag.get_text(strip=True) if timestamp_tag else None

    # 본문: <p> 태그 기준으로 sentences 리스트 생성
    article_body = soup.find(class_='article__content')
    sentences = []

    if article_body:
        for idx, p_tag in enumerate(article_body.find_all('p'), start=1):
            text = p_tag.get_text(strip=True)
            if text:
                sentence_entry = {
                    "id": idx,
                    "text": text,
                    "translation": "",
                }
                sentences.append(sentence_entry)

    # JSON 결과
    article_json = {
        "title": title,
        "author": {
            "name": author_name,
            "link": author_link
        },
        "published_time": published_time,
        "sentences": sentences
    }

    return article_json


if __name__ == "__main__":
    test_url = "https://edition.cnn.com/2025/05/11/health/tina-knowles-mother-wellness?iid=cnn_buildContentRecirc_end_recirc"
    article_data = extract_cnn_article(test_url)

    print(json.dumps(article_data, indent=2, ensure_ascii=False))
