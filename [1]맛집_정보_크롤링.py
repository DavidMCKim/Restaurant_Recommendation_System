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

# 홈페이지에서 맛집에 대해 소개할 정보들을 담아둘 리스트 생성
# 맛집 유형(ex. 카페, 한식, 중식 등등) : matzip_type
# 맛집 이름 : matzip_name
# 맛집 주소 : matzip_addr
# 맛집 평점 : matzip_score
# 맛집 전화번호 : matzip_phone
matzip_type = []
matzip_name = []
matzip_addr = []
matzip_score = []
matzip_phone = []

## 맛집정보 크롤링 코드 함수화
def info_crawl(rocalname):
    driver = webdriver.Chrome('/Users/mckimair/chromedriver')

    for i in tqdm(globals()[f'{rocalname}_matzip_num']['num']):
        new_url = f'https://pcmap.place.naver.com/accommodation/{i}/home?'
        driver.get(new_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        time.sleep(1)
        name = soup.find('span', {'class': '_3XamX'})
        style = soup.find('span', {'class': '_3ocDE'})
        addr = soup.find('span', {'class': '_2yqUQ'})
        score = soup.find('span', {'class': '_1Y6hi _1A8_M'})
        phone_num = soup.find('span', {'class': '_3ZA0S'})

        try:
            matzip_type.append(style.text)  ## 캠핑장 유형
        except:
            matzip_type.append('none')

        try:
            matzip_name.append(name.text)  ## 캠핑장 이름
        except:
            matzip_name.append('none')

        try:
            matzip_addr.append(addr.text)  ## 캠핑장 주소
        except:
            matzip_addr.append('none')

        try:
            matzip_score.append(score.em.text)  ## 캠핑장 평균별점
        except:
            matzip_score.append('none')
        ## 전화번호
        try:
            matzip_phone.append(phone_num.text)
        except:
            matzip_phone.append('none')

    driver.quit()

    globals()[f'{rocalname}_matzip_dict'] = {'Num': globals()[f'{rocalname}_matzip_num']['num'].to_list(),
                                             'Type': matzip_type, 'Name': matzip_name, 'Address': matzip_addr,
                                             'Score': matzip_score, 'Phone': matzip_phone}
    globals()[f'{rocalname}_matzip_info_df'] = pd.DataFrame(globals()[f'{rocalname}_matzip_dict'])

    globals()[f'{rocalname}_matzip_info_df'].to_csv(f'{rocalname}_matzip_info_df.csv')

    return matzip_type, matzip_name, matzip_addr, matzip_score, matzip_phone, globals()[f'{rocalname}_matzip_info_df']

