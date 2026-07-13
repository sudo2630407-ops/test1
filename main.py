import streamlit as st
import pandas as pd

st.set_page_config(page_title="도시 열섬현상 분석", layout="wide")

st.title("🌆 서울과 양평의 도시 열섬현상 분석")

# -----------------------------
# 데이터 읽기
# -----------------------------
seoul = pd.read_csv("서울_기온.csv", encoding="cp949")
yangpyeong = pd.read_csv("양평_기온.csv", encoding="cp949")

# 날짜형으로 변환
seoul["일시"] = pd.to_datetime(seoul["일시"])
yangpyeong["일시"] = pd.to_datetime(yangpyeong["일시"])

# 사용할 열만 선택
seoul = seoul[["일시", "기온(°C)"]].rename(columns={"기온(°C)": "서울"})
yangpyeong = yangpyeong[["일시", "기온(°C)"]].rename(columns={"기온(°C)": "양평"})

# 데이터 합치기
df = pd.merge(seoul, yangpyeong, on="일시")

# 기온차 계산
df["기온차"] = df["서울"] - df["양평"]

# 시각, 월 정보 추가
df["시"] = df["일시"].dt.hour
df["월"] = df["일시"].dt.month

# -----------------------------
# 1년간 기온 변화
# -----------------------------
st.header("① 1년간 서울과 양평의 기온 변화")

line_df = df.set_index("일시")[["서울", "양평"]]
st.line_chart(line_df)

# -----------------------------
# 시각별 평균 기온차
# -----------------------------
st.header("② 시각별 평균 기온차 (서울 - 양평)")

hour_diff = df.groupby("시")["기온차"].mean()

st.bar_chart(hour_diff)

# -----------------------------
# 월별 평균 기온차
# -----------------------------
st.header("③ 월별 평균 기온차 (서울 - 양평)")

month_diff = df.groupby("월")["기온차"].mean()

st.bar_chart(month_diff)

# -----------------------------
# 데이터 미리보기
# -----------------------------
with st.expander("데이터 보기"):
    st.dataframe(df)
