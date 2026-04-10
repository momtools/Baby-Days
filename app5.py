import streamlit as st
import json
import logic
import ui

# --- 1. 設定の読み込み (config.jsonから) ---
with open('config.json', 'r', encoding='utf-8') as f:
    conf = json.load(f)

# --- 2. ページ設定と共通デザイン ---
st.set_page_config(page_title=f"{conf['app_title']} {conf['app_subtitle']}", layout="centered")

ui.apply_css()
ui.render_header(conf['app_title'], conf['app_subtitle'], conf['description'])

with st.expander(conf['expander_title']):
    st.write(conf['expander_text'])

# --- 3. 入力受け付け ---
name = st.text_input(conf['input_name_label'])
gender = st.radio(conf['input_gender_label'], ["男の子", "女の子"], horizontal=True)
birth = st.date_input(conf['input_birth_label'])

# --- 4. 計算(logic.py) と 表示(ui.py) ---
if birth:
    # logic.pyに計算を丸投げ
    events = logic.calculate_milestones(birth, gender)
    
    # ui.pyに結果表示を丸投げ
    ui.render_result_card(name, events, conf['footer_text'])