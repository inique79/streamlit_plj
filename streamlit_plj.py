# import mlb_stat
import streamlit as st
import pandas as pd
import statsapi
import pandas as pd
import datetime
from tabulate import tabulate



player_id = [673490,808982,678225,808970] #김하성,이정후,배지환,고우석
division = ['nlw','nlc'] #내셔널 서부지구, 내셔널 중부지구
team_id = [135,137,134] #샌디에고,샌프란시스코,피츠버그




today = '03/20/2024'
class Playerstats:
    def __init__(self,player_id):
        self.player_id = player_id
        self.game_data = {}
        self.season_data = {}
        self.team_result = {}
        

    def get_gamedata(self,player_id,team_id):
        game = statsapi.schedule(start_date=today ,end_date=today,team=team_id) 
        try:

            if game:
                game_id = game[0]['game_id']  #게임 아이디 확인 목적
                if statsapi.boxscore_data(game_id, timecode=None)['teamInfo']['away']['id'] == team_id:
                    homeaway = "away" #홈인지 어웨이인지 체크
                else:
                    homeaway = "home"

                self.team_result={'금일 팀 성적' : statsapi.linescore(game_id)}
                batting = statsapi.boxscore_data(game_id, timecode=None)[homeaway]['players']['ID'+str(player_id)]['stats']['batting']
                print(batting)
                self.game_data = {'안타': batting['hits'],  # 안타
                    '2루타' : batting['doubles'],  #2루타
                    '3루타' : batting['triples'], #3루타
                    '홈런' : batting['homeRuns'], #홈런
                    '볼넷' : batting['baseOnBalls'], #볼넷
                    '삼진' : batting['strikeOuts'], #삼진아웃
                    '타수' : batting['atBats'], #타수
                    '도루' : batting['stolenBases'],  #도루
                    '타점' : batting['rbi'],  # 타점
                    '득점' : batting['runs'],  # 득점
                    '투구수': batting['hits'],  # 투구수
                    '승리' : batting['doubles'],  #승리
                    '패배' : batting['triples'],  #패전
                    '블론' : batting['homeRuns'],  #블론세이브
                    '피득점' : batting['strikeOuts'],  #피득점
                    '홀드' : batting['atBats']} #홀드

        except Exception as e:
            print('Error 발생')
            print(e)
        return self.game_data, self.team_result , game

    def get_season_data(self,player_id):
        try:
            if statsapi.player_stat_data(player_id, group="[hitting]", type="season")['stats'][0]['stats']:
                season_raw = self.season_data = statsapi.player_stat_data(player_id, group="[hitting]", type="season")['stats'][0]['stats']
                del season_raw['groundOuts']
                del season_raw['airOuts']
                del season_raw['intentionalWalks']
                del season_raw['caughtStealing']
                del season_raw['groundIntoDoublePlay']
                del season_raw['numberOfPitches']
                del season_raw['plateAppearances']
                del season_raw['totalBases']
                del season_raw['leftOnBase']
                del season_raw['groundOutsToAirouts']
                del season_raw['catchersInterference']
                del season_raw['atBatsPerHomeRun']
                del season_raw['stolenBasePercentage']
            else:
                season_raw = {'시즌 성적' : '시즌 성적이 없습니다' }
        except Exception as e:
            season_raw = {'시즌 성적' : '시즌 성적이 없습니다' }
            print(e)
        return season_raw
    

    
    def season_rank(self):
        try:
            slug_rank = statsapi.league_leaders('onBasePlusSlugging',statGroup='hitting',limit=5,season=2024,leagueId=104)  #아메리칸리그 장타율 순위
            avg_rank = statsapi.league_leaders('avg',statGroup='hitting',limit=5,season=2024,leagueId=104) #타율 순위
            hits_rank = statsapi.league_leaders('hits',statGroup='hitting',limit=5,season=2024,leagueId=104) #안타 순위
            obp_rank = statsapi.league_leaders('obp',statGroup='hitting',limit=5,season=2024,leagueId=104) #출루율 순위
            rbi_rank= statsapi.league_leaders('rbi',statGroup='hitting',limit=5,season=2024,leagueId=104) # 타점 순위
            runs_rank = statsapi.league_leaders('runs',statGroup='hitting',limit=5,season=2024,leagueId=104) #득점 순위
            homeruns_rank = statsapi.league_leaders('homeRuns',statGroup='hitting',limit=5,season=2024,leagueId=104) #득점 순위
            ops_rank = statsapi.league_leaders('ops',statGroup='hitting',limit=5,season=2024,leagueId=104) #ops순위
            stolenBases_rank = statsapi.league_leaders('stolenBases',statGroup='hitting',limit=5,season=2024,leagueId=104) #도루 순위
            return slug_rank, avg_rank, hits_rank, obp_rank, rbi_rank, runs_rank, ops_rank, stolenBases_rank,homeruns_rank
        except Exception as e:
            print(e)


# if __name__ =='__main__':
#     playerstat = Playerstats(673490)
#     playerstat.get_gamedata(673490, 135)
    # print(playerstat.get_season_data(673490))
            





