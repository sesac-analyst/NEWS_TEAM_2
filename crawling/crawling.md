# Naver news crawling

### 날짜 범위 설정
start_date = datetime.strptime
end_date = datetime.strptime
날짜 범위: 20230901~20240901

### 장르별 section_id 리스트 생성
section_ids = ['731', '226', '227', '732', '283', '229', '228', '230']

base_url = f"https://news.naver.com/breakingnews/section/105/{section_id}?date={date}"

### section_id 리스트 네임
    # 731 : 모바일 
    # 226 : 인터넷/SNS 
    # 227 : 통신/뉴미디어 
    # 732 : 보안/해킹 
    # 283 : 컴퓨터 
    # 229 : 게임/리뷰 
    # 228 : 과학 일반 
    # 230 : IT 일반
네이버 뉴스는 url뒤에 번호를 사용해서 뉴스의 주제를 바꾸기에 주소에 들어갈 숫자의 리스트를 만들어 사용했다.


### BeautifulSoup의 request를 사용해 html을 파서하여 title, content, author, update_date, publisher_id를 가져왔다
article_response = requests.get(url)
        article_response.raise_for_status()
        article_soup = BeautifulSoup(article_response.text, 'html.parser')

### 멀티스레딩을 이용해 각 URL에서 데이터를 크롤링
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
  for result in tqdm(executor.map(crawl_article, urls), desc=f'Processing articles on {date}, section {section_id}', total=len(urls), unit='article', dynamic_ncols=True, ascii=True):
                all_results.append(result)
url을 크롤링하는데 대량의 데이터를 가져오기에 시간을 단축하기위해 멀티스레딩을 사용했다.
time.sleep(0.3)
중간중간 지연시간을 두어 서버차단당하지 않게 time으로 딜레이를 추가해 주었다.

# Daum news crawling

### 카테고리 ID 설정
category_id = 'IT'

다음은 네이버와 달리 IT라는 하나의 id로 묶여있기에 it로 묶어주고 
날짜의 범위는 네이버와 같다.

###  BeautifulSoup의 request로 html을 파싱
def fetch_page_urls(date_str, page):
    url = f'https://news.daum.net/breakingnews/digital?page={page}&regDate={date_str}'
    response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

네이버와 다음은 기사주제의 구조가 다르기에 살짝 다르게 코드를 구성했다 
다음은 request로  html을 가져와 title과 content를 가져오면 되었지만
네이버는 IT주제 링크로 들어간뒤 각 주제의 section_ids의 url을 가져왔다.

### 다음 뉴스의 url도 멀티스레드로 가져온다
with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_article_data, url): url for url in urls}
