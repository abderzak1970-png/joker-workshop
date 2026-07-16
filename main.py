import streamlit as st
import os

st.set_page_config(page_title="ورشة جوكر", layout="centered")
st.title("🔧 نظام إدارة ورشة جوكر")

# --- إضافة بيانات جديدة ---
st.subheader("إضافة جهاز")
device_name = st.text_input("📱 اسم الجهاز")
status = st.selectbox("🛠️ الحالة", ["تحت الصيانة", "تم الإصلاح", "جاهز للتسليم"])
price = st.text_input("💰 السعر")

if st.button("💾 حفظ البيانات"):
    with open("joker_data.txt", "a", encoding="utf-8") as f:
        f.write(f"{device_name} | {status} | {price}\n")
    st.success("تم الحفظ!")

st.markdown("---")

# --- عرض البيانات مع خيارات إضافية ---
st.subheader("📋 قائمة الأجهزة")

if os.path.exists("joker_data.txt"):
    with open("joker_data.txt", "r", encoding="utf-8") as f:
        data = f.read()
        st.text(data)

    # زر تحميل البيانات
    st.download_button(label="📥 تحميل نسخة من البيانات", data=data, file_name="ورشة_جوكر.txt")

    # زر مسح البيانات
    if st.button("🗑️ مسح جميع البيانات"):
        os.remove("joker_data.txt")
        st.warning("تم مسح البيانات! قم بتحديث الصفحة.")
else:
    st.info("لا توجد أجهزة مسجلة حالياً.")
