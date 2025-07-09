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
# 2. GitHub Raw CSV 파일 경로
# -------------------------------
csv_url = "https://raw.githubusercontent.com/jooooooong/5/main/population(in)%20(1).csv"

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

# '가로형 데이터'를 '세로형(long-form)'으로 변환
df_melted = df.melt(id_vars='연도', var_name='연령대', value_name='인구수')

# 쉼표 제거하고 숫자로 변환
df_melted['인구수'] = df_melted['인구수'].astype(str).str.replace(',', '').astype(int)

# -------------------------------
# 5. 사용자 선택 UI
# -------------------------------
연령대목록 = sorted(df_melted['연령대'].unique())
선택연령대 = st.multiselect("🔎 분석할 연령대를 선택하세요:", 연령대목록, default=연령대목록)

# -------------------------------
# 6. 시각화
# -------------------------------
필터된데이터 = df_melted[df_melted['연령대'].isin(선택연령대)]

fig = px.line(
    필터된데이터,
    x='연도',
    y='인구수',
    color='연령대',
    markers=True,
    labels={'연도': '연도', '인구수': '인구 수', '연령대': '연령대'},
    title="📈 연령대별 인구 변화 추이 (2008–2024)"
)
fig.update_layout(height=550, xaxis=dict(dtick=1))

st.plotly_chart(fig, use_container_width=True)

#2
st.title("🏪 양주2동 업종별 점포 수 변화 분석 (2018–2023)")

st.markdown("""
이 웹앱은 GitHub에 저장된 엑셀 데이터를 불러와  
양주2동의 연도별 업종별 점포 수 변화를 시각적으로 보여줍니다.
""")

# ✅ GitHub에서 바로 읽는 Raw Excel URL
excel_url = "https://raw.githubusercontent.com/jooooooong/5/main/%EC%A0%90%ED%8F%AC%EC%88%98(2021_4%EB%B6%84%EA%B8%B0_%EB%8F%99%EB%B6%84%EA%B8%B0_%EC%97%85%EC%A2%85%EC%A0%84%EC%B2%B4_%EC%A7%80%EC%97%AD%EB%B3%84%ED%98%84%ED%99%A9).xlsx"

try:
    df = pd.read_excel(excel_url)
except Exception as e:
    st.error("❌ 엑셀 파일을 불러올 수 없습니다. URL 또는 파일 구조를 확인하세요.")
    st.stop()

# -------------------------------
# 1. 양주2동 필터링
# -------------------------------
if '지역명' not in df.columns:
    st.error("❌ '지역명' 열이 존재하지 않습니다. 엑셀 열 구조를 확인해주세요.")
    st.stop()

df = df[df['지역명'] == '양주2동']

# 2. 첫 번째 열 → '연도'로 이름 바꾸기
df.rename(columns={df.columns[0]: '연도'}, inplace=True)

# 3. '연도' 외 모든 열 중 '지역명' 제외하고 melt
value_columns = [col for col in df.columns if col not in ['연도', '지역명']]
df_melted = df.melt(id_vars='연도', value_vars=value_columns, var_name='업종', value_name='점포수')

# 4. 업종 선택 UI
업종목록 = sorted(df_melted['업종'].unique())
선택업종 = st.multiselect("🔍 분석할 업종을 선택하세요:", 업종목록, default=업종목록)

# 5. 필터링
필터된 = df_melted[df_melted['업종'].isin(선택업종)]

# 6. 시각화
fig = px.line(
    필터된,
    x='연도',
    y='점포수',
    color='업종',
    markers=True,
    labels={'연도': '연도', '점포수': '점포 수', '업종': '업종'},
    title="📉 양주2동 업종별 점포 수 변화 추이"
)
fig.update_layout(height=550, xaxis=dict(dtick=1))
st.plotly_chart(fig, use_container_width=True)
