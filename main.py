import streamlit as st
import pandas as pd

st.set_page_config(page_title="도시 열섬현상과 전력수요 분석", layout="wide")

st.title("🌆 도시 열섬현상과 전력수요 분석")

# ==========================
# 데이터 불러오기
# ==========================
seoul = pd.read_csv("서울_기온.csv", encoding="cp949")
yang = pd.read_csv("양평_기온.csv", encoding="cp949")
power = pd.read_csv("전력수요.csv", encoding="cp949")

# 날짜형 변환
seoul["일시"] = pd.to_datetime(seoul["일시"])
yang["일시"] = pd.to_datetime(yang["일시"])
power["일시"] = pd.to_datetime(power["일시"])

# 필요한 열만 선택
seoul = seoul[["일시", "기온(°C)"]].rename(columns={"기온(°C)": "서울기온"})
yang = yang[["일시", "기온(°C)"]].rename(columns={"기온(°C)": "양평기온"})

# ==========================
# 탭 생성
# ==========================
tab1, tab2 = st.tabs(["🌆 열섬 분석", "⚡ 전력 연결"])

# ======================================================
# 탭1 : 열섬 분석
# ======================================================
with tab1:

    st.header("서울과 양평의 도시 열섬현상")

    temp = pd.merge(seoul, yang, on="일시")

    temp["기온차"] = temp["서울기온"] - temp["양평기온"]
    temp["시"] = temp["일시"].dt.hour
    temp["월"] = temp["일시"].dt.month

    # ① 선그래프
    st.subheader("① 1년간 두 지역 기온 변화")

    line_df = temp.set_index("일시")[["서울기온", "양평기온"]]
    st.line_chart(line_df)

    # ② 시각별 평균 기온차
    st.subheader("② 시각별 평균 기온차 (서울 - 양평)")

    hour_diff = temp.groupby("시")["기온차"].mean()
    st.bar_chart(hour_diff)

    # ③ 월별 평균 기온차
    st.subheader("③ 월별 평균 기온차 (서울 - 양평)")

    month_diff = temp.groupby("월")["기온차"].mean()
    st.bar_chart(month_diff)

# ======================================================
# 탭2 : 전력 연결
# ======================================================
with tab2:

    st.header("서울 기온과 전력수요의 관계")

    power_df = pd.merge(seoul, power, on="일시")

    power_df["월"] = power_df["일시"].dt.month

    # 기온 구간 생성 (5도 간격)
    bins = [-20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40]
    labels = [
        "-20~-15", "-15~-10", "-10~-5", "-5~0",
        "0~5", "5~10", "10~15", "15~20",
        "20~25", "25~30", "30~35", "35~40"
    ]

    power_df["기온구간"] = pd.cut(
        power_df["서울기온"],
        bins=bins,
        labels=labels
    )

    # ① 산점도
    st.subheader("① 기온과 전력수요의 관계")

    st.scatter_chart(
        power_df,
        x="서울기온",
        y="전력수요(MWh)"
    )

    # ② 기온 구간별 평균 전력수요
    st.subheader("② 기온 구간별 평균 전력수요")

    temp_power = power_df.groupby("기온구간")["전력수요(MWh)"].mean()
    st.bar_chart(temp_power)

    # ③ 월별 평균 전력수요
    st.subheader("③ 월별 평균 전력수요")

    month_power = power_df.groupby("월")["전력수요(MWh)"].mean()
    st.bar_chart(month_power)
