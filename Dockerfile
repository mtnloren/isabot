# 1. בחירת מערכת הפעלה בסיסית
FROM python:3.10-slim

# 2. הגדרת תיקיית עבודה בתוך הקונטיינר
WORKDIR /app

# 3. העתקת רשימת הספריות קודם (לזיכרון מטמון טוב יותר)
COPY requirements.txt .

# 4. התקנת כל הספריות
RUN pip install --no-cache-dir -r requirements.txt

# 5. העתקת כל הקוד לקונטיינר
COPY . .

# 6. הגדרת הפורט שהאפליקציה תשתמש בו
EXPOSE 5000

# 7. פקודת הפעלה (חשוב: ללא סוגריים!)
CMD python main.py
