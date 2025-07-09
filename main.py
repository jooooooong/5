import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# 1. 페이지 제목 및 설명
# -------------------------------
st.title("📊 양주2동 연령대별 인구 변화 분석 (2008–2024)")

st.markdown("""
이 웹앱은 GitHub에 저장된 데이터를 이용하여  
양주2동의 연령대별 인구 구조 변화를 시각적으로 분석합니다.
""")

# -------------------------------
# 2. GitHub CSV 파일 경로
# 📌 아래 URL을 본인의 GitHub 파일에 맞게 수정하세요
# -------------------------------
csv_url = "https://raw.githubusercontent.com/your-username/your-repo/main/data/population(in)%20(1).csv"

# -------------------------------
# 3. 데이터 불러오기
# -------------------------------
try:
    df = pd.read_csv(csv_url)
except Exception as e:
    st.error("❌ CSV 파일을 불러올 수 없습니다. URL을 확인하세요.")
    st.stop()

# -------------------------------
# 4. 데이터 전처리
# -------------------------------
# 첫 번째 열 이름이 보통 'Unnamed: 0' → '연도'로 바꿔주기
df.rename(columns={df.columns[0]: '연도'}, inplace=True)

# '가로형 데이터'를 '세로형 데이터'로 변환
df_melted = df.melt(id_vars='연도', var_name='연령대', value_name='인구수')

# 쉼표 제거 및 숫자형 변환
df_melted['인구수'] = df_melted['인구수'].astype(str).str.replace(',', '').astype(int)

# -------------------------------
# 5. 연령대 선택 UI
# -------------------------------
연령대목록 = sorted(df_melted['연령대'].unique())

선택연령대 = st.multiselect(
    "🔎 분석할 연령대를 선택하세요:",
    연령대목록,
    default=연령대목록
)

# 선택된 연령대만 필터링
필터된데이터 = df_melted[df_melted['연령대'].isin(선택연령대)]

# -------------------------------
# 6. 시각화 (Plotly Line Chart)
# -------------------------------
fig = px.line(
    필터된데이터,
    x='연도',
    y='인구수',
    color='연령대',
    markers=True,
    labels={'연도': '연도', '인구수': '인구 수', '연령대': '연령대'},
    title="📈 연령대별 인구 변화 추이 (2008–2024)"
)

fig.update_layout(height=550, xaxis=dict(dtick=1), legend_title_text='연령대')

st.plotly_chart(fig, use_container_width=True)
