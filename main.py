import pandas as pd
import streamlit as st
#import는 전부 가져오기
#import crawling as cr
#from은 일부만 가져오기
from crawling import crawling_saramin,crawling_work24,download_to_csv

if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame()
df = st.session_state['df']

#레이아웃
#헤더
st.set_page_config(page_title="채용공고 자동 크롤링 서비스",
                   layout='wide')

st.title("채용 공고 조회 서비스")
st.write(""" 이 서비스는 """)


site_select = st.radio ("크롤링할 사이트 선택",
                        ["사람인","고용24"],
                        horizontal=True)

#with st.expander("열어보세요",expanded=True):
#    st.write("확장")
with st.expander("상세 검색 조건"):
    #여기서 두개로 쪼개는 역할
    col1,col2 = st.columns(2)

    with col1:
        st.success('컬럼 1')
        search_text=st.text_input("검색어를 입력",
                                  placeholder="예 : 파이썬, 인공지능")
        
        st.success('컬럼 2')
        except_text=st.text_input("제외할 검색어",
                                    placeholder="예 : 야간 근무, 출장")

        max_pages = st.number_input('크롤링 페이지 수',
                                    max_value=10,
                                    min_value=1)

                        
    

    with col2:
        if site_select == '사람인':
            #사람인 사이트에서 지역 의미하는 코드
            loc_options = {
                "전체": None,
                "서울": "101000",
                "경기": "102000",
                "인천": "108000",
                "부산": "106000",
                "대구": "104000",
                "광주": "103000",
                "대전": "105000"
            }
            #딕셔너리 형상인 옵션에서 KEY만 추출해서 리스트로 만들기
            selected_location=st.multiselect('지역을 선택하세요',
                           list(loc_options.keys()),
                           default=['전체'])
            
            #st.write(selected_location)
            #크롤링 진행할때 사용하기 위해서 문자열 추출 0:"전체" 1:"서울" 2:" 인천" 바로 사용을 못함 101000 식으로 나와야하니까

            locations = [loc_options[x] for x in selected_location if loc_options[x]]
            #st.write(locations)
            #이걸 하면 101000 식으로 나오게 됨
            # x 는 서울 경기 부산같은 지역명
            # if 조건 붙는 이유 지역명이 없는 지역이라면 추가 안됨

            #직무 검색
            cat_options = {
                "전체": None,
                "IT개발·데이터": "2",
                "경영·사무": "3",
                "마케팅·홍보": "4",
                "디자인": "9",
                "영업": "5"
            }

            selected_category = st.multiselect("직무를 선택하세요.",
                                               list(cat_options.keys()),
                                               default=['IT개발·데이터'])
            
            category = [cat_options[x] for x in selected_category if cat_options[x]]

            #경력
            career_option = {'전체':'0','신입':'1','경력':'2','신입/경력':'3',}
            selected_career = st.selectbox('경력을 선택하세요',list(career_option.keys()))
            career = career_option[selected_career]
            #st.write(career)

            #학력
            edu_option = {'전체':'0','고졸':'1','대졸(2,3년)':'2','대졸(4년)':'3','석사':'4','박사':'5'}
            selected_edu = st.selectbox("학력을 선택하시오",list(edu_option.keys()))
            edu = edu_option[selected_edu]

        else:
             #지역, 직무,경력,학력
             region = st.text_input('지역 코드를 입력하세요',value='11000',
                                    help='지역 코드 알 수 없는 관계로 서울로 제한')
             
             ocupation = st.text_input('직종 코드를 입력하세요',value='024',
                                       help='직종 코드 제한')
             
             career_options = {"전체": "A", "신입": "N", "경력": "E", "관계없음": "Z"}
             edu_options = {"전체": "noEdu", "중졸이하": "01,02", "고졸": "03", "대졸(2~3년)": "04", "대졸(4년)": "05", "석사": "06", "박사": "07", "학력무관": "00"}
             career = st.selectbox("경력을 선택하세요",list(career_options.keys()))
             career = career_options[career]
             edu = st.selectbox("학력을 선택하세요",list(edu_options.keys()))
             edu = edu_options[edu]

#st.button(버튼에 들어갈 글자,) '크기 조절 옵션'
crwaling_clicked = st.button("크롤링 시작",
                             use_container_width=True,
                             type='primary')

#crwaling_clicked -> true 버튼을 눌렀음 / False 버튼을 누르지 않음
if crwaling_clicked:
    st.write('버튼을 누름')
else:
    st.write('버튼을 안누름')

#크롤링 시행!!
#1.크롤링 한 결과를 어떻게 받아올 것인가?
#df = 
#2.크롤링 하는동안 어떻게 안내할 것인가?

if crwaling_clicked :
    #2-1 검색어나 필수요소가 누락된경우 안내
    #검색어가 없다
    if not search_text:
        st.warning('검색어를 입력해주세요!')
    #2-2 크롤링 시행하는 동안 기다려주세요 안내
    else:
        with st.spinner(f"{site_select}에서{search_text}검색 결과 가져오는 중..."):
            if site_select == '사람인':
                #사람인 크롤링 함수
                df= crawling_saramin(search_text = search_text, 
                                        except_text = except_text,
                                        region = locations, 
                                        category = category,
                                        career = career,
                                        education = edu,
                                        max_pages = max_pages)


            else:
                #고용24 크롤링 함수
                df = crawling_work24(search_text = search_text, 
                                    except_text = except_text,
                                    region = region, 
                                    category = ocupation,
                                    career = career,
                                    education = edu,
                                    max_pages = max_pages)
                    
    #st.session_state['df'] = df
# #st.session_state가 뭘까?
# #화면을 랜더링 할때에도 df의 정보를 기억하도록 만들어 줌 
# #session_state는 '딕셔너리' 처럼 저장
# #session_state['df']
# df['expection] = df.expection
#df = st.session_state['df']
st.write(df)

if not df.empty:
    st.subheader('검색결과')
    st.dataframe(df,
                 width='stretch',
                 hide_index=True)

    csv_data = download_to_csv(df)
    st.download_button(label= 'CSV 결과 다운로드',
                       data = csv_data,
                       file_name= f'crawling_results_{site_select}.csv',
                       mime='text/csv')

# if 'df' not in st.session_state:
#     st.session_state['df'] = pd.DataFrame()