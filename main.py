import streamlit as st
import os

st.set_page_config(page_title="ورشة جوكر", layout="centered")
st.title("🔧 نظام إدارة ورشة جوكر")

# --- إضافة بيانات جديدة ---
st.subheader("إضافة جهاز جديد للورشة")

customer_name = st.text_input("👤 اسم الزبون")
phone_number = st.text_input("📞 رقم الهاتف")
device_type = st.text_input("📱 نوع الجهاز")
fault = st.text_area("🛠️ العطل (المشكلة)")
status = st.selectbox("📋 حالة الجهاز", ["تحت الصيانة", "تم الإصلاح", "جاهز للتسليم"])
price = st.text_input("💰 السعر المتوقع")

if st.button("💾 حفظ البيانات"):
    with open("joker_data.txt", "a", encoding="utf-8") as f:
        f.write(f"الزبون: {customer_name} | الهاتف: {phone_number} | الجهاز: {device_type} | العطل: {fault} | الحالة: {status} | السعر: {price}\n")
    st.success("تم حفظ بيانات الجهاز بنجاح!")

st.markdown("---")

# --- عرض البيانات ---
st.subheader("📋 قائمة الأجهزة المسجلة")

if os.path.exists("joker_data.txt"):
    with open("joker_data.txt", "r", encoding="utf-8") as f:
        data = f.read()
        st.text(data)

    # زر تحميل البيانات
    st.download_button(label="📥 تحميل نسخة من البيانات", data=data, file_name="سجل_الورشة.txt")

    # زر مسح البيانات
    if st.button("🗑️ مسح جميع البيانات"):
        os.remove("joker_data.txt")
        st.rerun() # تحديث الصفحة بعد المسح
else:
    st.info("لا توجد أجهزة مسجلة حالياً.")
