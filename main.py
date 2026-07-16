import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="ورشة عبد الرزاق", layout="wide")
st.title("🔧 نظام إدارة ورشة عبد الرزاق")

# --- ملف البيانات ---
DATA_FILE = "joker_data.csv"

# --- إضافة بيانات جديدة ---
with st.expander("➕ إضافة جهاز جديد"):
    col1, col2 = st.columns(2)
    with col1:
        customer = st.text_input("اسم الزبون")
        phone = st.text_input("رقم الهاتف")
    with col2:
        device = st.text_input("نوع الجهاز")
        status = st.selectbox("حالة الجهاز", ["تحت الصيانة", "بانتظار قطع غيار", "جاهز للتسليم", "تم التسليم"])
    
    fault = st.text_area("وصف العطل")
    price = st.text_input("السعر")

    if st.button("حفظ البيانات"):
        new_data = pd.DataFrame([[customer, phone, device, fault, status, price]], 
                                columns=["الزبون", "الهاتف", "الجهاز", "العطل", "الحالة", "السعر"])
        if os.path.exists(DATA_FILE):
            new_data.to_csv(DATA_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')
        else:
            new_data.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
        st.success("تم الحفظ!")

st.markdown("---")

# --- عرض البيانات مع الفلتر ---
st.subheader("📋 سجل الأجهزة")
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
    
    # فلتر حسب الحالة
    filter_status = st.multiselect("فلتر حسب الحالة:", options=df["الحالة"].unique(), default=df["الحالة"].unique())
    filtered_df = df[df["الحالة"].isin(filter_status)]
    
    st.dataframe(filtered_df, use_container_width=True)

    # تنبيه للأجهزة التي تنتظر قطع غيار
    waiting_parts = df[df["الحالة"] == "بانتظار قطع غيار"]
    if not waiting_parts.empty:
        st.warning(f"⚠️ تنبيه: لديك {len(waiting_parts)} أجهزة بانتظار قطع غيار!")

    # زر مسح
    if st.button("🗑️ مسح جميع البيانات"):
        os.remove(DATA_FILE)
        st.rerun()
else:
    st.info("لا توجد بيانات حالياً.")
