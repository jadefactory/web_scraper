import requests
from bs4 import BeautifulSoup
import time

token = "Slack API KEY"
channel = "Slack Channel"

def post_message(token, channel, text):
    requests.post("https://slack.com/api/chat.postMessage",
        headers = {"Authorization":"Bearer" + token},
        data = {"channel":channel, "text": text}
    )

url = "https://www.toyoko-inn.com/korea/search"

data_obj = {
    'lcl_id': 'ko',
    'prcssng_dvsn': 'dtl',
    'sel_area_txt': '한국',
    'sel_htl_txt': '토요코인 서울강남',
    'chck_in': '2022/10/13',
    'inn_date': '1',
    'sel_area': '8',
    'sel_htl': '00282',
    'rsrv_num': '1',
    'sel_ldgngPpl': '1'
}

cnt = 1
while True:
    try:
        response = requests.post(url, data=data_obj)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        beds = soup.select("ul.btnLink03")

        for i, bed in enumerate(beds, 1):
            links = bed.select('a')
            if len(links) > 0:
                if i <= 3:
                    post_message(token, channel, "싱글 잔실 있어요!")
                    
                elif i <= 5:
                    post_message(token, channel, "더블 잔실 있어요!")
            
            print(f'{cnt}번째 시도입니다.')
            time.sleep(10)
            cnt += 1
    
    except:
        print("오류가 발생했지만 계속 실행")