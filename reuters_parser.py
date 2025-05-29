import requests
from bs4 import BeautifulSoup
import json

def extract_reuters_article(url):
    # 사용자 에이전트 설정 - 브라우저처럼 보이게 함
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 제목 추출: h1 태그, data-testid="Heading"
    title_tag = soup.find('h1', attrs={'data-testid': 'Heading'})
    title = title_tag.get_text(strip=True) if title_tag else None

    # 기자명 및 게시 시간 추출
    author_name = None
    author_link = None
    published_time = None
    
    # 기자명 추출: data-testid="SignOff" 속성을 가진 p 태그에서 추출
    author_p = soup.find('p', attrs={'data-testid': 'SignOff'})
    if author_p:
        author_name = author_p.get_text(strip=True)
    
    author_info_div = soup.find('div', class_='author-bio__author-info__2IJ1y')
    if author_info_div:
        author_link_tag = author_info_div.find('a', attrs={'data-testid': 'Heading'})
        if author_link_tag and 'href' in author_link_tag.attrs:
            author_link = author_link_tag.get('href')
            # 상대 경로인 경우 절대 URL로 변환
            if author_link and author_link.startswith('/'):
                author_link = 'https://www.reuters.com' + author_link
    
    time_tag = soup.find('time')
    if time_tag:
        published_time = time_tag.get_text(strip=True)

    # 본문 문단 추출: data-testid="paragraph-0"부터 시작하여 순차적으로 증가
    sentences = []
    idx = 0
    while True:
        para_tag = soup.find('div', attrs={'data-testid': f'paragraph-{idx}'})
        if not para_tag:
            break
        text = para_tag.get_text(strip=True)
        if text:
            sentences.append({
                "id": idx + 1,
                "text": text,
                "translation": ""
            })
        idx += 1

    # JSON 결과 생성
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
    test_url = "https://www.reuters.com/world/europe/telegram-founder-says-france-asked-him-ban-conservative-romanian-voices-2025-05-19/"
    article_data = extract_reuters_article(test_url)
    print(json.dumps(article_data, indent=2, ensure_ascii=False))