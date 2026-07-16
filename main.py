import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="ورشة عبد الرزاق", layout="wide")
st.title("🔧 ورشة عبد الرزاق للإصلاح")

DATA_FILE = "joker_data.csv"

# --- إضافة جهاز جديد ---
with st.expander("➕ إضافة جهاز جديد"):
    with st.form("add_form"):
        c1, c2 = st.columns(2)
        customer = c1.text_input("اسم الزبون")
        phone = c2.text_input("رقم الهاتف")
        device = c1.text_input("نوع الجهاز")
        fault = c2.text_input("العطل")
        status = st.selectbox("الحالة", ["تحت الصيانة", "بانتظار قطع غيار", "جاهز للتسليم", "تم التسليم"])
        if st.form_submit_button("حفظ الجهاز"):
            new_row = pd.DataFrame([[customer, phone, device, fault, status]], 
                                    columns=["الزبون", "الهاتف", "الجهاز", "العطل", "الحالة"])
            if os.path.exists(DATA_FILE):
                new_row.to_csv(DATA_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')
            else:
                new_row.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            st.success("تم الحفظ!")

st.markdown("---")

# --- البحث والفرز ---
st.subheader("🔍 بحث وعرض الأجهزة")
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
    
    # مربع البحث
    search = st.text_input("ابحث بالاسم أو رقم الهاتف:")
    if search:
        df = df[df["الزبون"].str.contains(search, na=False) | df["الهاتف"].str.contains(search, na=False)]
    
    # عرض الجدول
    st.dataframe(df, use_container_width=True)

    # التنبيهات الذكية
    pending = df[df["الحالة"] == "بانتظار قطع غيار"]
    if not pending.empty:
        st.warning(f"⚠️ تنبيه: {len(pending)} جهاز يحتاج لقطع غيار.")
else:
    st.info("لا توجد أجهزة مسجلة.")
