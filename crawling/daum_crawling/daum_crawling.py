import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.notebook import tqdm
import time

# 카테고리 ID 설정
category_id = 'IT'

# 날짜 범위 설정
start_date = datetime(2023, 9, 1)
end_date = datetime(2024, 9, 1)

def fetch_page_urls(date_str, page):
    url = f'https://news.daum.net/breakingnews/digital?page={page}&regDate={date_str}'
    response = requests.get(url)
    
    if response.status_code != 200:
        return [], True

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 뉴스 리스트 엘리먼트 찾기
    news_list = soup.find_all('ul', class_='list_news2 list_allnews')
    
    if not news_list:
        return [], True  # 뉴스 리스트가 없으면 종료
    
    page_urls = []
    for news_section in news_list:
        news_items = news_section.find_all('li')
        for item in news_items:
            link = item.find('a', class_='link_txt')['href']
            page_urls.append(link)
    
    return page_urls, False

def collect_urls_for_date(date):
    date_str = date.strftime('%Y%m%d')
    page = 1
    all_urls = []
    previous_page_urls = set()

    while True:
        page_urls, is_end = fetch_page_urls(date_str, page)
        if is_end or not page_urls or set(page_urls) == previous_page_urls:
            break
        
        previous_page_urls = set(page_urls)
        all_urls.extend(page_urls)
        page += 1
    
    return all_urls

def collect_urls_for_range(start_date, end_date):
    current_date = start_date
    all_urls = []
    total_days = (end_date - start_date).days + 1
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(collect_urls_for_date, current_date + timedelta(days=i)): (current_date + timedelta(days=i)).strftime('%Y%m%d') for i in range(total_days)}
        
        with tqdm(total=total_days, desc='전체 URL 수집 진행 상황', leave=True) as date_bar:
            for future in as_completed(futures):
                date_str = futures[future]
                try:
                    daily_urls = future.result()
                    all_urls.extend(daily_urls)
                except Exception as e:
                    print(f'{date_str}에서 URL 수집 중 오류 발생: {e}')
                date_bar.update(1)
                
    return all_urls

def fetch_article_data(url):
    try:
        time.sleep(0.3)  # 요청 간 지연
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 제목 크롤링
        title_tag = soup.find('h3', class_='tit_view')
        title = title_tag.get_text() if title_tag else 'Null'
        
        # 작성자와 날짜 크롤링
        author_tag = soup.find('span', class_='txt_info')
        author = author_tag.get_text() if author_tag else 'Null'
        date_tag = soup.find('span', class_='num_date')
        publication_date = date_tag.get_text() if date_tag else 'Null'
        
        # 본문 크롤링 (p 태그에서 text만 추출, 특정 클래스의 p 태그 제외)
        paragraphs = soup.find_all('p')
        content = ''
        for paragraph in paragraphs:
            if 'class' not in paragraph.attrs:
                content += paragraph.get_text() + ' '
        
        # 출처 크롤링
        publisher_id_tag = soup.find('a', {'data-tiara-action-name': 'GNB언론사명_클릭'})
        publisher_id = publisher_id_tag.get_text() if publisher_id_tag else 'Null'

        # 데이터 저장
        return {
            'article_url': url,
            'title': title.strip(),
            'author': author.strip(),
            'publication_date': publication_date.strip(),
            'content': content.strip(),
            'publisher_id': publisher_id.strip(),
            'category_id': category_id,
            'platform_id': '다음'  # 플랫폼 ID를 '다음'으로 설정
        }
    except Exception as e:
        print(f'기사 데이터 크롤링 중 오류 발생: {e}')
        return None

def collect_article_data(urls):
    results = []
    total_urls = len(urls)
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_article_data, url): url for url in urls}
        
        with tqdm(total=total_urls, desc='기사 데이터 크롤링 진행 상황', leave=True) as url_bar:
            for future in as_completed(futures):
                url = futures[future]
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as e:
                    print(f'{url}에서 기사 크롤링 중 오류 발생: {e}')
                url_bar.update(1)

    return results

# URL 수집 및 기사 데이터 크롤링
print("URL 수집 시작...")
urls = collect_urls_for_range(start_date, end_date)
print(f"총 {len(urls)}개의 URL 수집됨.")

print("기사 데이터 크롤링 시작...")
results = collect_article_data(urls)

# CSV 파일로 저장
csv_file = "news_data_range.csv"
csv_columns = ['article_url', 'title', 'author', 'publication_date', 'content', 'publisher_id', 'category_id', 'platform_id']

try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        with tqdm(total=len(results), desc='CSV 파일 저장 진행 상황', leave=True) as pbar:
            for row in results:
                writer.writerow(row)
                pbar.update(1)
except IOError:
    print("I/O error")

print(f"크롤링 완료. '{csv_file}'에 데이터 저장됨.")
