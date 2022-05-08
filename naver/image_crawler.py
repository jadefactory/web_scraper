from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import urllib.request
import pyautogui

keyword = pyautogui.prompt("검색어를 입력하세요.")

if not os.path.exists(f"{keyword}"):
    os.mkdir(f"{keyword}")

url = f"https://search.naver.com/search.naver?where=image&sm=tab_jum&query={keyword}"
browser = webdriver.Chrome("/Users/jade/Desktop/web_crawling/driver/chromedriver")
browser.implicitly_wait(10)
browser.maximize_window()
browser.get(url)

# 무한 스크롤 처리

# 스크롤 전 높이
before_h = browser.execute_script("return window.scrollY")

# 무한 스크롤
while True:
    # 맨 아래로 스크롤 내리기
    browser.find_element_by_css_selector("body").send_keys(Keys.END)

    # 스크롤 사이 페이지 로딩 시간
    time.sleep(1)

    # 스크롤 후 높이
    after_h = browser.execute_script("return window.scrollY")

    if after_h == before_h:
        break

    before_h = after_h

# 이미지 태그 추출
imgs = browser.find_elements_by_css_selector("._image._listImage")


for i, img in enumerate(imgs, 1):
    # 각 이미지 태그의 주소
    img_src = img.get_attribute("src")
    print(i, img_src)
    urllib.request.urlretrieve(img_src, f'{keyword}/{i}.png')