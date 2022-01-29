import pandas as pd
import numpy as np
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import re

# 네이버 지도에서 XX동 맛집을 검색해서 맛집을 클릭하면
# url이 map.naver.ocm/v5/search/연남동%20맛집/place/-----------?c=1412...와 같은 형태임을 볼 수 있었습니다.
# 맛집마다 위 urldml ------자리에 오는 숫자가 다름을 확인하고
# -------자리의 숫자를 크롤링하여 matzip_num이라는 리스트에 넣어두었습니다.
# -------자리에 오는 숫자를 맛집 고유 넘버라고 부르겠습니다.

# 맛집 고유 넘버 넣을 리스트 생성
matzip_num = []


def crawl_regional_restaurant_num(keyword):
    globals()[f'matzip_num_{keyword}'] = []

    url = f'https://map.naver.com/v5/search/{keyword}/place/'

    driver = webdriver.Chrome('/Users/mckimair/chromedriver')  # 크롬드라이버 경로 입력
    driver.get(url)
    time.sleep(2)

    # iframe 변경
    driver.switch_to.frame('searchIframe')

    for num in tqdm(range(1, 7)):  # 네이버 지도에서 맛집을 검색하면 6장의 페이지가 나오기 때문에 6장을 크롤링(범위)

        # 스크롤바 클릭
        driver.find_element_by_xpath('//*[@id="_pcmap_list_scroll_container"]').click()
        # END 키를 눌러서 페이지 제일 하단으로 이동 = 스크롤 다운
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(2)
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(2)
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(2)
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(2)
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(2)
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(2)

        if num == 1:  # 첫번째 페이지에서는 다른 동작을 하지 않고 그대로 크롤링
            pass
        else:  # 두번째 페이지 부터는 옆으로 넘어가는 버튼을 클릭하고 크롤링
            driver.find_element_by_xpath('//*[@id="app-root"]/div/div[2]/div[2]/a[7]').click()

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        time.sleep(2)

        matzip_list = soup.findAll('li', {'class': '_1EKsQ _12tNp'})

        for i in tqdm(range(len(matzip_list))):
            driver.find_element_by_xpath(
                f'//*[@id="_pcmap_list_scroll_container"]/ul/li[{str(i + 1)}]/div[1]/a').send_keys(Keys.ENTER)
            time.sleep(2)

            current_url = driver.current_url  # 검색이 성공된 플레이스에 대한 개별 페이지

            unique_code = re.findall(r"place/(\d+)", current_url)
            globals()[f'matzip_num_{keyword}'].append(unique_code[0])
            time.sleep(2)

    driver.quit()

    matzip_df = pd.DataFrame()
    matzip_df['num'] = globals()[f'matzip_num_{keyword}']
    matzip_df.to_csv('matzip_num.csv')

    return matzip_df
