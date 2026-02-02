import streamlit as st
import pandas as pd

st.title("e-Stat 人口統計可視化アプリ")
st.caption("Streamlit標準グラフを使用した安定版です。")

file_path = "FEH_00200524_260131160542.csv"

try:
    df_raw = pd.read_csv(
        file_path, 
        skiprows=14, 
        encoding="utf-8",
        on_bad_lines='skip'
    )
    
    df_raw.columns = [str(c).replace('\n', '').strip() for c in df_raw.columns]

    df = df_raw.copy()
    df["人口（千人）"] = pd.to_numeric(df["男女計【千人】"].astype(str).str.replace(',', ''), errors='coerce')
    df["age_num"] = df["年齢各歳"].str.extract(r'(\d+)').astype(float)
    
    df = df.dropna(subset=["人口（千人）", "age_num"])
    df = df[~df["年齢各歳"].str.contains("総数|不詳", na=False)]

    years = sorted(df["時間軸（年月日現在）"].unique(), reverse=True)
    selected_year = st.sidebar.selectbox("調査年を選択", years)
    
    df_year = df[df["時間軸（年月日現在）"] == selected_year].sort_values("age_num")

    st.subheader(f"{selected_year} 年齢別人口分布")

    chart_data = df_year.set_index("年齢各歳")[["人口（千人）"]]
    st.line_chart(chart_data)

    st.write("### エリアチャート")
    st.area_chart(chart_data)

    with st.expander("詳細データ表を確認"):
        st.dataframe(df_year[["年齢各歳", "人口（千人）", "男【千人】", "女【千人】"]])

except Exception as e:
    st.error(f"エラーが発生しました: {e}")