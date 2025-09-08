import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="CallIntel Dashboard", layout="wide")
st.title("📞 CallIntel – ניתוח שיחות")

uploaded_file = st.file_uploader("העלה הקלטת שיחה", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.info("מעלה קובץ לשרת...")
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "audio/wav")}
    response = requests.post(f"{API_URL}/upload", files=files)

    if response.status_code == 200:
        data = response.json()
        call_id = data["call_id"]
        st.success(f"שיחה הועלתה בהצלחה! מזהה: {call_id}")
        st.json(data["result"])
    else:
        st.error("שגיאה בהעלאה.")
