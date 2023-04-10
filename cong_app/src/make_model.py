import psycopg2
import time
import numpy as np
import pandas as pd
import tensorflow as tf
import keras
import pickle
from category_encoders import OrdinalEncoder
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, Input, BatchNormalization, Activation

# 이동 방향에 따른 역번호 증가
# 1호선(상선 증가) , 2호선(내선 증가), 3호선(하선 증가), 4호선(상선 증가), 5호선(하선 증가), 6호선(하선 증가), 7호선(하선 증가), 8(하선 증가)
# line 13(2호선), line 14(2호선), line 15(5호선)

def dataset_load():
  '''DB에서 Dataset 불러오기'''
  conn = psycopg2.connect(
    host='192.168.35.23',
    dbname='train_db',
    user='project4',
    password='abcdqwer',
    port='5432'
  )

  time.sleep(1)

  dataset = pd.read_sql("SELECT * FROM train_cong", conn)

  conn.close()

  return dataset

def st_dict():
  '''WEB에서 사용할 지하철역 딕셔너리'''
  dataset = dataset_load()
  data = dataset[['st_name', 'st_code']].drop_duplicates()
  st_list = {}
  for name, code in zip(data['st_name'], data['st_code']):
    # 새로운 키 추가
    if code < 200:
      st_list[name+'(1호선)'] = code
    elif code < 300:
      st_list[name+'(2호선)'] = code
    elif code < 400:
      st_list[name+'(3호선)'] = code
    elif code < 2500:
      st_list[name+'(4호선)'] = code
    elif code < 2600:
      st_list[name+'(5호선)'] = code
    elif code < 2700:
      st_list[name+'(6호선)'] = code
    elif code < 2700:
      st_list[name+'(7호선)'] = code
    elif code < 2700:
      st_list[name+'(8호선)'] = code
  
  return st_list

def data_preprocessing(dataset):
  '''학습을 위한 데이터 전처리'''
  model_path = '/Users/kkangjun/Desktop/Study/CodeStates/Project/Project4/codestates_Project4/cong_app/ai_model'
  
  dataset.drop(['id', 'number_asc', 'st_name'], axis=1, inplace=True)
  dataset.sort_values(['week', 'st_code', 'clss', 'time'], inplace=True)
  dataset.reset_index(drop=True, inplace=True)
  
  dataset = dataset.replace({'평일':1, '토요일':2, '일요일':3, '상선':1, '하선':2, '내선':3, '외선':4})

  x_train = dataset.drop('congestion', axis=1)
  y_train = dataset['congestion']
  
  scaler = StandardScaler()
  x_scaled = scaler.fit_transform(x_train)

  with open(model_path + '/scaler_pickle.pkl', 'wb') as pklf:
    pickle.dump(scaler, pklf)
  
  return x_scaled, y_train

def make_model(x_train):
  '''모델 제작'''
  inputs = Input(shape=(x_train.shape[1]))
  
  layer = Dense(512, kernel_initializer='he_normal')(inputs)
  layer = BatchNormalization()(layer)
  layer = Activation('relu')(layer)
  layer = Dropout(0.2)(layer)
  
  layer = Dense(256, kernel_initializer='he_normal')(layer)
  layer = BatchNormalization()(layer)
  layer = Activation('relu')(layer)
  layer = Dropout(0.2)(layer)
  
  layer = Dense(128, kernel_initializer='he_normal')(layer)
  layer = BatchNormalization()(layer)
  layer = Activation('relu')(layer)
  layer = Dropout(0.2)(layer)
  
  layer = Dense(64, kernel_initializer='he_normal')(layer)
  layer = BatchNormalization()(layer)
  layer = Activation('relu')(layer)
  layer = Dropout(0.2)(layer)
  
  outputs = Dense(1, name='output')(layer)
  
  model = Model(inputs=inputs, outputs=outputs)
  model.compile(optimizer='adam', loss='mean_squared_error')
  
  return model

def model_update():
  '''Model Update 함수'''
  model_path = '/Users/kkangjun/Desktop/Study/CodeStates/Project/Project4/codestates_Project4/cong_app/ai_model'
  dataset = dataset_load()
  
  x_train, y_train = data_preprocessing(dataset)
  
  early_stop = keras.callbacks.EarlyStopping(monitor='loss', patience=5, verbose=1)
  save_best = keras.callbacks.ModelCheckpoint(filepath=model_path + '/latest_model.h5', monitor='loss', verbose=1,
                                              save_best_only=True, save_weights_only=False)

  model = make_model()

  model.fit(x_train, y_train, batch_size=128, epochs=300, callbacks=[early_stop, save_best])
  
  print('dataset update completed')
  return