# 사이드바에 선택 상자 추가
add_selectbox = st.sidebar.selectbox(
    "MLB 대표 한국 선수",
    ( "HS KIM","JH LEE","JH BAE")
)

playstats = mlb_stat.Playerstats(673490) #김하성 데이터
today_HSKIM = playstats.get_gamedata(673490,135) #김하성 금일 성적 함수 호출
print(f'{today_HSKIM[0]}434')
season_raw = playstats.get_season_data(673490)
df_HSKIM = pd.DataFrame(season_raw,index=['주요 지표']).transpose()
season_HSKIM = df_HSKIM


playstats = mlb_stat.Playerstats(808982) #이정후 데이터
today_JHLEE =playstats.get_gamedata(808982,137) #이정후 금일 성적 함수 호출
season_raw = playstats.get_season_data(808982)
df_JHLEE = pd.DataFrame(season_raw,index=['주요 지표']).transpose()
season_JHLEE = df_JHLEE


playstats = mlb_stat.Playerstats(678225) #배지환 데이터
today_JHBAE = playstats.get_gamedata(678225,134) #배지환 금일 성적 함수 호출
season_raw = playstats.get_season_data(678225)
df_JHBAE = pd.DataFrame(season_raw,index=['주요 지표']).transpose()
season_JHBAE = df_JHBAE

playstats.season_rank()
try:
    slug_rank, avg_rank, hits_rank, obp_rank, rbi_rank, runs_rank, ops_rank, stolen_bases_rank, homeruns_rank = playstats.season_rank()
except Exception as e:
    print('시즌 랭크 정보가 업데이트 되지 않았습니다')


# 이정후 
# 선택된 선수에 따른 정보 표시
if add_selectbox == "JH LEE":
    col1, col2 = st.columns([1,5])

    with col2:
        # 선수의 이름을 타이틀로 표시
        st.title("JH LEE")
        
        # 나이와 팀 정보를 가로로 나란히 표시하기 위한 HTML 테이블 사용
        st.markdown("""
        <div style="display:flex; flex-direction:row;">
                    <div style="margin-right:5px;">25세
                    </div>
                    <div>샌프란시스코 자이언츠
                    </div>
        </div>
        """, unsafe_allow_html=True)

    # 선수의 이미지를 첫 번째 컬럼에 표시
    col1.image("https://search.pstatic.net/common?type=b&size=216&expire=1&refresh=true&quality=100&direct=true&src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2FprofileImg%2F63a0ab2c-68a7-40d3-a04f-591a6fe029f1.jpg", width=90)

    st.divider()
    col3, col4 = st.columns(2)
    with col3: 
        st.subheader("오늘의 성적")
        if today_JHLEE[2][0]['status'] != 'Scheduled' and today_JHLEE[0]['타수'] != None :
            st.text(f"오늘 {today_JHLEE[0]['타수']}타수, {today_JHLEE[0]['안타']}안타")
            st.text(f"2루타 {today_JHLEE[0]['2루타']}개, 3루타 {today_JHLEE[0]['3루타']}개, 홈런 {today_JHLEE[0]['홈런']}개")
            st.text(f"타점 {today_JHLEE[0]['타점']}개, 도루 {today_JHLEE[0]['도루']}개, 사사구 {today_JHLEE[0]['볼넷']}개")
        elif today_JHLEE[2][0]['status'] != 'Scheduled' and today_JHLEE[0]['타수'] == None :
            st.text('오늘 미출전')
        else:
            st.text('오늘 경기가 없습니다')
        st.divider()

        st.text('오늘 소속팀 경기 결과')
        if today_JHLEE[2][0]['status'] != 'Scheduled':
            st.text(f"{today_JHLEE[1]['금일 팀 성적']}")
        else:
            st.text('오늘 경기가 없습니다')
        

    with col4:
        st.subheader("시즌 성적")
        st.text(f'{season_JHLEE}')

    st.divider()

    st.subheader("주요 지표 순위")
    try:
        st.text('타율 순위')
        st.text(avg_rank)
        st.text('최다안타 순위')
        st.text(hits_rank)
        st.text('타점 순위')
        st.text(rbi_rank)
        st.text('홈런 순위')
        st.text(homeruns_rank)
        st.text('출루율 순위')
        st.text(obp_rank)
        st.text('장타율 순위')
        st.text(slug_rank)
        st.text('OPS 순위')
        st.text(ops_rank)
    except Exception as e:
        print(e)
        st.text("데이터가 업데이트 되지 않았습니다")

