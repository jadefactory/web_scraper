from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pyautogui
import openpyxl

def text_to_num(text):
    text = text.replace("조회수","").replace("회","").strip()

    if "억" in text:
        num = float(text.replace("억","").strip()) * 100000000
    elif "만" in text:
        num = float(text.replace("만","").strip()) * 10000
    elif "천" in text:
        num = float(text.replace("천","").strip()) * 1000
    elif "없음" == text:
        num = 0
    else:
        num = int(text)

    return num
 
# 검색어 입력
keyword = pyautogui.prompt("검색어를 입력하세요.")

# 엑셀 파일 생성
wb = openpyxl.Workbook()
ws = wb.create_sheet(keyword)
ws.append(['번호', '제목', '조회수', '날짜'])

url = f"https://www.youtube.com/results?search_query={keyword}"
browser = webdriver.Chrome("/Users/jade/Desktop/web_crawling/driver/chromedriver")
browser.implicitly_wait(10)
browser.maximize_window()
browser.get(url)

# 7번 스크롤하기
scroll_count = 5

i = 1
while True:
    # 맨 아래로 스크롤을 내린다.
    browser.find_element_by_css_selector("body").send_keys(Keys.END)

    # 스크롤 사이에 페이지 로딩 시간
    time.sleep(2)

    if i == scroll_count:
        break
    i += 1

# Selenium - BeautifulSoup 연동방법
html = browser.page_source
soup = BeautifulSoup(html, "html.parser")
infos = soup.select("div.text-wrapper")

for i, info in enumerate(infos, 1):
    # 원하는 정보 가져오기
    # 제목
    title = info.select_one("a#video-title").text

    try:
        # 조회수
        views = info.select_one("div#metadata-line > span:nth-child(1)").text

        # 날짜
        date = info.select_one("div#metadata-line > span:nth-child(2)").text
        
    except:
        views = "조회수 0회"
        date = "날짜 없음"

    views = text_to_num(views)
    print(title, views, date)
    ws.append([i, title, views, date])

wb.save(f'google/{keyword}.xlsx')