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
    
    # البحث
    search = st.text_input("🔍 بحث بالاسم أو الهاتف:")
    if search:
        df = df[df["الزبون"].str.contains(search, na=False) | df["الهاتف"].str.contains(search, na=False)]
    
    st.subheader("📋 قائمة الأجهزة")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- عمليات الإدارة ---
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔄 تحديث حالة")
        # نستخدم قائمة منسدلة لاختيار الزبون لتسهيل التحديث بدلاً من كتابة الرقم يدوياً
        selected_customer = st.selectbox("اختر الزبون لتحديث حالته:", df["الزبون"].tolist())
        new_stat = st.selectbox("الحالة الجديدة", ["تحت الصيانة", "بانتظار قطع غيار", "جاهز للتسليم", "تم التسليم"])
        
        if st.button("تحديث الحالة"):
            df.loc[df["الزبون"] == selected_customer, "الحالة"] = new_stat
            df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            st.rerun()

    with col2:
        st.subheader("🗑️ مسح زبون")
        del_customer = st.selectbox("اختر الزبون لمسحه:", df["الزبون"].tolist())
        if st.button("مسح هذا الزبون نهائياً"):
            df = df[df["الزبون"] != del_customer]
            df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            st.rerun()
else:
    st.info("لا توجد بيانات حالياً.")