# 김하성
# 선택된 선수에 따른 정보 표시
if add_selectbox == "HS KIM":
    col1, col2 = st.columns([1,5])

    with col2:
        # 선수의 이름을 타이틀로 표시
        st.title("HS KIM")
        
        # 나이와 팀 정보를 가로로 나란히 표시하기 위한 HTML 테이블 사용
        st.markdown("""
        <div style="display:flex; flex-direction:row;">
                    <div style="margin-right:5px;">25세
                    </div>
                    <div>샌디에이고 파드리스
                    </div>
        </div>
        """, unsafe_allow_html=True)

    # 선수의 이미지를 첫 번째 컬럼에 표시
    col1.image("https://search.pstatic.net/common?type=b&size=216&expire=1&refresh=true&quality=100&direct=true&src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F27%2F202306011655528101.png", width=90)

    st.divider()
    col3,col4= st.columns(2)
    with col3:
        st.subheader("오늘의 성적")
        if today_HSKIM[2][0]['status'] != 'Scheduled' and today_HSKIM[0]['타수'] != None:
            st.text(f"오늘 {today_HSKIM[0]['타수']}타수, {today_HSKIM[0]['안타']}안타")
            st.text(f"2루타 {today_HSKIM[0]['2루타']}개, 3루타 {today_HSKIM[0]['3루타']}개, 홈런 {today_HSKIM[0]['홈런']}개")
            st.text(f"타점 {today_HSKIM[0]['타점']}개, 도루 {today_HSKIM[0]['도루']}개, 사사구 {today_HSKIM[0]['볼넷']}개")
        elif today_HSKIM[2][0]['status'] != 'Scheduled' and today_HSKIM[0]['타수'] == None :
            st.text('오늘 미출전')
        else:
            st.text('오늘 경기가 없습니다')
        st.divider()
        st.text('오늘 소속팀 경기 결과')
        if today_HSKIM[2][0]['status'] != 'Scheduled':
            st.text(today_HSKIM[1]['금일 팀 성적'])
        else:
            st.text('오늘 경기가 없습니다')


    with col4:
        st.subheader("시즌 성적")
        st.text(season_HSKIM)

    st.divider()

    st.subheader("주요 지표 순위")
    try:
        st.text('타율 순위')
        st.text(avg_rank)
        st.text('최다안타 순위')
        st.text(hits_rank)
        st.text('타점 순위')
        st.text(rbi_rank)
        st.text('홈런 순위')
        st.text(homeruns_rank)
        st.text('출루율 순위')
        st.text(obp_rank)
        st.text('장타율 순위')
        st.text(slug_rank)
        st.text('OPS 순위')
        st.text(ops_rank)
    except Exception as e:
        print(e)
        st.text("데이터가 업데이트 되지 않았습니다")

    





# 배지환
# 선택된 선수에 따른 정보 표시
if add_selectbox == "JH BAE":
    col1, col2 = st.columns([1,5])

    with col2:
        # 선수의 이름을 타이틀로 표시
        st.title("JH BAE")
        
        # 나이와 팀 정보를 가로로 나란히 표시하기 위한 HTML 테이블 사용
        st.markdown("""
        <div style="display:flex; flex-direction:row;">
                    <div style="margin-right:5px;">25세
                    </div>
                    <div>피츠버그 파이어리츠
                    </div>
        </div>
        """, unsafe_allow_html=True)

    # 선수의 이미지를 첫 번째 컬럼에 표시
    col1.image("https://search.pstatic.net/common?type=b&size=216&expire=1&refresh=true&quality=100&direct=true&src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F30%2F202307131651185171.png", width=90)

    st.divider()
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("오늘의 성적")
        if today_JHBAE[2][0]['status'] != 'Scheduled' and today_JHBAE[0]['타수'] != None:
            st.text(f"오늘 {today_JHBAE[0]['타수']}타수, {today_JHBAE[0]['안타']}안타")
            st.text(f"2루타 {today_JHBAE[0]['2루타']}개, 3루타 {today_JHBAE[0]['3루타']}개, 홈런 {today_JHBAE[0]['홈런']}개")
            st.text(f"타점 {today_JHBAE[0]['타점']}개, 도루 {today_JHBAE[0]['도루']}개, 사사구 {today_JHBAE[0]['볼넷']}개")
        elif today_JHBAE[2][0]['status'] != 'Scheduled' and today_JHBAE[0]['타수'] == None :
            st.text('오늘 미출전')
        else:
            st.text('오늘 경기가 없습니다')
        st.divider()
        
        st.text('오늘 소속팀 경기 결과')
        if today_JHBAE[2][0]['status'] != 'Scheduled':
            st.text(today_JHBAE[2][0]['status'])
            st.text(today_JHBAE[1]['금일 팀 성적'])
        else:
            st.text('오늘 경기가 없습니다')


    with col4:
        st.subheader("시즌 성적")
        st.text(season_JHBAE)

    st.divider()

    st.subheader("주요 지표 순위")
    try:
        st.text('타율 순위')
        st.text(avg_rank)
        st.text('최다안타 순위')
        st.text(hits_rank)
        st.text('타점 순위')
        st.text(rbi_rank)
        st.text('홈런 순위')
        st.text(homeruns_rank)
        st.text('출루율 순위')
        st.text(obp_rank)
        st.text('장타율 순위')
        st.text(slug_rank)
        st.text('OPS 순위')
        st.text(ops_rank)
    except Exception as e:
        print(e)
        st.text("데이터가 업데이트 되지 않았습니다")