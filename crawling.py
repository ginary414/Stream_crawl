import requests                 #html요청
from bs4 import BeautifulSoup   #html을 파싱
import pandas as pd
import re



# #타입을 :타입 해주고 뒤에 = 하면거기서부터는 디폴트값
# def crawling_saramin(search_text:str,
#                      except_key:str = '',
#                      region:list = None,
#                      category:list = None,
#                      career:str = '',
#                      education:str = '',
#                      max_pages:int =1):

#     #결과로 변환할 데이터 프레임의 '열 이름'과 '행' 리스트
#     columns = ['이름','위치','조건1','조건2','회사이름','링크']
#     rows = []


#     url= "https://www.saramin.co.kr/zf_user/search"


#     headers = {
#             "User-Agent": (
#                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                 "AppleWebKit/537.36 (KHTML, like Gecko) "
#                 "Chrome/126.0.0.0 Safari/537.36"
#             ),
#             "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
#     }

#     #검색조건 키는 웹사이트가 지정한 키
#     parameters = {'searchword':search_text,
#                   'except_read':except_key,
#                   'comp_page':max_pages}
#     #직무
#     if category:
#         parameters['cat_mcd'] = category
#     #위치
#     if region:
#         parameters['loc_mcd'] = region
#     #경력
#     if career:
#         parameters['career_cd'] = career
#     #학력
#     if education:
#         parameters['edu_cd'] = education
    
#     response= requests.get(url=url,
#                  headers=headers,
#                  params=parameters,
#                  timeout=15)


#     #크롤링 결과를 response로 받고,
#     #response안에 있는 text 파일을 'html.parser' 로 파싱
#     #객체 soup를 생성
#     soup = BeautifulSoup(response.text,'html.parser')

#     #내가 필요한 결과의 구분자 전달 및 추출
#     #soup.select(구분자 ) : 구분자를 보유한 모든 내용
#     #soup.select_one(구분자) : 구분자를 보유한 내용 딱 하나
#     items = soup.select('div.item_recruit')
#     #items안에 엄청 정보가 많음 제목부터 내용등등 그래서 for문으로 분리
#     for item in items:
#         job_area = item.select_one('div.area_job')
#         corp_area = item.select_one('div.area_corp')

#         #직무정보가 없을경우
#         if not job_area :
#             #한칸의 정보가 없을때는 이번에만 넘어가자
#             continue

#         #직무, 회사정보 get
#         job_title = job_area.select_one('.job_tit').get_text(strip=True)
#         condition_area = job_area.select_one('.job_condition')
#         spans = condition_area.select('span')
#         #span 상위에서 가져오는것도 방법

#         location =spans[0].get_text(strip=True)
#         condition1 =spans[1].get_text(strip=True)
#         #condition2 =spans[-1].get_text(strip=True)

#         job_sector = item.select_one('div.job_sector')
#         condition2 = job_sector.get_text(strip=True)

#         #회사정보
#         cor_name = corp_area.select_one('.cor_name').get_text(strip=True)

#         #링크
#         link = job_area.select_one('.job_tit').select_one('.data_layer[href]')
#         real_link = 'https://www.saramin.co.kr/' +link.get('href')

#         rows.append({
#             '이름':job_title,
#             '위치':location,
#             '조건1':condition1,
#             '조건2':condition2,
#             '회사이름':cor_name,
#             '링크':real_link
#         })


#     df= pd.DataFrame(rows)
#     print(df)
#     return "사람인결과"

# def crawling_work24():
#     return "고용24결과"




def crawling_work24(search_text:str,
                     except_key:str = '',
                     region:list = None,
                     category:list = None,
                     career:str = '',
                     education:str = '',
                     max_pages:int =1):
    
    url = 'https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do'     
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }

    parameters = {'srcKeyword':search_text,
                  'notSrcKeyword':except_key,
                  'pageIndex':max_pages,
                  'resultCnt':10,
                  'occupation':region,
                  'careerTypes':"",
                  'academicGbnoEdu':""}
    
    response = requests.get(url,
                            headers=headers,
                            params=parameters,
                            timeout=15)

    soup = BeautifulSoup(response.text,
                         'html.parser')

    items = soup.select('div.box_table_group.gap_box08.column')
    items_2 = soup.select('td.link.pd24')
    
    #a 왼쪽박스
    #b 오른쪽박스
    for a,b in zip (items,items_2):
        #이름 위치 조건1 조건2 회사이름 링크
        cells = a.select('div.cell')

        name = cells[1].get_text(strip=True)

        location = cells[0].get_text(strip=True)

        money = b.select_one('span.item.b1_sb').get_text(strip=True)
        money = re.sub(r'\s+', '', money)

        work_time = b.select_one('li.time')
        if len(work_time) >=1:
            for i in range(len(work_time)):
                t+= work_time.select('span')

        crop_name = 

        link = 

##########################################################################
    #     # 1. 반복 단위(공고)를 먼저 잡습니다.
    # rows = soup.select('tr[id^="list"]') 

    # for row in rows:
    #     # 1. 태그 추출
    #     title_element = row.select_one('a.t3_sb.underline_hover')
    #     salary_element = row.select_one('span.item.b1_sb')
        
    #     # 2. 제목이 있을 때만 로직 실행 (들여쓰기 중요!)
    #     if title_element:
    #         title = title_element.get_text(strip=True)
            
    #         # 3. 급여 정제 로직을 여기서 바로 수행
    #         if salary_element:
    #             raw_salary = salary_element.get_text()
    #             salary = re.sub(r'\s+', '', raw_salary) # 정규표현식으로 깔끔하게!
    #         else:
    #             salary = "정보 없음"
            
    #         print(f"공고: {title} | 급여: {salary}")
#########################################################################
    return "고용24결과"

if __name__ == '__main__':
    #crawling_saramin("빅데이터")
    crawling_work24('AI')