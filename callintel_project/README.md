# CallIntel

מערכת SaaS לניתוח שיחות (עברית)

## 📌 איך מריצים

1. התקנת סביבת עבודה:
```bash
pip install -r requirements.txt
```

2. הרצת ה־API:
```bash
uvicorn backend.backend:app --reload --port 8000
```

3. הרצת הממשק (UI):
```bash
streamlit run ui/ui_dashboard.py
```

4. כניסה ל־Dashboard:
[http://localhost:8501](http://localhost:8501)
