import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 📌 1. 데이터 불러오기
# -----------------------------
# 예시 CSV: 'year', 'age_group', 'population'
df = pd.read_csv("age_population_2008_2024.csv")

# -----------------------------
# 📌 2. Streamlit UI
# -----------------------------
st.title("Population Trend by Age Group - Yangju 2-dong")

age_groups = sorted(df['age_group'].unique())

selected_groups = st.multiselect("Select age group(s):", age_groups, default=age_groups)

# -----------------------------
# 📌 3. 필터링
# -----------------------------
filtered_df = df[df['age_group'].isin(selected_groups)]

# -----------------------------
# 📌 4. 시각화 (Plotly)
# -----------------------------
fig = px.line(filtered_df, 
              x='year', 
              y='population', 
              color='age_group',
              labels={'year': 'Year', 'population': 'Population', 'age_group': 'Age Group'},
              title="Population Change by Age Group (2008–2024)")

fig.update_layout(height=500)

st.plotly_chart(fig, use_container_width=True)
