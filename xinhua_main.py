import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import time

BASE_URL = "http://www.news.cn"

def get_main_latest_articles(count=5):
    res = requests.get(BASE_URL)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    
    result = []
    for li in soup.select('div.list.list-txt.dot li'):
        a_tag = li.find('a')
        if a_tag and a_tag.get('href') and a_tag.text.strip():
            href = a_tag['href']
            full_url = urljoin(BASE_URL, href)
            result.append({
                "title": a_tag.text.strip(),
                "url": full_url
            })
        if len(result) >= count:
            break
    return result

def extract_xinhua_article(url, id=None, title=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # 제목
    title_tag = soup.select_one('div.mheader.domMobile span.title')
    extracted_title = title_tag.get_text(strip=True) if title_tag else title

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
        "id": id,
        "title": extracted_title,
        "url": url,
        "author": {
            "name": author_name,
            "link": None
        },
        "published_time": published_time,
        "sentences": sentences
    }

    return article_json




def xinhua_main(count=5):
    print(f"[*] 신화망 최신 기사 {count}개 수집 중...")
    try:
        articles = get_main_latest_articles(count)
        if not articles:
            print("[!] 최신 기사를 찾을 수 없습니다.")
            return None

        all_details = []
        for idx, article in enumerate(articles, 1):
            print(f"[+] ({idx}/{count}) 기사 수집 중: {article['title']}")
            try:
                detail = extract_xinhua_article(
                    url=article['url'],
                    id=idx,
                    title=article['title']
                )
                all_details.append(detail)
            except Exception as e:
                print(f"[ERROR] 기사 파싱 실패: {article['url']} | 에러: {e}")
            time.sleep(1)  # 과도한 요청 방지

        return all_details
    except Exception as e:
        print(f"[ERROR] 신화망 기사 수집 중 오류 발생: {e}")
        return None

if __name__ == "__main__":
    count = 30  # 원하는 기사 수로 조정 가능
    data = xinhua_main(count)
    if data:
        print(json.dumps(data, ensure_ascii=False, indent=2))
