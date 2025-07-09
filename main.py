import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 📌 제목 및 설명
# -----------------------------
st.title("📊 양주2동 연령대별 인구 변화 분석 (2008–2024)")
st.markdown("""
이 그래프는 양주2동의 연도별 인구 구조 변화를 연령대 기준으로 보여줍니다.  
아래에서 원하는 연령대를 선택하면, 해당 인구의 시간 흐름에 따른 증감을 확인할 수 있습니다.
""")

# -----------------------------
# 📂 CSV 파일 불러오기
# 파일명은 반드시 동일하게 유지하거나, 아래 경로 수정
# -----------------------------
df = pd.read_csv("population_in.csv")

# -----------------------------
# 🔍 데이터 기본 구조 확인
# 필요한 경우 컬럼 이름 확인 및 정제
# 예: 컬럼명이 '년도', '연령대', '인구수' 등이라면 아래처럼 수정
# df.columns = ['year', 'age_group', 'population']
# -----------------------------
df.columns = ['year', 'age_group', 'population']  # 필요 시 수정

# -----------------------------
# ✅ 사용자 선택 UI: 연령대 선택
# -----------------------------
age_groups = sorted(df['age_group'].unique())

selected_ages = st.multiselect(
    "🔎 분석할 연령대를 선택하세요:",
    age_groups,
    default=age_groups  # 기본은 전체 선택
)

# -----------------------------
# 📌 필터링
# -----------------------------
filtered_df = df[df['age_group'].isin(selected_ages)]

# -----------------------------
# 📈 시각화 (Plotly 라인 차트)
# -----------------------------
fig = px.line(
    filtered_df,
    x='year',
    y='population',
    color='age_group',
    markers=True,
    labels={
        'year': '연도',
        'population': '인구 수',
        'age_group': '연령대'
    },
    title="연령대별 인구 변화 추이 (2008–2024)"
)

fig.update_layout(
    height=550,
    xaxis=dict(dtick=1),
    legend_title_text='연령대'
)

st.plotly_chart(fig, use_container_width=True)
