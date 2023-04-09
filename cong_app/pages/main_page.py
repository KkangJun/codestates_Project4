from flask import Blueprint, render_template, current_app
from cong_app.src.make_model import st_dict

main_bp = Blueprint('main', __name__)
main_bp.maintenance_mode = False # 점검 상태 변수 선언

@main_bp.route('/')
def first():
  '''메인페이지'''
  # if current_cong_app.config.get('MAINTENANCE_MODE') or main_bp.maintenance_mode:
  
  st_name_list = list(st_dict())
  
  if main_bp.maintenance_mode:
    return render_template('maintenance.html')
  else:
    return render_template('first.html', st_name_list=st_name_list)