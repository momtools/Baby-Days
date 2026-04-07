import streamlit as st
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

# --- ページ設定（タイトルの横にアイコンを出すなど） ---
st.set_page_config(page_title="Baby Days - 記念日リスト", layout="centered")

st.markdown("""
<style>

/* アプリ全体 */
.stApp {
    background-color: #F8F9FA !important;
}

/* 文字色 */
.stApp p, .stApp span, .stApp h1, .stApp div, .stApp label, .stApp .stMarkdown {
    color: #333333 !important;
}

.stApp [data-testid="stMarkdownContainer"] p {
    color: #333333 !important;
}

/* ヘッダー非表示 */
[data-testid="stHeader"] {
    display: none;
}

header {
    display: none !important;
}

/* 余白 */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
}

/* カード */
.card {
    background-color: #ffffff !important;
    padding: 20px 25px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    margin-top: 30px; 
    margin-bottom: 40px; 
}

/* タイトル */
.title {
    font-size: 20px;
    text-align: center;
    margin-top: 5px;   
    margin-bottom: 30px;
    letter-spacing: 1px;
    font-weight: bold;
    color: #333333 !important;
}

/* イベント */
.event {
    display: flex;
    justify-content: space-between;
    padding: 10px 0; 
    font-size: 14px;
}

.event span:last-child {
    font-weight: bold;
    color: #555555 !important;
}

/* expander */
.streamlit-expanderHeader {
    color: #555555 !important;
    background-color: transparent !important;
}

/* ===== ここからが今回の本命 ===== */

/* 右下のUI消す */
[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

div[data-testid="stStatusWidget"] {
    display: none !important;
}

/* フッター完全抑制 */
footer {
    visibility: hidden !important;
    height: 0px !important;
}

/* クレジット */
.css-164nlkn {
    display: none !important;
}

</style>
""", unsafe_allow_html=True)

# --- アプリのメインタイトル ---
st.markdown("<h1 style='font-weight: bold; white-space: nowrap; font-size: 2.5rem; color: #333;'>Baby Days <span style='font-size: 0.45em; font-weight: normal; color: #555;'>-記念日リスト-</span></h1>", unsafe_allow_html=True)
st.write("誕生日を入力すると、小学校卒業までの記念日一覧が表示されます")

# --- 注意書き（折りたたみメニュー） ---
with st.expander("記念日の計算方法"):
    st.write("""
    * **日数の数え方**: **生まれた日を1日目**として計算しています。
    * **お宮参り**: 男の子は生後31日目、女の子は生後32日目で計算しています。
    * **七五三**: 満年齢の11月15日で表示しています。一般的には男の子は5歳、女の子は3歳と7歳でお祝いしますが、地域や風習によって異なるため、本アプリでは3歳・5歳・7歳のすべてを表示しています。
    * **お祝いする日について**: 実際の行事は、赤ちゃんの体調やご家族の都合に合わせてお祝いすることが多いです。
    """)

# --- 入力項目 ---
name = st.text_input("ニックネームを入力（任意）")
gender = st.radio("性別を選択してください", ["男の子", "女の子"], horizontal=True)
birth = st.date_input("誕生日を入力")

if birth:
    # --- 日付計算ロジック ---
    oshichiya = birth + timedelta(days=6)
    omiyamairi_days = 30 if gender == "男の子" else 31
    omiyamairi = birth + timedelta(days=omiyamairi_days)
    day100 = birth + timedelta(days=99)
    day1000 = birth + timedelta(days=999)
    half_birthday = birth + relativedelta(months=6)
    birthday1 = birth + relativedelta(years=1)

    events = [
        {"name": "お七夜", "date": oshichiya},
        {"name": "お宮参り", "date": omiyamairi},
        {"name": "百日祝い（お食い初め）", "date": day100},
        {"name": "ハーフバースデー", "date": half_birthday},
        {"name": "1歳", "date": birthday1},
        {"name": "1000日祝い", "date": day1000},
    ]

    # 初節句
    if gender == "女の子":
        hina = date(birth.year, 3, 3)
        if birth > hina: hina = date(birth.year + 1, 3, 3)
        events.append({"name": "初節句 (ひな祭り)", "date": hina})
    else:
        tango = date(birth.year, 5, 5)
        if birth > tango: tango = date(birth.year + 1, 5, 5)
        events.append({"name": "初節句 (こどもの日)", "date": tango})

    # 七五三
    events.append({"name": "七五三（3歳）", "date": birth + relativedelta(years=3, month=11, day=15)})
    events.append({"name": "七五三（5歳）", "date": birth + relativedelta(years=5, month=11, day=15)})
    events.append({"name": "七五三（7歳）", "date": birth + relativedelta(years=7, month=11, day=15)})

    # 小学校
    if (birth.month < 4) or (birth.month == 4 and birth.day == 1):
        school_entry_year = birth.year + 6
    else:
        school_entry_year = birth.year + 7
    
    events.append({"name": "小学校 入学", "date": date(school_entry_year, 4, 1), "display": f"{school_entry_year}.04"})
    events.append({"name": "小学校 卒業", "date": date(school_entry_year + 6, 3, 20), "display": f"{school_entry_year + 6}.03"})

    # --- 並べ替えと表示 ---
    events.sort(key=lambda x: x["date"])

    events_html = ""
    for ev in events:
        display_date = ev.get("display", ev["date"].strftime('%Y.%m.%d'))
        events_html += f'<div class="event"><span>{ev["name"]}</span><span>{display_date}</span></div>\n'

    card_title = f"{name}の記念日リスト" if name else "記念日リスト"

    # --- HTML表示 ---
    st.markdown(f"""
    <div class="card">
        <div class="title">{card_title}</div>
        {events_html}
    </div>
    """, unsafe_allow_html=True)
