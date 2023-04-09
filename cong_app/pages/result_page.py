import numpy as np
import os
from flask import Blueprint, request, render_template
from tensorflow.keras.models import load_model
from datetime import datetime
from cong_app.src.make_model import st_dict
from cong_app.src.route import return_routedata

result_bp = Blueprint('result', __name__)
result_bp.maintenance_mode = False # 점검 상태 변수 선언

@result_bp.route('/', methods=['GET', 'POST'])
def first():
  '''결과페이지'''
  days = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
  model = load_model('cong_app/ai_model/latest_model.h5')
  st = st_dict()
  preds = []
  # 예측 데이터 format : np.array([[week, st_code, clss, time]])
  
  if request.method == 'POST':
    start_st = str(st[request.form['start']]).zfill(4)
    end_st = str(st[request.form['end']]).zfill(4)
    date = request.form['date']
    
    week = datetime.strptime(date, '%Y-%m-%dT%H:%M').weekday()
    time = date.split('T')[1].replace(':','').zfill(4)
    
    org_data, preddata = return_routedata(start_st, end_st, week, time)
    
    if org_data == False:
      return render_template('error.html', st_name_list=list(st))
    
    for i, row in enumerate(preddata):
      pred = (model.predict(np.array([row])))
      timestamp = org_data[i]['timestamp'][:2] + ':' + org_data[i]['timestamp'][2:4]
      preds.append({'line': org_data[i]['line_num'], 'name': org_data[i]['station_nm'], 'time': timestamp, 'pred': round(pred[0][0], 1)})
    
    last_st = {'line': org_data[-1]['line_num'], 'name': org_data[-1]['station_nm'], 'time': org_data[-1]['timestamp'][:2] + ':' + org_data[-1]['timestamp'][2:4]}
  # if current_app.config.get('MAINTENANCE_MODE') or result_bp.maintenance_mode:
  if result_bp.maintenance_mode:
    return render_template('maintenance.html')
  else:
    return render_template('result.html', week=days[week], preds=preds, last_st=last_st, st_name_list=list(st))