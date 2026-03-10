import streamlit as st
import pandas as pd
import time

st.set_page_config(
    page_title="Commission_campaign",
    page_icon="💰",
    layout="wide"
)


INACTIVITY_TIMEOUT_SECONDS = 5 * 60

def update_last_activity():
    st.session_state.last_activity = time.time()

def is_timed_out():
    now = time.time()
    last = st.session_state.get("last_activity", now)
    return (now - last) > INACTIVITY_TIMEOUT_SECONDS

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("main.py")

if "last_activity" not in st.session_state:
    st.session_state.last_activity = time.time()

# ถ้าไม่มีกิจกรรม 3 นาที ให้ล็อกเอาต์อัตโนมัติ
if is_timed_out():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.clear()
    st.info("⚠️ หมดเวลาไม่มีการใช้งาน 3 นาที กรุณาล็อกอินใหม่")
    time.sleep(1)
    st.switch_page("main.py")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("main.py")


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
    st.dataframe(df_basic, use_container_width=True,hide_index=True)
    
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
    "เลือกเป้า SIM",
    sim_choices,
    default=["5-19"],  # ตั้ง default ให้ช่องดูสมบูรณ์
    key="sim_multi"
)

st.subheader("💰 ใส่จำนวนตามช่วงราคา")
price_cols = st.columns(4)
price_inputs = {}
with price_cols[0]:
    price_inputs["200-249"] = st.number_input("200-249 บาท", min_value=0, value=0, step=1, key="price_200")
with price_cols[1]:
    price_inputs["250-299"] = st.number_input("250-299 บาท", min_value=0, value=0, step=1, key="price_250")
with price_cols[2]:
    price_inputs["300-349"] = st.number_input("300-349 บาท", min_value=0, value=0, step=1, key="price_300")
with price_cols[3]:
    price_inputs["350+"] = st.number_input("350+ บาท", min_value=0, value=0, step=1, key="price_350")

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
    st.dataframe(df_general, use_container_width=True, hide_index=True)
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
    
    st.dataframe(df_flash, use_container_width=True,hide_index=True)
    
    
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
    st.dataframe(df_student, use_container_width=True, hide_index=True)
     
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
    st.dataframe(df_tvs, use_container_width=True, hide_index=True)

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
st.dataframe(df_display, use_container_width=True, hide_index=True)


st.divider()

if st.button("🗑️ เคลียร์ข้อมูลทั้งหมด"):
    # ลบ input ทุกตัวที่ใช้ key แบบ input_-, sim_-, price_-
    to_delete = [
        k for k in st.session_state.keys()
        if (
            k.startswith("input_") or
            k.startswith("sim_") or
            k.startswith("price_") or
            k.startswith("input_student") or
            k.startswith("input_tvs")
        )
    ]
    for k in to_delete:
        del st.session_state[k]

    # ล้างค่า commission ต่าง ๆ ที่ใช้
    for total_key in [
        "total_commission",
        "total_commission_student",
        "total_commission_tvs",
        "total_commission_basic",
        "total_commission_flash",
    ]:
        if total_key in st.session_state:
            st.session_state[total_key] = 0

    st.rerun()


st.sidebar.title("ตัวเลือก")
if st.sidebar.button("ออกจากระบบ"):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.switch_page("main.py")
