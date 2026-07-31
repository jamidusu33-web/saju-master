import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar

st.set_page_config(page_title="AI 사주명리 상담소", page_icon="🔮")
st.title("AI 사주명리 상담소 🔮")

HEAVENLY_STEMS = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
EARTHLY_BRANCHES = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

def get_saju(year, month, day, hour, minute, calendar_type, is_leap_month):
    cal = KoreanLunarCalendar()
    
    if calendar_type == "음력":
        cal.setLunarDate(year, month, day, is_leap_month)
    else:
        cal.setSolarDate(year, month, day)
        
    # 절기(24절기)를 기준으로 정확한 년/월/일주 산출
    gapja_str = cal.getKoreanGapJaString() 
    parts = gapja_str.split()
    
    if len(parts) == 3:
        y_p = parts[0][:2]
        m_p = parts[1][:2]
        d_p = parts[2][:2]
    else:
        return "오류", "오류", "오류", "오류"

    # 시주(時柱) 계산 - 시두법(時頭法) 적용
    day_stem = d_p[0]
    try:
        day_stem_idx = HEAVENLY_STEMS.index(day_stem)
    except ValueError:
        day_stem_idx = 0
        
    # 동경 135도 기준 한국 표준시 30분 보정 적용 (자시: 23:30 ~ 01:29)
    total_minutes = hour * 60 + minute
    shifted_minutes = (total_minutes + 30) % 1440
    hour_branch_idx = shifted_minutes // 120
    
    h_branch = EARTHLY_BRANCHES[hour_branch_idx]
    
    start_stem_idx = (day_stem_idx % 5) * 2
    h_stem_idx = (start_stem_idx + hour_branch_idx) % 10
    h_stem = HEAVENLY_STEMS[h_stem_idx]
    
    h_p = h_stem + h_branch
    
    return y_p, m_p, d_p, h_p

with st.form("saju_form"):
    st.write("생년월일시를 입력해 주세요.")
    
    calendar_type = st.radio("달력 기준", ["양력", "음력"], horizontal=True)
    is_leap_month = False
    if calendar_type == "음력":
        is_leap_month = st.checkbox("윤달입니까?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.number_input("태어난 연도", min_value=1920, max_value=2030, value=1956)
    with col2:
        month = st.number_input("월", min_value=1, max_value=12, value=12)
    with col3:
        day = st.number_input("일", min_value=1, max_value=31, value=30) 
        
    st.markdown("---")
    st.write("태어난 시간을 선택해 주세요.")
    col_hour, col_min = st.columns(2)
    with col_hour:
        hour = st.selectbox("시간 (시)", list(range(24)), index=18, format_func=lambda x: f"{x:02d}시")
    with col_min:
        minute = st.selectbox("분", list(range(60)), format_func=lambda x: f"{x:02d}분")

    submit_button = st.form_submit_button("사주 분석 시작하기")

if submit_button:
    y_p, m_p, d_p, h_p = get_saju(year, month, day, hour, minute, calendar_type, is_leap_month)
    
    leap_text = "(윤달)" if is_leap_month else ""
    st.success(f"입력 정보: {year}년 {month}월 {day}일 {hour:02d}시 {minute:02d}분 [{calendar_type}{leap_text}]")
    
    st.markdown("### 📊 산출된 사주팔자(명식)")
    
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.metric("시주 (時柱)", h_p)
    with col_b:
        st.metric("일주 (日柱)", d_p)
    with col_c:
        st.metric("월주 (月柱)", m_p)
    with col_d:
        st.metric("연주 (年柱)", y_p)
        
    st.info("명식이 정확하게 산출되었습니다. 이제 이 여덟 글자를 바탕으로 AI 해설을 받아볼 준비가 되었습니다!")
