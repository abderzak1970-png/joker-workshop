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
        
        # قائمة الأجهزة الذكية
        device_options = ["عجانات", "خلاطات", "مكروويف", "آلات عصر القهوة", "غير ذلك"]
        device_selection = c1.selectbox("نوع الجهاز", device_options)
        if device_selection == "غير ذلك":
            device_type = c1.text_input("اكتب نوع الجهاز هنا")
        else:
            device_type = device_selection
            
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

st.markdown("---")

# --- عرض وتحديث الأجهزة ---
st.subheader("📋 سجل الأجهزة")
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
    
    # البحث
    search = st.text_input("🔍 بحث بالاسم أو الهاتف:")
    if search:
        df = df[df["الزبون"].str.contains(search, na=False) | df["الهاتف"].str.contains(search, na=False)]
    
    st.dataframe(df, use_container_width=True)

    # زر بسيط لتحديث حالة أول جهاز يظهر في البحث
    if not df.empty:
        st.write("---")
        st.subheader("🔄 تحديث حالة جهاز")
        target_index = st.number_input("أدخل رقم الصف (Index) للجهاز المراد تحديثه", min_value=0, max_value=len(df)-1, step=1)
        new_status = st.selectbox("الحالة الجديدة", ["تحت الصيانة", "بانتظار قطع غيار", "جاهز للتسليم", "تم التسليم"])
        
        if st.button("تحديث الحالة"):
            df.at[target_index, "الحالة"] = new_status
            df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            st.success("تم التحديث!")
            st.rerun()
else:
    st.info("لا توجد أجهزة مسجلة.")
