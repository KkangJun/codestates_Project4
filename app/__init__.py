from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from app.src.make_dataset import cong_dataset_update
from datetime import datetime, date

def create_app():
  app = Flask(__name__)
  # app.config['MAINTENANCE_MODE'] = False # 점검 상태 변수 선언
  
  from app.pages.main_page import main_bp
  from app.pages.result_page import result_bp
  
  app.register_blueprint(main_bp)
  app.register_blueprint(result_bp, url_prefix='/result')

  def maintenance_status():
    ## 점검 상태 변경 함수 ##
    for bp in app.blueprints.values():
      if hasattr(bp, 'maintenance_mode'):
        bp.maintenance_mode = not bp.maintenance_mode

  # 스케줄링
  schedul = BackgroundScheduler({'apscheduler.timezone':'Asia/seoul'})
  schedul.add_job(func=maintenance_status, trigger='date', run_date=datetime(2024, 5, 1, 1, 11, 11))
  schedul.add_job(func=cong_dataset_update, trigger='date', run_date=datetime(2024, 5, 1, 1, 11, 11))
  schedul.add_job(func=maintenance_status, trigger='date', run_date=datetime(2024, 5, 1, 1, 11, 11))
  
  schedul.add_job(func=maintenance_status, trigger='date', run_date=datetime(2026, 5, 1, 1, 11, 11))
  schedul.add_job(func=cong_dataset_update, trigger='date', run_date=datetime(2026, 5, 1, 1, 11, 11))
  schedul.add_job(func=maintenance_status, trigger='date', run_date=datetime(2026, 5, 1, 1, 11, 11))
  # 2년 주기로 실행 (데이터 갱신도 늦고 4~5년 이전까지 서비스 종료한다고 판단)

  schedul.start()

if __name__ == "__main__":
  app = create_app()
  app.run()