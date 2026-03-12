import streamlit as st
import pandas as pd
import time
import datetime
import os

# ซ่อน sidebar navigation ทั้งหมด
st.markdown("""
    <style>
        /* ซ่อน sidebar navigation */
        .css-1d391kg {
            display: none !important;
        }
        /* ซ่อน page links ใน sidebar */
        .css-1v3f3lc {
            display: none !important;
        }
        /* ซ่อน header main/commission */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(initial_sidebar_state="collapsed")

st.set_page_config(
    page_title="Commission_campaign",
    page_icon="💰",
    layout="wide"
)

# ✅ ไฟล์กลาง เก็บทุกคน
HISTORY_FILE = "all_users_login.csv"

def log_user_login(username):
    """บันทึกการ login ของทุกคนลง CSV กลาง"""
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE, encoding='utf-8-sig')
    else:
        df = pd.DataFrame(columns=["วันที่", "ผู้ใช้"])
    
    # เช็คว่ามีการ login ซ้ำใน 10 นาทีล่าสุดหรือไม่
    now = datetime.datetime.now()
    recent = df[
        (df["ผู้ใช้"] == username) & 
        (pd.to_datetime(df["วันที่"]).dt.date == now.date()) &
        ((now - pd.to_datetime(df["วันที่"])).dt.total_seconds() < 300)
    ]
    
    if recent.empty:
        new_entry = pd.DataFrame({
            "วันที่": [now.strftime("%Y-%m-%d %H:%M:%S")],
            "ผู้ใช้": [username],
            
        })
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(HISTORY_FILE, index=False, encoding='utf-8-sig')
        st.sidebar.success(f"✅ บันทึก {username} แล้ว")

def get_all_users():
    """อ่านข้อมูลทุกคนจาก CSV"""
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE, encoding='utf-8-sig')
    return pd.DataFrame()


INACTIVITY_TIMEOUT_SECONDS = 10 * 60

def update_last_activity():
    st.session_state.last_activity = time.time()

def is_timed_out():
    now = time.time()
    last = st.session_state.get("last_activity", now)
    return (now - last) > INACTIVITY_TIMEOUT_SECONDS

# ✅ ใช้ไฟล์กลางแทน session_state
if "logged_in" in st.session_state and st.session_state.logged_in:
    current_user = st.session_state.get("username", "Unknown")
    log_user_login(current_user)  # บันทึกทุกคนอัตโนมัติ


if "last_activity" not in st.session_state:
    st.session_state.last_activity = time.time()

# ถ้าไม่มีกิจกรรม 10 นาที ให้ล็อกเอาต์อัตโนมัติ
if is_timed_out():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.clear()
    st.info("⚠️ หมดเวลาไม่มีการใช้งาน 10 นาที กรุณาล็อกอินใหม่")
    time.sleep(1)
    st.switch_page("main.py")

if not st.session_state.get("logged_in", False):
    st.warning("⚠️ กรุณาล็อกอินก่อนใช้งาน")
    st.stop()  # หยุดการรัน ไม่ให้ไปต่อ


st.title("💰Commission_Campaign")

#กำหนด campaign
campaign_value = {
    "Extra comm": 20,
    "Student comn": 15, 
    "Flash sales": 30,
    "TVS Now": 5
}

#กำหนด Basic comm
Basic_comm = {
    "AP1D>150-199/SIM": 15,
    "AP1D>200-249/SIM": 20,
    "AP1D>250-299/SIM": 30,
    "AP1D>300-499/SIM": 35,
    "AP1D>500/SIM": 42
}

flash_sale = {
    "AP1D>200-249/SIM": 25,
    "AP1D>250-299/SIM": 30,
    "AP1D>300/SIM": 40,
}
# 1. ตั้งค่าเริ่มต้นทุกอย่างให้ 0
total_commission = 0
total_commission_student = 0
total_commission_tvs = 0
total_commission_basic = 0
total_commission_flash = 0



st.divider()

# Step 1: Basic_comm Input (เพิ่ม key)
st.subheader("1. 🔢 Basic Commission")
col2, col3, col4, col5 = st.columns(4)
inputs_basic = {}

with col2:
    inputs_basic["AP1D>200-249/SIM"] = st.number_input("AP1D>200-249", value=0, step=1, key="input_basic_200")
with col3:
    inputs_basic["AP1D>250-299/SIM"] = st.number_input("AP1D>250-299", value=0, step=1, key="input_basic_250")
with col4:
    inputs_basic["AP1D>300-499/SIM"] = st.number_input("AP1D>300-499", value=0, step=1, key="input_basic_300")
with col5:
    inputs_basic["AP1D>500/SIM"] = st.number_input("AP1D>500", value=0, step=1, key="input_basic_500")

st.divider()

# Basic Commission Calculation
results_basic = []
total_sim_basic = 0
total_commission_basic = 0  # แก้ชื่อตัวแปร

for category, sim_count in inputs_basic.items():
    if sim_count > 0:
        commission_rate = Basic_comm[category]
        commission = sim_count * commission_rate
        total_sim_basic += sim_count
        total_commission_basic += commission  # แก้ไข

        results_basic.append({
            "Campaign": category,
            "SIMs": sim_count,
            "Rate": f"{commission_rate:,.0f} บาท/SIM",
            "Commission": f"{commission:,.0f} บาท"
        })

# แสดง Basic Commission
if results_basic:
    df_basic = pd.DataFrame(results_basic)
    st.dataframe(df_basic, width="stretch",hide_index=True)
    
else:
    st.info("กรุณาใส่จำนวน SIM เพื่อดูผลรวม Basic")

st.divider()

# ฟังก์ชันคำนวณอัตราคอมมิชชั่นตามเงื่อนไข
def get_commission_rate(sim_count, price_category):
    """
    คำนวณอัตราคอมมิชชั่นตามปริมาณ SIM และช่วงราคา
    
    price_category: '200-249', '250-299', '300-349', '350+'
    """
    if 5 <= sim_count <= 19:
        rates = {'200-249': 0, '250-299': 15, '300-349': 30, '350+': 30}
    elif 20 <= sim_count <= 29:
        rates = {'200-249': 10, '250-299': 15, '300-349': 30, '350+': 30}
    elif 30 <= sim_count <= 89:  # แก้ไขจาก 30-89
        rates = {'200-249': 15, '250-299': 20, '300-349': 30, '350+': 35}
    elif 90 <= sim_count <= 199:
        rates = {'200-249': 20, '250-299': 30, '300-349': 45, '350+': 50}
    elif 200 <= sim_count <= 499:
        rates = {'200-249': 25, '250-299': 30, '300-349': 45, '350+': 50}
    elif 500 <= sim_count <= 899:
        rates = {'200-249': 25, '250-299': 40, '300-349': 60, '350+': 70}
    elif sim_count >= 900:
        rates = {'200-249': 20, '250-299': 40, '300-349': 60, '350+': 75}
    else:
        rates = {'200-249': 0, '250-299': 0, '300-349': 0, '350+': 0}
    
    return rates.get(price_category, 0)

st.subheader("2. 🏪 Extra Commission")

price_inputs = {
    "200-249": 0,
    "250-299": 0,
    "300-349": 0,
    "350+": 0
}


# Mapping ช่วง SIM → ค่าใช้คำนวณอัตรา (เหมือนเดิม)
sim_ranges = {
    "5-19": 12,
    "20-29": 25,
    "30-89": 50,
    "90-199": 120,
    "200-499": 300,
    "500-899": 600,
    "900+": 1000,
}

# ตัวเลือกช่วง
sim_choices = [
    "5-19", "20-29", "30-89", "90-199", "200-499", "500-899", "900+"
]

selected_ranges = st.multiselect(
    "เลือกเป้าหมาย SIM",
    sim_choices,
    default=["5-19"],  # ตั้ง default ให้ช่องดูสมบูรณ์
    key="sim_multi"
)

st.subheader("💰 ใส่จำนวนตามช่วงราคา(AP1D)")
price_cols = st.columns(4)
price_inputs = {}
with price_cols[0]:
    price_inputs["200-249"] = st.number_input("AP1D>200-249 บาท", min_value=0, value=0, step=1, key="price_200")
with price_cols[1]:
    price_inputs["250-299"] = st.number_input("AP1D>250-299 บาท", min_value=0, value=0, step=1, key="price_250")
with price_cols[2]:
    price_inputs["300-349"] = st.number_input("AP1D300-349 บาท", min_value=0, value=0, step=1, key="price_300")
with price_cols[3]:
    price_inputs["350+"] = st.number_input("AP1D350+ บาท", min_value=0, value=0, step=1, key="price_350")

st.divider()

# ตัวอย่างการใช้ selected_ranges ไปคำนวณ commission
results_extra = []
total_sim = 0
total_commission = 0

for selected in selected_ranges:
    sim_count_for_rate = sim_ranges[selected]  # ใช้ค่าจาก mapping สำหรับเลือกอัตรา

    for price_cat, price_qty in price_inputs.items():
        if price_qty > 0:
            extra_rate = get_commission_rate(sim_count_for_rate, price_cat)
            commission = price_qty * extra_rate
            total_sim += sim_count_for_rate * price_qty
            total_commission += commission

            results_extra.append({
                "ช่วง SIM": selected,
                "ช่วงราคา": price_cat,
                "จำนวน SIM": f"{price_qty:,}",
                "อัตรา": f"{extra_rate}",
                "คอม/ช่วง": f"{commission:,.0f} บาท"
            })

# แสดงผลตาราง
if results_extra:
    df_general = pd.DataFrame(results_extra)
    st.dataframe(df_general, width="stretch", hide_index=True)
else:
    st.warning("⚠️ กรุณาเลือกช่วงปริมาณ SIM และกรอกจำนวนช่วงราคาเพื่อคำนวณ")


st.divider()

# Step 3 Flash sales Input (แก้ไข)
st.subheader("3. 🎯 Flash Sales ")
col11, col12, col13 = st.columns(3)
inputs_flash = {}


with col11:
    inputs_flash["AP1D>200-249/SIM"] = st.number_input("AP1D>200-249", value=0, step=1, key="input_flash_200")
with col12:
    inputs_flash["AP1D>250-299/SIM"] = st.number_input("AP1D>250-299", value=0, step=1, key="input_flash_250")
with col13:
    inputs_flash["AP1D>300/SIM"] = st.number_input("AP1D>300-499", value=0, step=1, key="input_flash_300")


st.divider()

# Flash sales Calculation (แก้ไข)
results_flash = []
total_sim_flash = 0
total_commission_flash = 0

for category, sim_count in inputs_flash.items():
    if sim_count > 0:
        # Flash rate = 30 บาท/SIM สำหรับทุก category
        flash_rate = flash_sale[category]
        flash_comm = sim_count * flash_rate
        total_sim_flash += sim_count
        total_commission_flash += flash_comm

        results_flash.append({
            "Campaign": "Flash Sales",
            "SIMs": sim_count,
            "Rate": f"{flash_rate:,.0f} บาท/SIM",
            "Commission": f"{flash_comm:,.0f} บาท"
        })

# แสดง Flash Results
if results_flash:
    df_flash= pd.DataFrame(results_flash)
    
    st.dataframe(df_flash, width="stretch",hide_index=True)
    
    
else:
    st.info("กรุณาใส่จำนวน SIM Flash Sales เพื่อดูผลรวม")

#step 4 : Student comm
st.subheader("4. 🎓 Student")
col17, col18 = st.columns([20, 1])  # แก้ syntax columns
inputs_student = {}

with col17:
    inputs_student["AP1D>200-249/SIM"] = st.number_input(
        "AP1D>200-249/SIM", 
        value=0, 
        step=1, 
        min_value=0,
        help="ใส่จำนวน SIM Student ราคา 200-249 บาท",
        key="input_student_200"
    )

st.divider()

# ตัวแปรเริ่มต้น (สำคัญ!)
total_commission_student = 0
total_sim_student = 0

# Student Calculation (ย้ายเข้า if)
results_student = []
if inputs_student["AP1D>200-249/SIM"] > 0:
    sim_count = inputs_student["AP1D>200-249/SIM"]
    student_rate = 15  # บาทต่อ SIM
    student_comm = sim_count * student_rate
    total_sim_student = sim_count
    total_commission_student = student_comm

    results_student.append({
        "Campaign": "Student Comm",  # แก้ typo "capaign"
        "SIMs": sim_count,
        "Rate": f"{student_rate} บาท/SIM",
        "Commission": f"{student_comm:,.0f} บาท"
    })

    df_student = pd.DataFrame(results_student)
    st.dataframe(df_student, width="stretch", hide_index=True)
     
else:
    st.info("กรุณาใส่จำนวน SIM Student เพื่อดูผลรวม")
    total_commission_student = 0  # สำหรับสรุปรวม


st.divider()

st.subheader("5. 📺 TVS Now")
col_tvs1 = st.columns(1)[0]
with col_tvs1:
    if 'inputs_tvs' not in locals():
        inputs_tvs = {}
    inputs_tvs["AP1D>300-499/SIM"] = st.number_input(
        "AP1D>300-499/SIM",
        min_value=0,
        value=0,
        step=1,
        key="input_tvs_300_499"
    )

st.divider()

if inputs_tvs["AP1D>300-499/SIM"] > 0:
    tvs_qty = inputs_tvs["AP1D>300-499/SIM"]
    tvs_commission = tvs_qty * 5
    total_commission_tvs = tvs_commission  # ✅ อัปเดตค่า

    tvs_data = [{
        "Campaign": "TVS Now",
        "SIMs": tvs_qty,
        "Rate": "5 บาท/SIM",
        "Commission": f"{total_commission_tvs:,.0f} บาท"
    }]
    df_tvs = pd.DataFrame(tvs_data)
    st.dataframe(df_tvs, width="stretch", hide_index=True)

else:
    st.info("กรุณาใส่จำนวน SIM TVS เพื่อดูผลรวม")
    # ไม่ต้องทำอะไร เพราะ total_commission_tvs ถูกตั้งค่าไว้แล้ว = 0

st.divider()


# ใช้ตัวเลขจริงใน df_summary
summary_data = {
    "Campaign": ["Extra comm", "Student comm", "TVS Now", "Basic comm", "Flash sales"],
    "Commission": [
        total_commission,
        total_commission_student, 
        total_commission_tvs,
        total_commission_basic,
        total_commission_flash
    ]
}

df_summary = pd.DataFrame(summary_data)

# แยก “Total row” สำหรับการแสดงผล
total_all = df_summary["Commission"].sum()

# ถ้าจะใช้ display ให้สวย → ทำเป็น DataFrame ใหม่สำหรับแสดงอย่างเดียว
df_display = df_summary.copy()
df_display["Commission"] = df_display["Commission"].map("{:,.0f}".format)

# เพิ่ม Total แบบแสดงผล (เฉพาะหน้า UI)
df_display.loc[len(df_display)] = ["**รวมทั้งหมด**", f"**{total_all:,.0f}**"]

st.subheader("💎 สรุปรวม")
st.dataframe(df_display, width="stretch", hide_index=True)


st.divider()

# ฟังก์ชันคำนวณแต้ม (แก้ docstring)
def get_point_rate(sim_count, point_category):
    """
    คำนวณแต้มโบนัสต่อ SIM ตามปริมาณและช่วงราคา
    
    point_category: '150-199', '200-249', '250-299', '300+'
    """
    if 5 <= sim_count <= 20:
        rates = {'150-199': 10, '200-249': 60, '250-299': 80, '300+': 90}
    elif 21 <= sim_count <= 50:
        rates = {'150-199': 10, '200-249': 80, '250-299': 100, '300+': 110}
    elif 51 <= sim_count <= 100:
        rates = {'150-199': 10, '200-249': 100, '250-299': 120, '300+': 130}
    elif 101 <= sim_count <= 300:
        rates = {'150-199': 10, '200-249': 120, '250-299': 140, '300+': 150}
    elif sim_count >= 301:
        rates = {'150-199': 10, '200-249': 140, '250-299': 160, '300+': 170}
    else:
        rates = {'150-199': 0, '200-249': 0, '250-299': 0, '300+': 0}
    
    return rates.get(point_category, 0)

st.subheader("👉POINT+")

# Mapping ช่วง → ค่ากลางที่แก้ไขแล้ว
point_ranges_corrected = {
    "5-20": 12,      # (5+20)/2 = 12.5
    "21-50": 36,     # (21+50)/2 = 35.5
    "51-100": 76,    # (51+100)/2 = 75.5
    "101-300": 201,  # (101+300)/2 = 200.5
    "300+": 300      # ขอบล่าง
}

point_choices = ["5-20", "21-50", "51-100", "101-300", "300+"]  # แก้ "301>" เป็น "300+"

selected_point_ranges = st.multiselect(
    "เลือกเป้าหมาย SIM",
    point_choices,
    default=["5-20"],
    key="point_multi"  # key ไม่ซ้ำ
)

st.subheader("💰 ใส่จำนวนตามช่วงราคา(AP1D)")
point_cols = st.columns(4)
point_inputs = {}
with point_cols[0]:
    point_inputs["150-199"] = st.number_input("AP1D>150-199", min_value=0, value=0, step=1, key="point_price_150")
with point_cols[1]:
    point_inputs["200-249"] = st.number_input("AP1D>200-249", min_value=0, value=0, step=1, key="point_price_200")
with point_cols[2]:
    point_inputs["250-299"] = st.number_input("AP1D250-299", min_value=0, value=0, step=1, key="point_price_250")
with point_cols[3]:
    point_inputs["300+"] = st.number_input("AP1D300+", min_value=0, value=0, step=1, key="point_price_300")


# ✅ แก้ไข: ตัวแปรเฉพาะสำหรับ Point+ (ไม่ใช้ selected_ranges จาก Extra Commission)
results_point = []
total_point_sim = 0
total_points = 0

for selected in selected_point_ranges:
    sim_count_for_rate = point_ranges_corrected[selected]
    
    for price_cat, qty in point_inputs.items():
        if qty > 0:
            point_rate = get_point_rate(sim_count_for_rate, price_cat)  # ใช้ get_point_rate
            points = qty * point_rate  # แต้ม = จำนวน × อัตราแต้ม
            total_point_sim += sim_count_for_rate * qty
            total_points += points
            
            results_point.append({
                "ช่วง SIM": selected,
                "ช่วงราคา": price_cat,
                "จำนวน": f"{qty:,}",
                "แต้ม/SIM": f"{point_rate}",
                "รวมแต้ม": f"{points:,.0f}"
            })

if results_point:
    # SIM จริงที่ขายได้
    total_actual_sim = sum(point_inputs.values())
    df_point = pd.DataFrame(results_point)
    st.dataframe(df_point, width="stretch", hide_index=True)
    
    # ค่าตัวแทนทั้งหมด (สำหรับ tier)
    total_tier_sim = sum(point_ranges_corrected[selected] for selected in selected_point_ranges)
    
    col1,  col3 = st.columns(2)
    col1.metric("SIM ขายจริง", f"{total_actual_sim:,} SIM")
    col3.metric("รวมแต้ม", f"{total_points:,.0f} POINT")

st.divider()

st.subheader("🏪>MOU")

# Rates สำหรับแต่ละเป้าหมาย
rate_commission1 = {
    "200-299": 25,
    "300-399": 30,
    "400-499": 35,
    ">500": 40
}

rate_commission3 = {
    "600-899": 25,
    "900-1199": 30,
    "1200-1499": 35,
    ">1500": 40
}

choice_sim = st.selectbox("เลือกเป้าหมาย",
                          ("1 MONTH", "3 MONTH"),
                          index=1,
                          key="choice_sim")

# Dynamic options และ rates
if choice_sim == "1 MONTH":
    sim_options = ["200-299", "300-399", "400-499", ">500"]
    rates = rate_commission1
    default_sim = ["200-299"]
else:
    sim_options = ["600-899", "900-1199", "1200-1499", ">1500"]
    rates = rate_commission3
    default_sim = ["600-899"]

select_range = st.multiselect(
    "เลือกเป้าหมาย SIM",
    sim_options,
    default=default_sim,
    key="sim"
)

st.divider()

# แสดงผลที่เลือก
col10, col20 = st.columns(2)
with col10:
    st.subheader(f"เป้าหมาย:red[ {choice_sim}]")
with col20:
    st.subheader(f"ช่วง SIM:red[ {', '.join(select_range) if select_range else 'ไม่มี'}]")

st.divider()

# คำนวณ commission
if select_range:
    col1, col2 = st.columns([2, 1])
    with col1:
        # Default ตาม choice_sim
        default_count = 600 if choice_sim == "3 MONTH" else 200
        
        sim_count = st.number_input(
            "จำนวน SIM ทั้งหมด", 
            min_value=0, 
            value=default_count,  # ← เปลี่ยนตรงนี้
            key="sim_count"
        )

    with col2:
        st.info("**อัตรา/ช่วง:**")
        for sim in select_range:
            st.caption(f"{sim}:red[ {rates[sim]} บ/:ซิม]")
    
    # คำนวณจริงด้วย rates
    commission_per_range = {sim: rates[sim] * sim_count for sim in select_range}
    total_commission = sum(commission_per_range.values())
    
    # แสดงตาราง breakdown
    df_breakdown = pd.DataFrame(list(commission_per_range.items()), columns=["ช่วง SIM", "คอมรวม"])
    st.dataframe(df_breakdown, width="stretch",hide_index=True)
    
    st.metric("คอมมิชชั่นรวม", f"{total_commission:,.0f} บาท")
    
else:
    st.warning("กรุณาเลือกช่วง SIM")


st.divider()

if st.button("🗑️ เคลียร์ข้อมูลทั้งหมด", use_container_width=True):
    # Clear ทุก input ในแอป
    prefixes_to_clear = [
        "input_", "sim_", "price_", "point_price_", "input_student", 
        "input_tvs", "input_basic", "input_flash", "point_input",
        "choice_sim", "sim_multi", "point_multi"  # ✅ เพิ่ม MOU keys
    ]
    
    for key in list(st.session_state.keys()):
        if any(prefix in key for prefix in prefixes_to_clear):
            del st.session_state[key]
    
    # Reset ค่า total ทุกตัว
    totals_to_reset = [
        "total_commission", "total_commission_student", "total_commission_tvs",
        "total_commission_basic", "total_commission_flash", "total_points"
    ]
    for total_key in totals_to_reset:
        st.session_state[total_key] = 0
    
    st.success("✅ เคลียร์ข้อมูลทั้งหมดเรียบร้อย!")
    st.rerun()



st.divider()

st.sidebar.title("👥")

# แสดงข้อมูลทั้งหมด
df_all = get_all_users()
if not df_all.empty:
    df_all["วันที่"] = pd.to_datetime(df_all["วันที่"])
    df_today = df_all[df_all["วันที่"].dt.date == datetime.datetime.now().date()]
    

    st.sidebar.metric("ผู้ใช้ทั้งหมด", len(df_all["ผู้ใช้"].unique()))
    st.sidebar.metric("Login วันนี้", len(df_today))
    
    
    # ดาวน์โหลด
    csv_data = df_all.to_csv(index=False, encoding='utf-8-sig')
    st.sidebar.download_button(
        label="💾 ประวัติการเข้าใช้งาน",
        data=csv_data,
        file_name="all_users_history.csv",
        mime="text/csv"
    )
else:
    st.sidebar.info("ยังไม่มีใคร login")

if st.sidebar.button("ออกจากระบบ"):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.switch_page("main.py")

