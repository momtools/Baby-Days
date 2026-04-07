import streamlit as st
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="Baby Days - 記念日リスト", layout="centered")

# --- アプリのメインタイトル（Baby Daysをさらに大きく、サブタイトルとのバランスを調整） ---
st.markdown("<h1 style='font-weight: bold; white-space: nowrap; font-size: 2.5rem;'>Baby Days <span style='font-size: 0.45em; font-weight: normal; color: #555;'>-記念日リスト-</span></h1>", unsafe_allow_html=True)
st.write("誕生日を入力すると、小学校卒業までの記念日一覧が日付順で表示されます")

# --- 注意書き（折りたたみメニュー） ---
with st.expander("記念日の計算方法"):
    st.write("""
    * **日数の数え方**: **生まれた日を1日目**として計算しています。
    * **お宮参り**: 男の子は生後31日目、女の子は生後32日目で計算しています。
    * **七五三**: 満年齢の11月15日で表示しています。一般的には男の子は5歳、女の子は3歳と7歳でお祝いしますが、地域や風習によって異なるため、本アプリでは3歳・5歳・7歳のすべてを表示しています。
    * **お祝いする日について**: 実際の行事は、赤ちゃんの体調やご家族の都合に合わせてお祝いすることが多いです。あくまで目安としてご活用ください！
    """)

# --- 入力項目 ---
name = st.text_input("ニックネームを入力（任意）")
gender = st.radio("性別を選択してください", ["男の子", "女の子"], horizontal=True)
birth = st.date_input("誕生日を入力")

if birth:
    # --- 日付計算 ---
    # 1. お七夜 (生後7日目 → +6日)
    oshichiya = birth + timedelta(days=6)
    
    # 2. お宮参り (男の子:31日目→+30日、女の子:32日目→+31日)
    omiyamairi_days = 30 if gender == "男の子" else 31
    omiyamairi = birth + timedelta(days=omiyamairi_days)
    
    # 3. 百日・1000日・ハーフ・1歳 (百日・1000日は「-1日」して計算)
    day100 = birth + timedelta(days=99)
    day1000 = birth + timedelta(days=999)
    half_birthday = birth + relativedelta(months=6)
    birthday1 = birth + relativedelta(years=1)

    # --- イベントリストの作成 ---
    events = [
        {"name": "お七夜", "date": oshichiya},
        {"name": "お宮参り", "date": omiyamairi},
        {"name": "百日祝い（お食い初め）", "date": day100},
        {"name": "ハーフバースデー", "date": half_birthday},
        {"name": "1歳", "date": birthday1},
        {"name": "1000日祝い", "date": day1000},
    ]

    # 4. 初節句 (性別によって切り替え)
    if gender == "女の子":
        hina = date(birth.year, 3, 3)
        if birth > hina:
            hina = date(birth.year + 1, 3, 3)
        events.append({"name": "初節句 (ひな祭り)", "date": hina})
    else:
        tango = date(birth.year, 5, 5)
        if birth > tango:
            tango = date(birth.year + 1, 5, 5)
        events.append({"name": "初節句 (こどもの日)", "date": tango})

    # 5. 七五三 (満年齢の11/15、地域差に配慮して3,5,7歳すべて表示)
    events.append({"name": "七五三（3歳）", "date": birth + relativedelta(years=3, month=11, day=15)})
    events.append({"name": "七五三（5歳）", "date": birth + relativedelta(years=5, month=11, day=15)})
    events.append({"name": "七五三（7歳）", "date": birth + relativedelta(years=7, month=11, day=15)})

    # 6. 小学校入学・卒業（早生まれ判定）
    if (birth.month < 4) or (birth.month == 4 and birth.day == 1):
        school_entry_year = birth.year + 6
    else:
        school_entry_year = birth.year + 7
    
    elem_entry_date = date(school_entry_year, 4, 1)
    elem_grad_date = date(school_entry_year + 6, 3, 20)

    # ドット区切りに合わせる
    events.append({"name": "小学校 入学式", "date": elem_entry_date, "display": f"{school_entry_year}.04"})
    events.append({"name": "小学校 卒業式", "date": elem_grad_date, "display": f"{school_entry_year + 6}.03"})

    # --- 並べ替えとHTML生成 ---
    events.sort(key=lambda x: x["date"])

    events_html = ""
    for ev in events:
        # ドット区切りのフォーマットに変更
        display_date = ev.get("display", ev["date"].strftime('%Y.%m.%d'))
        events_html += f'<div class="event"><span>{ev["name"]}</span><span>{display_date}</span></div>\n'

    # カード用タイトルの生成（ニックネームの有無で分岐）
    card_title = f"{name}の記念日" if name else "記念日"

    # --- CSS ---
    st.markdown("""
<style>
/* 右上の「･･･」メニューを含むヘッダー全体を非表示にする */
[data-testid="stHeader"] {
    display: none;
}

/* メニューが消えた分、上部の余白を少し詰めました */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
}

.card {
    background-color: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    margin-top: 50px; 
    margin-bottom: 40px; 
    color: #333;
}
.title {
    font-size: 20px;
    text-align: center;
    margin-top: 5px;   
    margin-bottom: 25px; 
    letter-spacing: 1px;
    font-weight: bold;
}
.event {
    display: flex;
    justify-content: space-between;
    padding: 8px 0; 
    font-size: 14px;
}
.event span:last-child {
    font-weight: bold;
    color: #555;
}
/* Expanderの見た目調整 */
.streamlit-expanderHeader {
    font-size: 14px;
    color: #555;
}
</style>
    """, unsafe_allow_html=True)

    # --- 表示 ---
    st.markdown(f"""
<div class="card">
<div class="title">{card_title}</div>
{events_html}
</div>
    """, unsafe_allow_html=True)