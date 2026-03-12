import streamlit as st
import pandas as pd

# ซ่อน sidebar ในหน้านี้เท่านั้น
st.markdown("""
    <style>
        /* ซ่อน sidebar ทั้งหมด */
        section[data-testid="stSidebar"] { 
            display: none !important; 
        }
        /* ซ่อน navigation links */
        [data-testid="stSidebarNav"] { 
            display: none !important; 
        }
        /* ซ่อน page menu */
        div[data-testid="stSidebarNav"] > div { 
            display: none !important; 
        }
    </style>
""", unsafe_allow_html=True)

# Login form ของคุณ
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

st.set_page_config(initial_sidebar_state="collapsed")

st.set_page_config(
    page_title="Commission",
    page_icon="💎",
    layout="wide"
)


USERS = {
    "admin": "123456*",
    "Somwang": "0944542994",
    "Tharinee": "0955405556",
    "Chutipa": "0963544236",
    "Jittima":"0968625565",
    "Thanapon":"0842465935",
    "Charinthip":"0829514536",
    "Namoun":"0886774449",
    "Areewan":"0967193456",
    "Maneewan":"0815914236",
    "Kitti": "0972456459",
    "Khanittha ":"0990834923",
    "Darawan":"0929242899",
    "Panisara":"0946592445",
    "Kriangkrai":"0635199969",
    "Sumintra ":"0949655693",
    "Surachet":"0949644423",
    "Jittra":"0963566592",
    "Siriya": "0875569928",
    "Namphueng":"0626965495",
    "Wanwisa":"0886966512",
    "Nathawat ":"0619295978",
    "Kriangkrai":"0635199969",
    "Khanittayada":"0971565697",
    "Narin":"0925495655",
    "Thawatchai":"0925495655",
    "Jiraporn":"0868293697",
    "Ponphan":"0822282526",
    "Chatphat": "0814536195",
    "Chalothon":"0993619241",
    "Preecha":"0993619241",
    "Waruth ":"0952464692",
    "Natthawat":"0959199455",
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

