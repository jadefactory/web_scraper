from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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
channel_name = pyautogui.prompt("채널명을 입력하세요.")
url = f"https://www.youtube.com/c/{channel_name}/videos"

# 엑셀 파일 생성
wb = openpyxl.Workbook()
ws = wb.create_sheet(channel_name)
ws.append(['번호', '제목', '조회수'])

chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
browser.implicitly_wait(10)
browser.maximize_window()
browser.get(url)

# 무한 스크롤 처리

# 스크롤 전 높이
before_h = browser.execute_script("return window.scrollY")

# 무한 스크롤
while True:
    # 맨 아래로 스크롤 내리기
    browser.find_element(by=By.CSS_SELECTOR, value="body").send_keys(Keys.END)

    # 스크롤 사이 페이지 로딩 시간
    time.sleep(1)

    # 스크롤 후 높이
    after_h = browser.execute_script("return window.scrollY")

    if after_h == before_h:
        break

    before_h = after_h

html = browser.page_source
soup = BeautifulSoup(html, "html.parser")
infos = soup.select("div#details")

sum_view = 0
for i, info in enumerate(infos, 1):
    # 제목
    title = info.select_one("a#video-title").text

    # 조회수
    views = info.select_one("div#metadata-line > span:nth-child(1)").text

    views = text_to_num(views)
    sum_view += views
    print(title, views)
    ws.append([i, title, views])

describe = f'{channel_name} 채널 평균 조회수: {round(sum_view/i, 2)}'
ws.append([describe])

wb.save(f'google/{channel_name}.xlsx')