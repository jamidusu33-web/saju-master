
import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar
from datetime import datetime

st.set_page_config(page_title="AI 사주명리 상담소", page_icon="🔮")

st.title("AI 사주명리 상담소 🔮")

# 천간과 지지 정의
HEAVENLY_STEMS = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
EARTHLY_BRANCHES = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# 만세력 계산 함수
def calculate_saju(year, month, day, hour):
    base_date = datetime(1900, 1, 1)
    target_date = datetime(year, month, day)
    delta_days = (target_date - base_date).days
    
    day_stem = HEAVENLY_STEMS[(delta_days + 6) % 10]
    day_branch = EARTHLY_BRANCHES[(delta_days + 8) % 12]
    day_pillar = day_stem + day_branch
    
    year_stem = HEAVENLY_STEMS[(year - 4) % 10]
    year_branch = EARTHLY_BRANCHES[(year - 4) % 12]
    year_pillar = year_stem + year_branch
    
    month_stem = HEAVENLY_STEMS[(year * 2 + month) % 10]
    month_branch = EARTHLY_BRANCHES[(month + 1) % 12]
    month_pillar = month_stem + month_branch
    
    hour_branch_idx = (hour + 1) // 2 % 12
    hour_branch = EARTHLY_BRANCHES[hour_branch_idx]
    hour_stem = HEAVENLY_STEMS[(delta_days * 2 + hour_branch_idx) % 10]
    hour_pillar = hour_stem + hour_branch
    
    return year_pillar, month_pillar, day_pillar, hour_pillar

with st.form("saju_form"):
    st.write("생년월일시를 입력해 주세요.")
    
    calendar_type = st.radio("달력 기준", ["양력", "음력"], horizontal=True)
    
    is_leap_month = False
    if calendar_type == "음력":
        is_leap_month = st.checkbox("윤달입니까?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.number_input("태어난 연도", min_value=1920, max_value=2026, value=1956)
    with col2:
        month = st.number_input("월", min_value=1, max_value=12, value=12)
    with col3:
        day = st.number_input("일", min_value=1, max_value=31, value=31)
        
    st.markdown("---")
    st.write("태어난 시간을 선택해 주세요.")
    col_hour, col_min = st.columns(2)
    with col_hour:
        hour = st.selectbox("시간 (시)", list(range(24)), index=18, format_func=lambda x: f"{x:02d}시")
    with col_min:
        minute = st.selectbox("분", list(range(60)), format_func=lambda x: f"{x:02d}분")

    submit_button = st.form_submit_button("사주 분석 시작하기")

if submit_button:
    solar_year, solar_month, solar_day = year, month, day
    if calendar_type == "음력":
        try:
            cal = KoreanLunarCalendar()
            cal.setLunarDate(year, month, day, is_leap_month)
            solar_year = cal.getSolarYear()
            solar_month = cal.getSolarMonth()
            solar_day = cal.getSolarDay()
        except Exception as e:
            st.error(f"음력 변환 중 오류가 발생했습니다: {e}")

    y_p, m_p, d_p, h_p = calculate_saju(solar_year, solar_month, solar_day, hour)
    
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
        
    st.info("사주팔자 산출이 완료되었습니다. 다음 단계에서 AI 상세 해설 기능을 붙여보겠습니다!")
