import os
from selenium import webdriver
from bs4 import BeautifulSoup

restaurant_num_list = []
restaurant_name_list = []
restaurant_category_list = []
restaurant_address_list = []
restaurant_phone_list = []
restaurant_info_list = []

## 한페이지 안에 있는 음식점 고유 넘버 크롤링 (* 여기서 고유 넘버란 음식점 마다 url에 숫자가 존재하는데 이를 고유 넘버라고 부르기로 정함!!)
def Crawl_RestaurantNum_perPage(restaurant_list):
    for restaurant in restaurant_list:
        restaurant_num = restaurant.select('.rating > a')[0]['href']
        restaurant_num_list.append(re.findall(r"com/(\d+)", restaurant_num)[0])

options = webdriver.ChromeOptions() # 크롬 브라우저 옵션
# options.add_argument('headless')    # 브라우저 안 띄우기
options.add_argument('lang=ko_KR')  # KR 언어
chromedriver_path = '/Users/mckimair/chromedriver'
driver = webdriver.Chrome(os.path.join(os.getcwd(), chromedriver_path), options = options) # chromedriver 열기


url = 'https://map.kakao.com'
driver.get(url)

search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]') # 검색창
search_area.send_keys('제주도 맛집')
driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER) # Enter로 검색
driver.implicitly_wait(3) # 기다려 주자
more_page = driver.find_element_by_id("info.search.place.more")
time.sleep(2)
more_page.send_keys(Keys.ENTER) # 더보기 누르고
# 첫 번째 검색 페이지 끝
time.sleep(1) # 기다려 주자

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
for i in range(1,6):
    if i != 1:
        driver.find_element_by_xpath(f'//*[@id="info.search.page.no{i}"]').send_keys(Keys.ENTER)
    restaurant_list = soup.select('.placelist > .PlaceItem')

Crawl_RestaurantNum_perPage(restaurant_list)

driver.quit() # driver 종료, 브라우저 닫기
