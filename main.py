import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 양주2동 연령대별 인구 변화 분석 (2008–2024)")
st.markdown("""
데이터를 업로드하면, 연령대별 인구 변화 추이를 그래프로 확인할 수 있습니다.
""")

uploaded_file = st.file_uploader("📂 CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    # 1. CSV 불러오기
    df = pd.read_csv(uploaded_file)

    # 2. 첫 열(Unnamed: 0)을 '연도'로 이름 바꾸기
    df.rename(columns={df.columns[0]: '연도'}, inplace=True)

    # 3. 가로형 데이터를 세로형으로 변환 (melt)
    df_melted = df.melt(id_vars='연도', var_name='연령대', value_name='인구수')

    # 4. 문자열 숫자 제거 (예: "1,234" → 1234)
    df_melted['인구수'] = df_melted['인구수'].astype(str).str.replace(',', '').astype(int)

    # 5. 연령대 목록 정렬
    연령대목록 = sorted(df_melted['연령대'].unique())
    선택연령대 = st.multiselect("🔎 분석할 연령대를 선택하세요:", 연령대목록, default=연령대목록)

    # 6. 필터링
    필터된데이터 = df_melted[df_melted['연령대'].isin(선택연령대)]

    # 7. 시각화
    fig = px.line(
        필터된데이터,
        x='연도',
        y='인구수',
        color='연령대',
        markers=True,
        labels={'연도': '연도', '인구수': '인구 수', '연령대': '연령대'},
        title="📈 연령대별 인구 변화 추이"
    )
    fig.update_layout(height=550, xaxis=dict(dtick=1), legend_title_text='연령대')

    st.plotly_chart(fig, use_container_width=True)
