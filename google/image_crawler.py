from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import urllib.request
import pyautogui

keyword = pyautogui.prompt("검색어를 입력하세요.")

if not os.path.exists(f"{keyword}"):
    os.mkdir(f"{keyword}")

url = f"https://www.google.com/search?q={keyword}&sxsrf=ALiCzsbbDQXImlszympGzwSboSTdtuIz9g:1652166326485&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjW2_-Xr9T3AhXqQfUHHT0QDm0Q_AUoAXoECAIQAw&biw=1863&bih=913&dpr=1"

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
imgs = browser.find_elements_by_css_selector(".rg_i.Q4LuWd")

for i, img in enumerate(imgs, 1):
    # 이미지를 클릭
    # click intercepted error 처리
    browser.execute_script("arguments[0].click();", img)
    time.sleep(1)
    
    # 큰 이미지 주소 추출
    if i == 1:
        target = browser.find_elements_by_css_selector("img.n3VNCb")[0]
    else:
        target = browser.find_elements_by_css_selector("img.n3VNCb")[1]
        
    img_src = target.get_attribute("src")

    # 이미지 다운로드
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(img_src, f'{keyword}/{i}.jpg')