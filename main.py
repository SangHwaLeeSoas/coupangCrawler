import datetime
import os
import re
import time
import random

from builtins import enumerate

# 크롤링
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# excel
import pandas as pd


urls = {
    1: [1, "여성패션", "https://www.coupang.com/np/categories/186764?listSize=120&brand=&offerCondition=&filterType=rocket%2C&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&rating=0"],
    2: [2, "남성패션", "https://www.coupang.com/np/categories/187069?listSize=120&brand=&offerCondition=&filterType=rocket%2C&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&rating=0"],
    3: [3, "유아동패션", "https://www.coupang.com/np/categories/213201?listSize=120&brand=&offerCondition=&filterType=rocket%2C&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&rating=0"],
    4: [4, "뷰티", "https://www.coupang.com/np/categories/176522?listSize=120&brand=&offerCondition=&filterType=rocket%2C&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&rating=0"],
    5: [5, "출산/유아동", "https://www.coupang.com/np/categories/221934?listSize=120&brand=&offerCondition=&filterType=rocket%2Crocket_wow%2Ccoupang_global&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&rating=0&rocketAll=true"],
    6: [6, "식품", "https://www.coupang.com/np/categories/194276?listSize=120&brand=&offerCondition=&filterType=rocket_wow%2C&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&rating=0"],
    7: [7, "주방용품", "https://www.coupang.com/np/categories/185669?listSize=120&brand=&offerCondition=&filterType=rocket%2C&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&rating=0"],
    8: [8, "생활용품", "https://www.coupang.com/np/categories/115673?listSize=120&brand=&offerCondition=&filterType=rocket%2C&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&rating=0"],
    9: [9, "홈인테리어", "https://www.coupang.com/np/categories/184555?listSize=120&brand=&offerCondition=&filterType=rocket_wow%2C&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&rating=0"],
    10: [10, "가전디지털", "https://www.coupang.com/np/categories/178255?listSize=120&brand=&offerCondition=&filterType=rocket%2C&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&rating=0"],
    11: [11, "스포츠/레저", "https://www.coupang.com/np/categories/317778?listSize=120&brand=&offerCondition=&filterType=rocket%2Ccoupang_global&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&rating=0&rocketAll=true"],
    12: [12, "자동차용품", "https://www.coupang.com/np/categories/184060?listSize=120&brand=&offerCondition=&filterType=rocket%2C&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&rating=0"],
    13: [13, "도서/음반/DVD", "https://www.coupang.com/np/categories/317777?listSize=120&brand=&offerCondition=&filterType=rocket%2C&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&rating=0"],
    14: [14, "완구/취미", "https://www.coupang.com/np/categories/317779?listSize=120&brand=&offerCondition=&filterType=rocket%2C&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&rating=0"],
    15: [15, "문구/오피스", "https://www.coupang.com/np/categories/177295?listSize=120&brand=&offerCondition=&filterType=rocket%2C&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&rating=0"],
    16: [16, "반려동물용품", "https://www.coupang.com/np/categories/115674?listSize=120&brand=&offerCondition=&filterType=rocket_wow%2C&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&rating=0"],
    17: [17, "헬스/건강식품", "https://www.coupang.com/np/categories/305798?listSize=120&brand=&offerCondition=&filterType=rocket_wow%2C&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=&rating=0"]
}


def main():

    # Properties
    PAGE_LOADING_TIME = 5

    print('###############################################################')
    print('프로그램 실행')
    print('###############################################################')
    print('=====================================')
    for key, value in urls.items():
        print(value[0], ' : ', value[1])
    print('=====================================')
    print('###############################################################')
    print('작업할 쿠팡 카테고리 번호를 선택해주세요.')
    print('###############################################################')

    cpUrl = ''

    while True:
        inputText = input('번호 : ')
        inputText = inputText.strip()

        # 문자열 검증
        try:
            inputInt = int(inputText)
        except ValueError as e:
            print('유효한 번호를 입력해주세요.')
            continue

        # 범위 검증
        if inputInt <= 0 or inputInt > len(urls):
            print('유효한 번호를 입력해주세요.')
            continue

        print('###############################################################')
        print(urls[inputInt][1], '크롤링을 시작합니다.')
        print('###############################################################')
        cpUrl = urls[inputInt][2]
        break;



    # 크롤링
    options = webdriver.ChromeOptions()
    options.add_argument("disable-gpu")
    options.add_argument("lang=ko_KR")
    # options.add_argument('--proxy-server=' + 'localhost:8080')
    # options.add_argument('--proxy-server=socks5://' + '127.0.0.1:9150')
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    # options.add_argument('headless')
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    # ChromDriver 연동 세팅
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.implicitly_wait(PAGE_LOADING_TIME)
    driver.maximize_window()

    time.sleep(PAGE_LOADING_TIME)

    # 엑셀 저장 리스트
    excelList = []

    # 폴더
    DIR_NAME = datetime.datetime.now().strftime("%y%m%d_%H%M")
    PATH_SEPARATOR = '/'
    DIR_PATH = 'data' + PATH_SEPARATOR + DIR_NAME

    # 크롤링

    # 데이터 저장
    fileName = DIR_NAME + '.xlsx'
    df = pd.DataFrame(excelList, columns=['URL', 'DATE', '价格', '起批量', '手机专享', '物流', '快递', '供应等级',
                                          '经营模式', '货描', '响应', '发货', '回头率', '产品类别', '货号'])
    df.to_excel(DIR_PATH + PATH_SEPARATOR + fileName, index=False)

    print('==================================')
    print('크롤링이 완료되었습니다.')
    print('==================================')


if __name__ == '__main__':
    # try:
    main()
    # except Exception as e:
    #     print('==================================')
    #     print('크롤링이 실패했습니다.')
    #     print('해당 URL의 접속 상태를 확인하세요.')
    #     print(e)
    #     print('==================================')
    # finally:
    #     input('아무 키를 눌러 종료해주세요.')

