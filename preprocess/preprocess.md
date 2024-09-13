# 전처리 과정

## 네이버 뉴스와 다음 뉴스의 title과 content의 클랜징과 전처리 과정

### title 열 클렌징

df['title'] = df['title'].str.replace(r'\d+', '', regex=True)  # 숫자 제거

df['title'] = df['title'].apply(lambda x: re.sub(r'[^\w\s]|[\u4e00-\u9fff]|▁', '', x))  # 특수문자, 한문, '▁' 제거

df['title'] = df['title'].apply(lambda x: re.sub(r'[^\w\s]|▁', '', x))  # 특수기호 및 '▁' 제거

df['title'] = df['title'].str.replace(r'[a-zA-Z]', '', regex=True)  # 영어 제거

df['title'] = df['title'].str.strip()  # 앞뒤 공백 제거

df['title'] = df['title'].str.replace(r'\s+', ' ', regex=True)  # 다중 공백 단일화

### content 열 클렌징

df['content'] = df['content'].str.replace(r'\d+', '', regex=True)  # 숫자 제거

df['content'] = df['content'].apply(lambda x: re.sub(r'[^\w\s]|[\u4e00-\u9fff]|▁', '', x))  # 특수문자, 한문, '▁' 제거

df['content'] = df['content'].apply(lambda x: re.sub(r'[^\w\s]|▁', '', x))  # 특수기호 및 '▁' 제거

df['content'] = df['content'].str.replace(r'[a-zA-Z]', '', regex=True)  # 영어 제거

df['content'] = df['content'].str.strip()  # 앞뒤 공백 제거

df['content'] = df['content'].str.replace(r'\s+', ' ', regex=True)  # 다중 공백 단일화

### 결측값 처리 (빈 문자열로 대체)

df['content'] = df['content'].fillna('')

df['author'] = df['author'].fillna('')

df['title'] = df['title'].fillna('')

### content 중복 데이터 제거

df = df.drop_duplicates(subset=['content'])

### title 중복된 데이터 제거

df = df.drop_duplicates(subset=['title'])

## 토큰화
### 네이버와 다음뉴스의 title에서는 명사만 추출하고 content는 토큰화만 시킨다

### Mecab 사용

from konlpy.tag import Mecab

mecab = Mecab(dicpath="C:/mecab/mecab-ko-dic")

### title 열에서 명사만 추출하여 기존 열 수정

df['title'] = df['title'].fillna('').apply(lambda x: ' '.join(mecab.nouns(x)))

### content 열의 결측값을 빈 문자열로 대체한 후 토큰화하여 기존 열 수정
df['content'] = df['content'].fillna('').apply(lambda x: ' '.join(mecab.morphs(x)))


