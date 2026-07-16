import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="ورشة عبد الرزاق", layout="wide")
st.title("🔧 ورشة عبد الرزاق للإصلاح")

DATA_FILE = "joker_data.csv"

# --- إضافة جهاز جديد ---
with st.expander("➕ إضافة جهاز جديد"):
    with st.form("add_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        customer = c1.text_input("اسم الزبون")
        phone = c2.text_input("رقم الهاتف")
        device_type = c1.selectbox("نوع الجهاز", ["عجانات", "خلاطات", "مكروويف", "آلات عصر القهوة", "غير ذلك"])
        fault = c2.text_input("العطل")
        price = c1.text_input("السعر")
        status = c2.selectbox("الحالة", ["تحت الصيانة", "بانتظار قطع غيار", "جاهز للتسليم", "تم التسليم"])
        
        if st.form_submit_button("حفظ الجهاز"):
            today = datetime.now().strftime("%Y-%m-%d")
            new_data = pd.DataFrame([[customer, phone, device_type, fault, price, status, today]], 
                                    columns=["الزبون", "الهاتف", "الجهاز", "العطل", "السعر", "الحالة", "التاريخ"])
            if os.path.exists(DATA_FILE):
                new_data.to_csv(DATA_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')
            else:
                new_data.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            st.success("تم الحفظ!")
            st.rerun()

st.markdown("---")

# --- عرض وإدارة الأجهزة ---
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
    
    st.subheader("📋 قائمة الأجهزة")
    # عرض الجدول بدون الفهرس (0, 1, 2)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- عمليات الإدارة ---
    st.markdown("---")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("🔄 تحديث حالة")
        idx = st.number_input("رقم الصف لتحديثه", min_value=0, max_value=len(df)-1, step=1)
        new_stat = st.selectbox("الحالة الجديدة", ["تحت الصيانة", "بانتظار قطع غيار", "جاهز للتسليم", "تم التسليم"])
        if st.button("تحديث الحالة"):
            df.at[idx, "الحالة"] = new_stat
            df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            st.rerun()

    with col_b:
        st.subheader("🗑️ مسح زبون")
        del_idx = st.number_input("رقم الصف لمسحه", min_value=0, max_value=len(df)-1, step=1)
        if st.button("مسح هذا الزبون"):
            df = df.drop(del_idx)
            df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            st.rerun()
else:
    st.info("لا توجد بيانات حالياً.")
