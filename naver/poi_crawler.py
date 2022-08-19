from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = "https://map.naver.com/v5/"
browser = webdriver.Chrome("/Users/jade/Desktop/portfolio/_web_crawling/driver/chromedriver")
browser.implicitly_wait(10)
browser.maximize_window()
browser.get(url)

# 검색창 입력
search = browser.find_element_by_css_selector("input.input_search")
search.click()
time.sleep(1)
search.send_keys("강남역맛집")
time.sleep(1)
search.send_keys(Keys.ENTER)
time.sleep(2)


# iframe 안으로 들어가기
browser.switch_to.frame("searchIframe")

# iframe 밖으로 나오기
# browser.switch_to_default_content()



# 가게 이름 10개 가져오기
names = browser.find_elements_by_css_selector("span.OXiLu")

for name in names:
    print(name.text)
