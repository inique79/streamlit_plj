#MLB 스탯을 네이버 블로그에 자동 포스팅하기 위한 코드

import sys
sys.path.append('/Users/parkhyunwoo/Desktop/dev/NAVER_BLG_PLJ')

import Naver_posting_interschool
import streamlit_plj
import mlb_stat
import pandas as pd
import datetime
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.naver.com"
# 아이디/비번
ID = os.environ.get('ID')
PASSWORD = os.environ.get('PASSWORD')

today = datetime.date.today()


player_id = [673490,808982,678225,808970] #김하성,이정후,배지환,고우석
division = ['nlw','nlc'] #내셔널 서부지구, 내셔널 중부지구
team_id = [135,137,134] #샌디에고,샌프란시스코,피츠버그

#셀레니움 셋업
naver_posting = Naver_posting_interschool.Naver_posting(url)

#크롤링 시작 
naver_posting.start_scraping()

# 네이버 로그인 시작
naver_posting.log_in(ID,PASSWORD)


# 블로그 버튼 / 창 전환 / 프레임 전환 등 사전 작업
naver_posting.pre_task()

#글쓰기 시작
naver_posting.start_posting()
    
title_xpath = '/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/section/article/div[1]/div[1]/div/div/p'
title_elem = WebDriverWait(naver_posting.driver,10).until(EC.presence_of_element_located((By.XPATH,title_xpath)))
action = ActionChains(naver_posting.driver)
(action
        .move_to_element(title_elem).pause(1)
        .click()
        .send_keys('오늘의 MLB 한국 선수 주요 성적')
        .perform()
        )
action.reset_actions()
naver_posting.driver.implicitly_wait(2)

players= {'김하성' : [streamlit_plj.today_HSKIM[0],streamlit_plj.season_HSKIM],' 이정후' : [streamlit_plj.today_JHLEE[0],streamlit_plj.season_JHLEE],'배지환' : [streamlit_plj.today_JHBAE[0],streamlit_plj.season_JHBAE]}

try:
        for key, value in players.items():
                contents_elem = naver_posting.driver.find_element(By.CSS_SELECTOR,'.se-canvas-bottom')
                contents_elem.click()
                action = ActionChains(naver_posting.driver)
                (action
                        .move_to_element(contents_elem).pause(2)
                        .click()
                        .send_keys(f'{today} 오늘의 {key} 성적')
                        .send_keys(Keys.ENTER)
                        .send_keys(f"오늘 {value[0]['타수']}타수 , {value[0]['안타']}안타 , 2루타 {value[0]['2루타']}개 , "
                                f"3루타 {value[0]['3루타']}개 , 홈런 {value[0]['홈런']}개 , "
                                f"타점 {value[0]['타점']}개 , 도루 {value[0]['도루']}개 , 사사구 {value[0]['볼넷']}개 ")
                        .send_keys(Keys.ENTER)
                        .send_keys(Keys.ENTER)
                        .send_keys(Keys.ENTER)
                        .send_keys(Keys.ENTER)
                        .perform()
                        )
                time.sleep(3)
except Exception as e:
        pass
        print('오류 발생')
time.sleep(20)
action = ActionChains(naver_posting.driver)
(action
                # .move_to_element(contents_elem).pause(2)
                # .click()
                .send_keys(Keys.ENTER)
                .send_keys('내셔널리그 주요 지표 순위')
                .send_keys(Keys.ENTER)
                .send_keys('타율 순위')
                .send_keys(streamlit_plj.avg_rank)
                .send_keys(Keys.ENTER)
                .send_keys('최다안타 순위')
                .send_keys(streamlit_plj.hits_rank)
                .send_keys(Keys.ENTER)
                .send_keys('타점 순위')
                .send_keys(streamlit_plj.rbi_rank)
                .send_keys(Keys.ENTER)
                .send_keys('득점 순위')
                .send_keys(streamlit_plj.runs_rank)
                .send_keys(Keys.ENTER)
                .send_keys('장타율 순위')
                .send_keys(streamlit_plj.slug_rank)
                .send_keys(Keys.ENTER)
                .send_keys('출루율 순위')
                .send_keys(streamlit_plj.obp_rank)
                .send_keys(Keys.ENTER)
                .send_keys('OPS 순위')
                .send_keys(streamlit_plj.ops_rank)
                .send_keys(Keys.ENTER)
                .send_keys('도루 순위')
                .send_keys(streamlit_plj.stolenBases_rank)
                .send_keys(Keys.ENTER)
                .perform())
time.sleep(20)


