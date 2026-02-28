import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Commission",
    page_icon="💎",
    layout="wide"
)


USERS = {
    "Somwang": "0944542994",
    "Thari": "0955405556",
    "user2": "pass2"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔒 เข้าสู่ระบบ")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("เข้าสู่ระบบ"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username  # ถ้าอยากเก็บชื่อ user
            st.rerun()
        else:
            st.error("Username หรือ Password ไม่ถูกต้อง")

else:
    st.title(f"สวัสดี {st.session_state.username}")
    st.switch_page("pages/commission.py")
    # วางโค้ดคำนวณทั้งหมดตรงนี


# ต่อจากส่วน else: ด้านบน (ส่วนที่แสดงแอป)
st.sidebar.title("ตัวเลือก")
if st.sidebar.button("ออกจากระบบ"):
    st.session_state.logged_in = False
    st.rerun()

