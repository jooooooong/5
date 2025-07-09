import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 양주2동 연령대별 인구 변화 분석 (2008–2024)")
st.markdown("""
이 그래프는 양주2동의 연도별 인구 구조 변화를 연령대 기준으로 보여줍니다.  
원하는 연령대를 선택하면, 해당 인구의 시간 흐름에 따른 증감을 확인할 수 있습니다.
""")

# 파일 업로드
uploaded_file = st.file_uploader("📂 CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    # CSV 파일 읽기 (한글 컬럼명 그대로 유지)
    df = pd.read_csv(uploaded_file)

    # 데이터 확인
    st.write("✅ 데이터 미리보기", df.head())
    st.write("📌 열 이름:", df.columns)

    # 사용자 선택: 연령대 선택
    연령대목록 = sorted(df['연령대'].unique())
    선택연령대 = st.multiselect("🔎 분석할 연령대를 선택하세요:", 연령대목록, default=연령대목록)

    # 필터링
    필터된데이터 = df[df['연령대'].isin(선택연령대)]

    # 시각화
    fig = px.line(
        필터된데이터,
        x='연도',
        y='인구수',
        color='연령대',
        markers=True,
        labels={'연도': '연도', '인구수': '인구 수', '연령대': '연령대'},
        title="📈 연령대별 인구 변화 추이"
    )
    fig.update_layout(
        height=550,
        xaxis=dict(dtick=1),
        legend_title_text='연령대'
    )

    st.plotly_chart(fig, use_container_width=True)
