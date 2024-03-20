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
