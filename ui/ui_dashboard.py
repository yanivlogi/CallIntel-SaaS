import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="CallIntel Dashboard", layout="wide")
st.title("📞 CallIntel – ניתוח שיחות")

uploaded_files = st.file_uploader(
    "העלה הקלטות שיחה", type=["mp3", "wav", "m4a"], accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) == 1:
        uploaded_file = uploaded_files[0]
        st.info("מעלה קובץ לשרת...")
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "audio/wav")}
        response = requests.post(f"{API_URL}/upload", files=files)
    else:
        st.info("מעלה קבצים לשרת (batch)...")
        files = [("files", (f.name, f.getvalue(), "audio/wav")) for f in uploaded_files]
        response = requests.post(f"{API_URL}/upload_batch", files=files)

    if response.status_code == 200:
        data = response.json()
        st.success("העלאה הושלמה!")
        st.json(data)
    else:
        st.error("שגיאה בהעלאה.")
