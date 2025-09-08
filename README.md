# CallIntel

מערכת SaaS לניתוח שיחות (עברית)

## 📌 איך מריצים

1. התקנת סביבת עבודה:
   ```bash
   pip install -r requirements.txt
   ```

2. הרצת ה־API (בטרמינל אחד):
   ```bash
   uvicorn backend.backend:app --reload --port 8000
   ```

3. הרצת הממשק (UI) בטרמינל נוסף:
   ```bash
   streamlit run ui/ui_dashboard.py
   ```
   ניתן גם להריץ את שתי הפקודות במקביל בעזרת `&` או בכלי כמו `tmux`.

4. כניסה ל־Dashboard:
   [http://localhost:8501](http://localhost:8501)

## Batch Processing

ה־API תומך בהעלאת מספר קבצי שמע במקביל דרך הנתיב `/upload_batch`, והממשק יודע לשלוח קבצים מרובים בעת בחירה מרובה.

## המשך פיתוח

- שמירת נתונים ב־DB (PostgreSQL / MongoDB)
- אימות משתמשים (JWT/OAuth)
- חיוב לקוחות ושילוב ספק תשלומים
