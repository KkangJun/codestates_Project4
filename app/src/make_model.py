import psycopg2
import time
import numpy as np
import pandas as pd
import tensorflow as tf
from category_encoders import OrdinalEncoder
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, Input, BatchNormalization, Activation

# 이동 방향에 따른 역번호 증가
# 1호선(상선 증가) , 2호선(내선 증가), 3호선(하선 증가), 4호선(상선 증가), 5호선(하선 증가), 6호선(하선 증가), 7호선(하선 증가), 8(하선 증가)
# line 13(2호선), line 14(2호선), line 15(5호선)

def dataset_load():
  conn = psycopg2.connect(
    host='localhost',
    dbname='train_db',
    user='project4',
    password='abcdqwer',
    port='5432'
  )

  time.sleep(1)

  dataset = pd.read_sql("SELECT * FROM train_cong", conn)

  conn.close()

  dataset.drop(['id', 'number_asc', 'st_name', 'line'], axis=1, inplace=True)
  dataset.sort_values(['week', 'st_code', 'clss', 'time'], inplace=True)
  dataset.reset_index(drop=True, inplace=True)

  return dataset

def data_preprocessing(dataset):
  dataset = dataset.replace({'평일':1, '토요일':2, '일요일':3, '상선':1, '하선':2, '내선':3, '외선':4})

  x_train = dataset.drop('congestion', axis=1)
  y_train = dataset['congestion']
  
  return x_train, y_train

def make_model(x_train):
  inputs = Input(shape=(x_train.shape[1]))
  
  layer = Dense(256, kernel_initializer='he_normal')(inputs)
  layer = BatchNormalization()(layer)
  layer = Activation('relu')(layer)
  layer = Dropout(0.2)(layer)
  
  layer = Dense(128, kernel_initializer='he_normal')(inputs)
  layer = BatchNormalization()(layer)
  layer = Activation('relu')(layer)
  layer = Dropout(0.2)(layer)
  
  layer = Dense(64, kernel_initializer='he_normal')(inputs)
  layer = BatchNormalization()(layer)
  layer = Activation('relu')(layer)
  layer = Dropout(0.2)(layer)
  
  outputs = Dense(1, name='output')(layer)
  
  model = Model(inputs=inputs, outputs=outputs)
  model.compile(optimizer='adam', loss='mean_squared_error')
  
  return model

def model_update():
  dataset = dataset_load()
  
  x_train, y_train = data_preprocessing(dataset)
  
  model = make_model(x_train)
  
  model.fit(x_train, y_train, batch_size=128, epochs=30)
  model.save('../ai_model/latest_model.h5')
  
  print('dataset update completed')
  return