import requests
import json
import time

def return_routedata(start, end, week, tim):
  '''WEB에 전달할 original Data, 모델 예측을 위한 Pridict Data return'''
  t = tim + '00'
  
  if week == 5:
    w = ('SAT', 2)
  elif week == 6:
    w = ('SAT', 3) # API 공식 메뉴얼에 공휴일은 HOL로 되있지만 인자로 넣으면 에러가 남. 따라서 토요일로 대체
  else:
    w = ('DAY', 1)
    
  print(start, end, w[0], t)
  
  # 지하철 경로 탐색 API
  API_KEY = '7x1TU10Ct0763mZVXpBvYSYizKLENWLSWK9K1J6pz0euL7mh7iZhN0TEKp48968l7TFlRh9SXPsO%2BANWRXaDUA%3D%3D'
  SUBWAY_NAV_API = f'https://apis.data.go.kr/B553766/smt-path/path?serviceKey={API_KEY}&pageNo=1&numOfRows=300&dept_station_code={start}&dest_station_code={end}&week={w[0]}&search_type=FASTEST&dept_time={t}'
  
  time.sleep(1)
  
  raw = requests.get(SUBWAY_NAV_API)
  
  try:
    data = json.loads(raw.text)
    
    # 상선 하선 내선 외선 구분
    raw = data['data']['route']
    clss_list = []

    for i in range(len(raw) - 1):
      if int(raw[i]['line_num']) == int(raw[i + 1]['line_num']):
        if int(raw[i]['line_num']) in [2, 13, 14]: # 2호선
          if int(raw[i]['station_cd']) < int(raw[i + 1]['station_cd']):
            clss_list.append(3) # 내선
          else:
            clss_list.append(4) # 외선
        elif int(raw[i]['line_num']) in [1, 4]: # 1호선, 4호선
          if int(raw[i]['station_cd']) < int(raw[i + 1]['station_cd']):
            clss_list.append(1) # 상선
          else:
            clss_list.append(2) # 하선
        else: # 그 외 호선
          if int(raw[i]['station_cd']) < int(raw[i + 1]['station_cd']):
            clss_list.append(2) # 하선
          else:
            clss_list.append(1) # 상선
      else:
        continue # 환승하기전은 계산하지 않음
    
    predlist = []
    i = 0
    # 예측 데이터 format np.array([[week, st_code, clss, time]])
    
    for row in raw[:-1]:
      if row['transfer_loc'] != None:
        continue
      
      predlist.append([w[1], int(row['line_num']), int(row['station_cd']), clss_list[i], int(tim)])
      i = i+1
    
    return [row for row in raw if row['transfer_loc'] == None], predlist
  except:
    return False, False