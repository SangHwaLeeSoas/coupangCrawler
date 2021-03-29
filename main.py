import datetime
import os
import re
import subprocess
import time
import random

from builtins import enumerate

# 크롤링
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# excel
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


# Properties
PAGE_LOADING_TIME = 10

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


# 품절 상품 찾기 함수
def findOutOfStock(driver, outStockList):
    time.sleep(PAGE_LOADING_TIME)
    outStock = driver.find_elements_by_xpath('//*[@class="out-of-stock"]//ancestor::a')
    for e in outStock:
        outStockList.append(e.get_attribute('href'))
    return outStockList


# Alert 제거 함수
def isAlert(driver):
    try:
        alert = driver.switch_to_alert()
        alert.accpet()
        return False
    except Exception:
        return True

def main():



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
    cpTitle = ''
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
        cpTitle = urls[inputInt][1]
        break;



    # 크롤링
    subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')  # 디버거 크롬 구동

    options = webdriver.ChromeOptions()
    options.add_argument("disable-gpu")
    options.add_argument("lang=ko_KR")
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
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

    # 품절 상품 리스트
    outStockList = []

    # 히스토리 세팅
    driver.get('https://google.com')
    time.sleep(PAGE_LOADING_TIME)
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
    driver.get('https://www.coupang.com/?src=1042016&spec=10304903&addtag=900&ctag=HOME&lptag=%EC%BF%A0%ED%8C%A1&itime=20210329220815&pageType=HOME&pageValue=HOME&wPcid=16170232950131418422682&wRef=www.google.com&wTime=20210329220815&redirect=landing&gclid=EAIaIQobChMI7K-GmMnV7wIVgsuWCh1CjwV_EAAYASAAEgLKC_D_BwE')
    time.sleep(PAGE_LOADING_TIME)

    # 얼럿 확인
    # driver.switch_to.alert.accept()

    # 쿠팡 접속
    driver.get(cpUrl)
    time.sleep(PAGE_LOADING_TIME)

    curPageNo = 1
    isNext = ''

    # 품절상품 수집
    # while True:
    #     time.sleep(PAGE_LOADING_TIME)
    #
    #     # 차단시 리로드
    #     soup = BeautifulSoup(driver.page_source, 'html.parser')
    #     title = str(soup.find('title'))
    #     if title.find('Denied') >= 0:
    #         print('쿠팡에서 접속을 거부했습니다. 재접속')
    #         driver.refresh()
    #         time.sleep(PAGE_LOADING_TIME)
    #
    #     time.sleep(random.randint(5, 10))
    #     print('curPageNo : ', curPageNo)
    #     # if isEnd:
    #     #     break
    #
    #     findOutOfStock(driver, outStockList)
    #
    #     pagination = driver.find_elements_by_xpath('//*[@class="page-warpper"]/a')
    #
    #     # 다음 번호 선택
    #     curPageNo = curPageNo + 1
    #     try:
    #         xpath = '//*[@class="page-warpper"]/a[@data-page="' + str(curPageNo) + '"]'
    #         e = driver.find_element_by_xpath(xpath)
    #     # 다음 버튼 || 끝
    #     except NoSuchElementException:
    #         # 다음 버튼 클릭
    #         try:
    #             nextBtn = driver.find_element_by_xpath('//*[@class="page-warpper"]/a[@class="next-page"]')
    #             print(len(nextBtn))
    #             e = nextBtn
    #         # 끝
    #         except NoSuchElementException:
    #             print('끝번호!!!')
    #             break;
    #             # limitBtn = driver.find_element_by_xpath('//*[@class="page-warpper"]/a[@class="icon next-page-dimmed"]')
    #             # if len(limitBtn) > 0:
    #             #     break;
    #
    #     # 스크롤 다운
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     # 다읍 페이지 클릭
    #     curPageNo = int(e.get_attribute('innerHTML'))
    #     webdriver.ActionChains(driver).move_to_element(e).click(e).perform()
    #     pagination.clear()
    #     time.sleep(PAGE_LOADING_TIME)

    # 개발용 테스트 데이터
    outStockList = [['https://www.coupang.com/vp/products/1271111126?itemId=2275791440&vendorItemId=70272921456&sourceType=CATEGORY&categoryId=194176'],
                    ['https://www.coupang.com/vp/products/111287760?itemId=335216426&vendorItemId=3822438016&sourceType=CATEGORY&categoryId=194176'],
                    ['https://www.coupang.com/vp/products/344626827?itemId=1094728390&vendorItemId=5613508016&sourceType=CATEGORY&categoryId=194176']]
    # 상세 정보 수집
    for i, e in enumerate(outStockList):
        driver.get(e[0])
        time.sleep(PAGE_LOADING_TIME)

        try:
            title = driver.find_element_by_xpath('//h2[@class="prod-buy-header__title"]').text
            price = driver.find_element_by_xpath('//span[@class="total-price"]').text.replace('원', '').strip()
            coNum = driver.find_element_by_xpath('//ul[@class="prod-description-attribute"]/li[last()]').text.split('쿠팡상품번호:')[1].split('-')[0].strip()
            reviewLi = driver.find_element_by_xpath('//ul[@class="tab-titles"]//ancestor::span[@class="product-tab-review-count"]')
            reviewCnt = reviewLi.text.replace('(', '').replace(')', '')

            print('title', title)
            print('price', price)
            print('coNum', coNum)
            print('revieCnt', reviewCnt)

            outStockList[i].append(title)
            outStockList[i].append(price)
            outStockList[i].append(coNum)
            outStockList[i].append(reviewCnt)

            # 리뷰 클릭
            # driver.execute_script("window.scrollTo(0, 1200);")
            driver.execute_script("$('html, body').animate({scrollTop : $('.product-tab-review-count').offset().top -200}, 400);")
            time.sleep(PAGE_LOADING_TIME)
            webdriver.ActionChains(driver).move_to_element(reviewLi).click(reviewLi).perform()
            if isAlert(driver):
                time.sleep(PAGE_LOADING_TIME)

            time.sleep(PAGE_LOADING_TIME)

            # 최신순 클릭
            driver.execute_script("$('html, body').animate({scrollTop : $('.js_reviewArticleOrderContainer').offset().top -200}, 400);")
            time.sleep(PAGE_LOADING_TIME)
            descBtn = driver.find_element_by_xpath('//div[@class="sdp-review__article__order__sort"]/*[@data-order="DATE_DESC"]')
            webdriver.ActionChains(driver).move_to_element(descBtn).click(descBtn).perform()
            if isAlert(driver):
                time.sleep(PAGE_LOADING_TIME)

            time.sleep(PAGE_LOADING_TIME)

            # 평균 별점
            driver.execute_script("$('html, body').animate({scrollTop : $('.js_reviewAverageTotalStarRating').offset().top -200}, 400);")
            time.sleep(PAGE_LOADING_TIME)
            avgRateDiv = driver.find_element_by_xpath('//div[@class="sdp-review__average__total-star__info-orange js_reviewAverageTotalStarRating"]')
            avgRate = avgRateDiv.get_attribute('data-rating')
            print('avgRate', avgRate)
            outStockList[i].append(avgRate)

            latestDiv = driver.find_element_by_xpath('//section[@class="js_reviewArticleListContainer"]/article/div/div[@class="sdp-review__article__list__info__product-info"]/div[@class="sdp-review__article__list__info__product-info__reg-date"]')
            latestDt = latestDiv.text.strip()
            print('latestDt', latestDt)
            outStockList[i].append(latestDt)

        except NoSuchElementException:
            print('---없음')

    print(outStockList)

    # 폴더
    DIR_NAME = datetime.datetime.now().strftime("%y%m%d_%H%M")
    PATH_SEPARATOR = '/'
    DIR_PATH = 'data'

    # 크롤링

    # 데이터 저장
    fileName = cpTitle.strip() + '_' + DIR_NAME + '.xlsx'
    df = pd.DataFrame(outStockList, columns=['URL', '상품명', '가격', '상품번호', '총리뷰 갯수', '평균 별점', '최신 리뷰일자']) # , '네이버 최저가', '에누리 최저가', '다나와 최저가'
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

