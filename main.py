import streamlit as st
import os

st.set_page_config(page_title="ورشة جوكر", layout="centered")
st.title("🔧 نظام إدارة ورشة جوكر")

device_name = st.text_input("📱 اسم الجهاز")
status = st.selectbox("🛠️ حالة الجهاز", ["تحت الصيانة", "تم الإصلاح", "جاهز للتسليم"])
price = st.text_input("💰 السعر")

if st.button("💾 حفظ"):
    with open("joker_data.txt", "a", encoding="utf-8") as f:
        f.write(f"{device_name} | {status} | {price}\n")
    st.success("تم الحفظ!")

if os.path.exists("joker_data.txt"):
    with open("joker_data.txt", "r", encoding="utf-8") as f:
        st.write("📋 الأجهزة:")
        st.text(f.read())
