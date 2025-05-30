import requests
from bs4 import BeautifulSoup
import json

def normalize_url(href):
    if href.startswith('//'):
        return 'https:' + href
    elif href.startswith('/'):
        return 'https://www.news.cn' + href
    else:
        return href

def extract_xinhua_categories():
    url = "http://www.news.cn/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    categories = []

    nav_div = soup.find('div', class_='nav right')
    if nav_div:
        a_tags = nav_div.find_all('a')
        for a_tag in a_tags:
            name = a_tag.get_text(strip=True)
            href = a_tag.get('href')
            if name and href:
                categories.append({
                    "name": name,
                    "url": normalize_url(href)
                })

    return categories

if __name__ == "__main__":
    categories = extract_xinhua_categories()
    print(json.dumps(categories, indent=2, ensure_ascii=False))
