import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="ورشة عبد الرزاق", layout="wide")
st.title("🔧 ورشة عبد الرزاق للإصلاح")

DATA_FILE = "joker_data.csv"

# --- إضافة جهاز جديد ---
with st.expander("➕ إضافة جهاز جديد"):
    with st.form("add_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        customer = c1.text_input("اسم الزبون")
        phone = c2.text_input("رقم الهاتف")
        device = c1.text_input("نوع الجهاز")
        fault = c2.text_input("العطل")
        status = st.selectbox("الحالة", ["تحت الصيانة", "بانتظار قطع غيار", "جاهز للتسليم", "تم التسليم"])
        if st.form_submit_button("حفظ الجهاز"):
            new_data = pd.DataFrame([[customer, phone, device, fault, status]], 
                                    columns=["الزبون", "الهاتف", "الجهاز", "العطل", "الحالة"])
            if os.path.exists(DATA_FILE):
                new_data.to_csv(DATA_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')
            else:
                new_data.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            st.success("تم الحفظ!")

st.markdown("---")

# --- البحث والعرض ---
st.subheader("🔍 بحث وعرض الأجهزة")
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
    
    # تحويل الحقول لنصوص لتجنب الأخطاء
    df["الزبون"] = df["الزبون"].astype(str)
    df["الهاتف"] = df["الهاتف"].astype(str)
    
    search = st.text_input("ابحث بالاسم أو رقم الهاتف:")
    if search:
        # البحث في الاسم أو الهاتف
        filtered_df = df[df["الزبون"].str.contains(search, na=False) | df["الهاتف"].str.contains(search, na=False)]
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)
else:
    st.info("لا توجد أجهزة مسجلة بعد.")
