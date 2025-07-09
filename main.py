import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# 📌 사이드바 메뉴 구성
# -------------------------------
st.sidebar.title("📂 분석 페이지")
page = st.sidebar.radio("항목 선택", ["연령대별 인구 변화", "업종별 점포 수 변화", "전체 점포 수 비교"])

# ===============================
# 1. 연령대별 인구 변화
# ===============================
if page == "연령대별 인구 변화":
    st.title("📊 양주2동 연령대별 인구 변화 분석 (2008–2024)")

    csv_url = "https://raw.githubusercontent.com/jooooooong/5/main/population(in)%20(1).csv"
    try:
        df = pd.read_csv(csv_url)
    except Exception as e:
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
    st.title("🏪 양주2동 업종별 점포 수 변화 분석 (2018–2023)")

    excel_url = "https://raw.githubusercontent.com/jooooooong/5/main/%EC%A0%90%ED%8F%AC%EC%88%98(2021_4%EB%B6%84%EA%B8%B0_%EB%8F%99%EB%B6%84%EA%B8%B0_%EC%97%85%EC%A2%85%EC%A0%84%EC%B2%B4_%EC%A7%80%EC%97%AD%EB%B3%84%ED%98%84%ED%99%A9).xlsx"
    try:
        df = pd.read_excel(excel_url)
    except Exception as e:
        st.error("❌ 엑셀 파일을 불러올 수 없습니다.")
        st.stop()

    if '지역명' not in df.columns:
        st.error("❌ '지역명' 열이 없습니다.")
        st.stop()

    df = df[df['지역명'] == '양주2동']
    df.rename(columns={df.columns[0]: '연도'}, inplace=True)
    value_columns = [col for col in df.columns if col not in ['연도', '지역명']]
    df_melted = df.melt(id_vars='연도', value_vars=value_columns, var_name='업종', value_name='점포수')

    업종목록 = sorted(df_melted['업종'].unique())
    선택업종 = st.multiselect("🔍 분석할 업종:", 업종목록, default=업종목록)
    필터된 = df_melted[df_melted['업종'].isin(선택업종)]

    fig = px.line(필터된, x='연도', y='점포수', color='업종', markers=True,
                  title="📉 업종별 점포 수 변화", labels={'연도': '연도', '점포수': '점포 수'})
    st.plotly_chart(fig, use_container_width=True)

# ===============================
# 3. 전체 점포 수 비교 (수동 입력)
# ===============================
elif page == "전체 점포 수 비교":
    st.title("📍 양주2동 vs 회천4동 전체 점포 수 변화 (2018–2024)")

    # 수동 입력 데이터
    data = {
        "연도": ["2018", "2019", "2020", "2021", "2022", "2023", "2024"],
        "양주2동": [516, 556, 572, 588, 591, 610, 588],
        "회천4동": [169, 292, 426, 545, 700, 784, 846]
    }
    df = pd.DataFrame(data)

    # melt 변환
    df_melted = df.melt(id_vars="연도", var_name="행정구역", value_name="점포수")

    # 선택 UI
    선택지역 = st.multiselect("🔎 비교할 지역을 선택하세요:", df_melted['행정구역'].unique(), default=["양주2동", "회천4동"])
    df_filtered = df_melted[df_melted['행정구역'].isin(선택지역)]

    # 시각화
    fig = px.line(
        df_filtered,
        x="연도",
        y="점포수",
        color="행정구역",
        markers=True,
        title="📈 연도별 전체 점포 수 변화 비교",
        labels={'연도': '연도', '점포수': '점포 수', '행정구역': '지역'}
    )
    st.plotly_chart(fig, use_container_width=True)
