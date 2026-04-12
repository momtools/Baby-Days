import streamlit as st

def apply_css():
    """白ベース×グレー×くすみピンクの洗練されたデザイン"""
    st.markdown("""
    <style>
    /* 1. アプリ全体の背景を完全な白に */
    .stApp { background-color: #FFFFFF !important; }

    /* 2. 基本の文字色を真っ黒ではなく、上品なダークグレーに */
    .stApp p, .stApp div, .stApp label, .stApp .stMarkdown { 
        color: #4A4A4A !important; 
        font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', sans-serif;
    }

    /* 不要なパーツを隠す */
    [data-testid="stHeader"], header, footer, [data-testid="stToolbar"] { 
        display: none !important; visibility: hidden !important; 
    }

    /* 画面幅を少し狭めて、よりWebサイトっぽく（中央寄せ） */
    .block-container { 
        padding-top: 3rem !important; 
        padding-bottom: 1rem !important;
        max-width: 600px !important;
    }

    /* 3. タイトルのデザイン（細字で余白を多く） */
    .main-title {
        text-align: center;
        font-size: 26px;
        font-weight: 300; 
        letter-spacing: 2px;
        color: #333333;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        font-size: 12px;
        color: #999999; 
        letter-spacing: 2px;
        margin-bottom: 30px;
    }

    /* 4. 結果カード */
    .card { 
        background-color: #FFFFFF !important; 
        padding: 20px; 
        border: 1px solid #EAEAEA; 
        border-radius: 8px; 
        margin-top: 20px; 
        margin-bottom: 30px; 
    }

    /* 5. 行事リスト */
    .event { 
        display: flex; 
        justify-content: space-between; 
        padding: 8px 0; 
        font-size: 14px; 
        border-bottom: 1px dashed #F0F0F0; 
    }
    .event:last-child { border-bottom: none; } 
    .event span { font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', sans-serif; }
    .event span:first-child { color: #666666 !important; }
    .event span:last-child { 
        font-weight: 500; 
        color: #D6A4A4 !important; 
    }

    /* 6. 入力ボックス */
    div[data-testid="stTextInput"] div[data-baseweb="base-input"], 
    div[data-testid="stDateInput"] div[data-baseweb="base-input"] { 
        background-color: #FAFAFA !important; 
        border: 1px solid #E5E5E5 !important; 
        border-radius: 6px !important; 
    }
    
    div[data-testid="stTextInput"] div[data-baseweb="base-input"]:focus-within, 
    div[data-testid="stDateInput"] div[data-baseweb="base-input"]:focus-within { 
        border-color: #D6A4A4 !important; 
        box-shadow: 0 0 0 1px #D6A4A4 !important;
    }

    div[data-testid="stTextInput"] input, 
    div[data-testid="stDateInput"] input {
        background-color: transparent !important;
        color: #4A4A4A !important;
    }
    
    /* 7. ラジオボタン（選択ドット）の色 */
    
    /* ★最強・確実に効くやつ */
input[type="radio"]:checked {
    accent-color: #D6A4A4;
}
    /* 選択されている時の外枠（円） */
    div[data-testid="stRadio"] label[aria-checked="true"] > div:first-of-type {
        border-color: #D6A4A4 !important;
    }

    /* 選択されている時の中のポチ */
    div[data-testid="stRadio"] label[aria-checked="true"] > div:first-of-type > div {
        background-color: #D6A4A4 !important;
    }

    /* 選択されていない時の外枠も少し整える（任意） */
    div[data-testid="stRadio"] label[aria-checked="false"] > div:first-of-type {
        border-color: #E5E5E5 !important;
    }

    /* 選択中のテキストを太字にする（視認性アップ） */
    div[data-testid="stRadio"] label[aria-checked="true"] div[data-testid="stMarkdownContainer"] p {
        font-weight: bold !important;
        color: #4A4A4A !important;
    }


    /* 【最後の手段】カレンダーアイコンの背景ブロックを強制的に透明化 */
    div[data-testid="stDateInput"] div[data-baseweb="base-input"] > div:last-child {
        background-color: transparent !important;
        border: none !important;
    }
    
    /* エクスパンダー（折りたたみメニュー）をシンプルに */
    .streamlit-expanderHeader p { color: #888888 !important; font-size: 14px; }
    
    </style>
    """, unsafe_allow_html=True)

def render_header(title, subtitle, description):
    """洗練されたヘッダー"""
    st.markdown(f"""
        <div class="main-title">{title}</div>
        <div class="sub-title">{subtitle}</div>
    """, unsafe_allow_html=True)
    # 【修正】誕生日を入力すると～表示されます。は左寄せに変更済み
    st.markdown(f"<p style='text-align: left; font-size: 13px; color: #777; margin-bottom: 30px;'>{description}</p>", unsafe_allow_html=True)

def render_result_card(name, events, footer_text):
    """シンプルでおしゃれな結果表示カード"""
    card_title = f"{name}の記念日" if name else "記念日"
    
    events_html = ""
    for ev in events:
        display_date = ev.get("display", ev["date"].strftime('%Y.%m.%d'))
        events_html += f'<div class="event"><span>{ev["name"]}</span><span>{display_date}</span></div>\n'
    
    # 【修正】閉じタグの出力をピンポイントで修正しました
    st.markdown(f"""
<div class="card">
    <div style="text-align: center; font-size: 16px; font-weight: bold; color: #555555; margin-bottom: 20px; letter-spacing: 1px;">
        {card_title}
    </div>
    {events_html}
</div>
""", unsafe_allow_html=True)
    
    # ここに単独の </div> タグの出力がないことを確認しました

    # フッター表示
    st.markdown(f"<div style='text-align: center; font-size: 10px; color: #CCCCCC; margin-top: -10px; margin-bottom: 40px; letter-spacing: 1px;'>{footer_text}</div>", unsafe_allow_html=True)
