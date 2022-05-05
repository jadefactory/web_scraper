import requests
from bs4 import BeautifulSoup
import pyautogui
import openpyxl

keyword = pyautogui.prompt("검색어를 입력하세요 >>>")

wb = openpyxl.Workbook('coupang_result.xlsx')
ws = wb.create_sheet(keyword)
ws.append(['순위', '브랜드명', '상품명', '가격', '상세페이지 링크'])

rank = 1
done = False
for page in range(1, 5):
    if done == True:
        break
   
    main_url = f"https://www.coupang.com/np/search?&q={keyword}&page={page}"

    header = {
        'Host': 'www.coupang.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
    }

    # 헤더에 User-Agent, Accept-Language를 추가하지 않으면 오류가 난다(멈춰버림)
    response = requests.get(main_url, headers=header)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    links = soup.select("a.search-product-link") # select의 결과는 리스트 자료형

    for link in links:
        # 광고 상품 제거
        if len(link.select("span.ad-badge-text")) > 0:
            print("광고 상품입니다.")
        else:
            sub_url = "https://www.coupang.com/" + link.attrs["href"]

            response = requests.get(sub_url, headers=header)
            html = response.text
            soup = BeautifulSoup(html, "html.parser")

            # 브랜드명(있을 수도 있고, 없을 수도 있다)
            # 중고상품일 때는 태그가 달라진다
            # try - except로 예외처리를 해주면 된다
            try:
                brand_name = soup.select_one("a.prod-brand-name").text
            except:
                brand_name = ""

            # 상품명
            product_name = soup.select_one("h2.prod-buy-header__title").text
            # 가격
            try:
                product_price = soup.select_one("span.total-price > strong").text
            except:
                product_price = 0
            print(rank, brand_name, product_name, product_price)
            ws.append([rank, brand_name, product_name, product_price, sub_url])
            rank += 1
            if rank > 100:
                done = True
                break

wb.save('coupang_result.xlsx')