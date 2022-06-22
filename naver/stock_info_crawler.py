import requests
from bs4 import BeautifulSoup
import pyautogui
import openpyxl

wb = openpyxl.Workbook()
ws = wb.create_sheet("코스피")
ws.append(["종목명", "PER", "ROE", "PBR", "유보율"])

lastpage = int(pyautogui.prompt("몇 페이지까지 크롤링할까요? (1페이지=50개)"))

for i in range(1, lastpage + 1):
    url = f"https://finance.naver.com/sise/field_submit.naver?menu=market_sum&returnUrl=http://finance.naver.com/sise/sise_market_sum.naver?page={i}&fieldIds=per&fieldIds=roe&fieldIds=pbr&fieldIds=reserve_ratio"

    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    trs = soup.select("table.type_2 > tbody > tr[onmouseover='mouseOver(this)']")
    for tr in trs:
        name = tr.select_one('td:nth-child(2)').text
        per = tr.select_one('td:nth-child(7)').text
        roe = tr.select_one('td:nth-child(8)').text
        pbr = tr.select_one('td:nth-child(9)').text
        reserve_ratio = tr.select_one('td:nth-child(10)').text

        # 'N/A'값이 아닐 경우에만 데이터 수집
        if per != 'N/A' and roe != 'N/A' and pbr != 'N/A' and reserve_ratio != 'N/A':
            per = float(per.replace(',', ''))
            roe = float(roe.replace(',', ''))
            pbr = float(pbr.replace(',', ''))
            reserve_ratio = float(reserve_ratio.replace(',',''))
            print(name, per, roe, pbr, reserve_ratio)

            ws.append([name, per, roe, pbr, reserve_ratio])

wb.save("stock_data.xlsx")