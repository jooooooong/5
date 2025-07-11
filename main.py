import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# 📂 사이드바 메뉴 구성
# -------------------------------
st.sidebar.title("📂 분석 페이지")
page = st.sidebar.radio("항목 선택", ["연령대별 인구 변화", "업종별 점포 수 변화", "소비 분석 및 전략 제안"])

# ===============================
# 1. 연령대별 인구 변화
# ===============================
if page == "연령대별 인구 변화":
    st.title("📊 양주2동 연령대별 인구 변화 분석 (2008–2024)")

    csv_url = "https://raw.githubusercontent.com/jooooooong/5/main/population(in)%20(1).csv?raw=true"
    try:
        df = pd.read_csv(csv_url)
    except:
        st.error("❌ CSV 파일을 불러올 수 없습니다.")
        st.stop()

    df.rename(columns={df.columns[0]: '연도'}, inplace=True)
    df_melted = df.melt(id_vars='연도', var_name='연령대', value_name='인구수')
    df_melted['인구수'] = df_melted['인구수'].astype(str).str.replace(',', '').astype(int)

    연령대목록 = sorted(df_melted['연령대'].unique())
    선택연령대 = st.multiselect("🔎 분석할 연령대를 선택하세요:", 연령대목록, default=연령대목록)
    필터된 = df_melted[df_melted['연령대'].isin(선택연령대)]

    fig = px.line(필터된, x='연도', y='인구수', color='연령대', markers=True,
                  title="📈 연령대별 인구 변화 추이", labels={'연도': '연도', '인구수': '인구 수'})
    st.plotly_chart(fig, use_container_width=True)

# ===============================
# 2. 업종별 점포 수 변화
# ===============================
elif page == "업종별 점포 수 변화":
    st.title("🏪 양주2동 전체 점포 수 변화 (2018–2023)")

    df = pd.DataFrame({
        "연도": [2018, 2019, 2020, 2021, 2022, 2023],
        "전체점포수": [516, 556, 572, 588, 591, 610]
    })

    fig = px.bar(df, x='연도', y='전체점포수', text='전체점포수',
                 title="양주2동 전체 점포 수 추이", labels={'전체점포수': '점포 수'})
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

# ===============================
# 3. 소비 분석 및 전략 제안
# ===============================
elif page == "소비 분석 및 전략 제안":
    st.title("💸 연령대별 소비 특성과 회복 전략")

    # 인구 구성비 변화
    st.subheader("📈 연령대별 인구 구성비 변화 (2008 → 2024)")
    pop_data = {
        "연령대": ["유아·아동층 (0~14세)", "청소년층 (15~19세)", "청년층 (20~34세)", "중년층 (35~54세)", "장년층 (55~64세)", "노년층 (65세 이상)"],
        "2008": [25.20, 4.33, 21.49, 33.81, 7.69, 7.48],
        "2024": [12.30, 6.61, 15.99, 31.90, 14.73, 18.47]
    }
    df_pop = pd.DataFrame(pop_data)
    df_melted = df_pop.melt(id_vars="연령대", var_name="연도", value_name="구성비")

    fig = px.bar(df_melted, x="연령대", y="구성비", color="연도",
                 barmode="group", title="연령대별 인구 구성비 변화 (%)")
    st.plotly_chart(fig, use_container_width=True)

    # 소비 데이터
    st.subheader("🛍️ 연령대별 업종 소비 금액 (단위: 억원)")
    df_consume = pd.DataFrame({
        "연령대": ["20대", "30대", "40대", "50대", "60대"],
        "종합소매점": [0.83, 1.95, 4.47, 5.11, 2.92],
        "한식": [0.41, 1.34, 2.41, 2.68, 1.49],
        "연료판매": [0.71, 2.17, 4.17, 4.48, 2.38],
        "가전제품": [0.62, None, 1.99, None, 1.10],
        "음/식료품소매": [None, 0.77, 2.12, 2.60, 1.89],
        "일반병원": [None, None, None, 1.54, None]
    }).fillna(0)
    df_c = df_consume.melt(id_vars="연령대", var_name="업종", value_name="소비금액(억원)")

    fig2 = px.bar(df_c, x="업종", y="소비금액(억원)", color="연령대", barmode="group")
    fig2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)

    # 전략 제안
    st.subheader("✅ 회복 전략 요약")

    st.markdown("""
    - **👴 증가한 연령층:** 장년층, 노년층 → 건강, 필수소비, 편의시설 업종 확대 필요  
    - **👶 감소한 연령층:** 유아, 청년층 → 교육, 놀이시설, 청년트렌드 업종 축소 우려  
    - **추천 업종:**  
        - 병원, 약국, 실버카페, 경로당, 건강식품점  
        - 편의점, 음식점(한식), 대형마트  
        - 공공 도서관, 복합문화공간, 교통 접근성 강화
    """)
