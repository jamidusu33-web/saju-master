import streamlit as st

st.set_page_config(page_title="AI 사주명리 상담소", page_icon="🔮")

st.title("AI 사주명리 상담소 🔮")

with st.form("saju_form"):
    st.write("생년월일시를 입력해 주세요.")
    
    # 양력/음력 선택 기능
    calendar_type = st.radio("달력 기준", ["양력", "음력"], horizontal=True)
    
    # 음력을 선택했을 때만 윤달 체크박스 표시
    is_leap_month = False
    if calendar_type == "음력":
        is_leap_month = st.checkbox("윤달입니까?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.number_input("태어난 연도", min_value=1920, max_value=2026, value=1980)
    with col2:
        month = st.number_input("월", min_value=1, max_value=12, value=1)
    with col3:
        day = st.number_input("일", min_value=1, max_value=31, value=1)
        
    submit_button = st.form_submit_button("사주 분석 시작하기")

if submit_button:
    leap_text = "(윤달)" if is_leap_month else ""
    st.success(f"입력하신 정보: {year}년 {month}월 {day}일 [{calendar_type}{leap_text}]")
    st.info("여기에 만세력 엔진이 양력 변환 및 사주팔자를 연산한 결과가 나타나게 됩니다.")
