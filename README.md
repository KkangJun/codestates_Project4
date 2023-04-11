# CodeStates Project4
## 서울 지하철역 시간별 혼잡도 예상 API
지하철을 타고 가고있을 때 언제쯤이면 혼잡한게 풀릴까... 라는 생각이 많이 들었고, 현재 또는 미래의 가는 경로의 혼잡도를 예측해보고 싶다..!! 해서 작업하게 되었습니다.
1. 오픈 시간 : 4월 13일 ~ 4월 19일 사이 맥북으로 작업하고 있을 때 (평균 09시 ~ 19시, 주말은 오픈 X)

2. 사용방법 :
- 출발지, 도착지, 출발 시간, 날짜 입력
- 경로에 있는 역마다 혼잡률 예측 (각 역의 도착시간에 맞게)
- 자리에 앉을 가능성이 있는 부분 강조

#### (참고) 데이터셋이 1~8호선 까지만 지원하고, 2년 주기로 업데이트 되므로 정확한 예측은 힘듭니다...
#### (데이터셋은 2021년 기준, api 업데이트는 짝수년에 진행 됨 예) 2024년 api 업데이트 - 데이터셋 2023년 기준)  
### Link : [지하철 혼잡도 예측 앱](http://211.204.34.56:59)  
  
3. API
- [공공데이터포털 서울교통공사 지하철 혼잡도](https://www.data.go.kr/tcs/dss/selectFileDataDetailView.do?publicDataPk=15071311#tab-layer-openapi)
- [공공데이터포털 서울교통공사 지하철 경로정보](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15097640)
4. Program
- PostgreSQL (로컬 서버 DB)
- Tableau-Desktop (Dashboard 툴)
- VScode
5. WEB Serving Pipeline
- Flask
- Gunicorn
- NginX (Port Forwarding)