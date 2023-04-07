from flask import Blueprint, request, render_template

result_bp = Blueprint('result', __name__)
result_bp.maintenance_mode = False # 점검 상태 변수 선언

@result_bp.route('/')
def first():
  '''메인페이지'''
  # if current_app.config.get('MAINTENANCE_MODE') or result_bp.maintenance_mode:
  if result_bp.maintenance_mode:
    return render_template('maintenance.html')
  else:
    return render_template('result.html')