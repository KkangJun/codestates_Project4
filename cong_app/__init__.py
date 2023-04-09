from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from cong_app.src.make_dataset import cong_dataset_update
from cong_app.src.make_model import model_update
from datetime import datetime, date

def create_app():
  app = Flask(__name__)
  # cong_app.config['MAINTENANCE_MODE'] = False # 점검 상태 변수 선언
  
  from cong_app.pages.main_page import main_bp
  from cong_app.pages.result_page import result_bp
  
  app.register_blueprint(main_bp)
  app.register_blueprint(result_bp, url_prefix='/result')

  def maintenance_status():
    ## 점검 상태 변경 함수 ##
    for bp in app.blueprints.values():
      if hasattr(bp, 'maintenance_mode'):
        bp.maintenance_mode = not bp.maintenance_mode

  # 스케줄링
  schedul = BackgroundScheduler({'apscheduler.timezone':'Asia/seoul'})
  schedul.add_job(func=maintenance_status, trigger='date', run_date=datetime(2024, 5, 1, 1, 10, 0))
  schedul.add_job(func=cong_dataset_update, trigger='date', run_date=datetime(2024, 5, 1, 1, 11, 0))
  schedul.add_job(func=model_update, trigger='date', run_date=datetime(2024, 5, 1, 2, 11, 0))
  schedul.add_job(func=maintenance_status, trigger='date', run_date=datetime(2024, 5, 1, 3, 12, 0))
  
  schedul.add_job(func=maintenance_status, trigger='date', run_date=datetime(2026, 5, 1, 1, 10, 0))
  schedul.add_job(func=cong_dataset_update, trigger='date', run_date=datetime(2026, 5, 1, 1, 11, 0))
  schedul.add_job(func=model_update, trigger='date', run_date=datetime(2026, 5, 1, 2, 11, 0))
  schedul.add_job(func=maintenance_status, trigger='date', run_date=datetime(2026, 5, 1, 3, 12, 0))
  # 2년 주기로 두번 실행

  schedul.start()
  return app

if __name__ == "__main__":
  app = create_app()
  app.run(debug=True)