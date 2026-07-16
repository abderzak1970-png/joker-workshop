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
            
            if not os.path.exists(DATA_FILE):
                new_data.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            else:
                new_data.to_csv(DATA_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')
            st.success("تم الحفظ!")
            st.rerun()

st.markdown("---")

# --- عرض البيانات ---
if os.path.exists(DATA_FILE):
    try:
        df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
        st.subheader("📋 قائمة الأجهزة")
        st.dataframe(df, use_container_width=True, hide_index=True)
    except:
        st.error("حدث خطأ في قراءة ملف البيانات، يرجى مسح الملف والبدء من جديد.")
        if st.button("مسح الملف المتضرر"):
            os.remove(DATA_FILE)
            st.rerun()
else:
    st.info("لا توجد بيانات حالياً.")
