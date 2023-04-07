from flask import Blueprint, render_template, current_app

main_bp = Blueprint('main', __name__)
main_bp.maintenance_mode = False # 점검 상태 변수 선언

@main_bp.route('/')
def first():
  '''메인페이지'''
  # if current_app.config.get('MAINTENANCE_MODE') or main_bp.maintenance_mode:
  if main_bp.maintenance_mode:
    return render_template('maintenance.html')
  else:
    return render_template('first.html')