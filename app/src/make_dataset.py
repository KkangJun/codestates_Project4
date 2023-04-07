import psycopg2
import os
import csv
import requests
import json
import re
import time

def db_init():
  '''DB 연결 및 초기화'''
  conn = psycopg2.connect(
    host='localhost',
    dbname='train_db',
    user='project4',
    password='abcdqwer',
    port='5432'
  )
  
  cur = conn.cursor()

  # DB 업데이트를 위한 TABLE 정리
  cur.execute('DROP TABLE IF EXISTS train_cong;')
  cur.execute('''CREATE TABLE train_cong (
    id    SERIAL    PRIMARY KEY,
    number_asc  INTEGER,
    week  VARCHAR(10)   NOT NULL,
    line  INTEGER   NOT NULL,
    st_code   INTEGER   NOT NULL,
    st_name   VARCHAR(50)   NOT NULL,
    cls   VARCHAR(10)   NOT NULL,
    time  INTEGER,
    congestion  FLOAT
  );''')
  
  conn.commit()
  cur.close()
  
  return conn

def _cong_dataset(path, conn, num):
  '''지하철 혼잡도 API를 이용해 DB로 저장
    path : INFO_URL에서 가져온 혼잡도 API PATH
    conn : 클라우드 DB 연결 객체
    num : API PATH 순서'''
  cur = conn.cursor()
  
  API_KEY = '7x1TU10Ct0763mZVXpBvYSYizKLENWLSWK9K1J6pz0euL7mh7iZhN0TEKp48968l7TFlRh9SXPsO%2BANWRXaDUA%3D%3D'
  CONGESTION_API = f'https://api.odcloud.kr/api{path}?page=1&perPage=2000&serviceKey={API_KEY}'

  cong_raw = requests.get(CONGESTION_API)
  cong_data = json.loads(cong_raw.text)
  
  time.sleep(1)
  
  for data in cong_data['data']:
    number_asc = num
    week = data['조사일자']
    line = int(data['호선'])
    st_code = int(data['역번호'])
    st_name = data['역명']
    cls = data['구분']
    
    for t, c in list(cong_data['data'][0].items())[:-6]:
      times = int(re.sub(r'[^0-9]', '', t))
      cong = float(c)
      cur.execute(f'''INSERT INTO train_cong VALUES
                  (DEFAULT, {number_asc}, '{week}', {line}, {st_code}, '{st_name}', '{cls}', {times}, {cong});''')
  
  conn.commit()
  cur.close()
  return

def cong_dataset_update():
  '''Dataset Update 함수'''
  
  # 추후 혼잡도 데이터 업데이트를 위한 INFO parsing
  INFO_URL = 'https://infuser.odcloud.kr/oas/docs?namespace=15071311/v1'

  path_raw = requests.get(INFO_URL)
  path_data = json.loads(path_raw.text)

  update_paths = list(path_data['paths'])[-1:] # update 시 이코드 사용
  # 참고 : 지하철 혼잡도 데이터 갱신주기가 2년이라, 현재는 가장 최근 2021년 데이터만 사용 추후 API의 갱신 주기가 빨라지면 바꿀 예정

  time.sleep(1)
  
  conn = db_init()
  
  for i, path in enumerate(update_paths):
    _cong_dataset(path, conn, i+1)
  
  conn.commit()
  conn.close()
  print('update completed')
  return