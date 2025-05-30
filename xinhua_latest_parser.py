import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://www.news.cn"

def get_main_latest_articles():
    res = requests.get(BASE_URL)
    res.encoding = 'utf-8'  # 필요에 따라 'gbk'로 변경
    soup = BeautifulSoup(res.text, 'html.parser')
    
    result = []
    for li in soup.select('div.list.list-txt.dot li'):
        a_tag = li.find('a')
        if a_tag and a_tag.get('href') and a_tag.text.strip():
            href = a_tag['href']
            full_url = href if href.startswith('http') else BASE_URL + href
            result.append({
                "title": a_tag.text.strip(),
                "url": full_url
            })
    return result

# 실행 예시
articles = get_main_latest_articles()
print(json.dumps(articles, ensure_ascii=False, indent=2))
