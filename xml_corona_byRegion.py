import urllib.request
import pandas as pd
from datetime import datetime,timedelta
import requests
import xmltodict
import openpyxl

url_base = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey='
url_serviceKey = 'XK5R2J%2B6nCIWNwl5Bn7iYOJ6fRZ4cyiryScBggttDGsPPsbXjvKJLlZ%2FOhHS3Uf2M3DHKjex3HMOdivbFB5Blg%3D%3D'
url_pages = '10'
url_start_date = '20200527'
url_end_date = datetime.today().strftime('%Y%m%d')

url = url_base + url_serviceKey + '&pageNo=1&num0fRows=' + url_pages + '&startCreateDt=' + url_start_date + '&endCreateDt=' + url_end_date

print("Raw Data url:" + url)

fileName = input('결과 데이터 문서명: ')

req = requests.get(url).content

xmlObject = xmltodict.parse(req)

dict_data = xmlObject['response']['body']['items']['item']

df_conf = pd.DataFrame(dict_data)
df_conf1 = df_conf[['createDt','deathCnt','gubun','isolClearCnt','isolIngCnt']]
df_conf1.columns = ['날짜','사망자수','구분','격리해소','격리중']

with pd.ExcelWriter('./'+fileName+'.xlsx') as writer:
    df_conf1.to_excel(writer, sheet_name = 'raw_data')

'''
# 불러온 데이터 중 하루에 두 번 이상 데이터가 존재하는 경우를 대비해(오전, 오후), 하루 중 마지막에 발표한 데이터로 중복 처리
df_conf = df_conf.drop_duplicates(['stateDt'])

# 데이터를 날짜순으로 오름차순 정리
df_conf_1 = df_conf.sort_values(by='stateDt')

df_conf_1.to_excel('./data.xlsx',sheet_name=1)

# 공공데이터포털의 일일값의 합과 누적값에 차이 있어
# 명확한 가이드라인이 주어지지 않으면 누적값을 차분에 계산

# 숫자여야 할 열(누적확진자)이 object로 되어있으므로 숫자로 형변환 필요
df_conf_1.iloc[:,7] = df_conf_1.iloc[:,7].apply(pd.to_numeric)
# 누적확진자를 일일확진자로 변경
df_conf_1['daily_decideCnt'] = df_conf_1['decideCnt'].diff()

# 숫자여야 할 열(누적 사망자 수)이 object로 되어있으므로 숫자로 형변환
df_conf_1.iloc[:,6] = df_conf_1.iloc[:,6].apply(pd.to_numeric)
# 누적 사망자를 일일 사망자로 변경
df_conf_1['daily_deathCnt'] = df_conf_1['deathCnt'].diff()

# 숫자여야 할 열(누적검사수)이 object로 되어있으므로 숫자로 형변환 필요
df_conf_1.iloc[:,1] = df_conf_1.iloc[:,1].apply(pd.to_numeric)
# 누적검사수를 일일검사수로 변경
df_conf_1['daily_ExamCnt'] = df_conf_1['accExamCnt'].diff()

# 날짜, 확진자 수, 누적 확진자 수, 사망자 수, 누적 사망자 수, 검사자 수, 누적 검사자 수
# 1차 백신 접종자 수, 누적 1차 백신 접종자 수, 2차 백신 접종자 수, 누적 2차 백신 접종자 수
df_conf_2 = df_conf_1[['accDefRate','resutlNegCnt','stateDt','daily_decideCnt','decideCnt','daily_deathCnt','deathCnt','daily_ExamCnt','accExamCnt']]

df_conf_2.columns = ['누적 환진률','결과 음성 수','날짜','확진자 수','누적 확진자 수','사망자 수','누적 사망자 수','검사자 수','누적 검사자 수']

# 한국 데이터의 틀린 부분 수정 코드
# 공공데이터포털의 오픈API에서 불러오는 데이터에 수정이 있을 경우 삭제 가능

add_dat = pd.DataFrame({"날짜":['20200121','20200122','20200123','20200124','20200125','20200126','20200127','20200128','20200129',
                    '20200130','20200131','20200201','20200202','20200203','20200204','20200205'],
              "확진자 수":[1,0,0,1,0,1,1,0,0,2,5,1,3,0,1,3],
              "누적 확진자 수":[1,1,1,2,2,3,4,4,4,6,11,12,15,15,16,19]})

df_conf_3 = pd.concat([add_dat, df_conf_2.iloc[6:,]], ignore_index = True)
df_conf_3



with pd.ExcelWriter('./'+fileName+'.xlsx') as writer:
    df_conf_1.to_excel(writer, sheet_name = 'raw_data')
    df_conf_2.to_excel(writer, sheet_name = 'second')
    df_conf_3.to_excel(writer, sheet_name = 'final_data')
'''
