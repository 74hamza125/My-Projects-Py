

import requests
from bs4 import BeautifulSoup
import time

# ✅ إعدادات بوت التلجرام
TELEGRAM_BOT_TOKEN = "7865254826:AAGrw61kugnvNTqfT0ayCoT1BqCst9WBRqg"  # ضع التوكن الخاص بك هنا
TELEGRAM_CHAT_ID = "1210701503"  # ضع chat_id هنا

# ✅ رابط الصفحة المستهدفة
url = "https://mostaql.com/projects"

# ✅ تهيئة هيدر يشبه متصفح حقيقي
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

# ✅ تشغيل الكود بشكل متكرر
while True:
    print("\n🔍 جاري البحث عن المحتوى الجديد...")

    # ✅ إرسال الطلب وجلب الصفحة
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # ✅ تحليل المحتوى باستخدام BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # ✅ استخراج النصوص من الصفحة بالكامل
        full_text = soup.get_text(separator="\n", strip=True)

        # ✅ تقسيم النصوص لضمان عدم تجاوز الحد الأقصى لرسائل تلجرام (4096 حرف)
        max_length = 4000
        chunks = [full_text[i:i + max_length] for i in range(0, len(full_text), max_length)]

        for chunk in chunks:
            message = f"🔍 محتوى صفحة مستقل:\n\n{chunk}"
            
            # ✅ إرسال المحتوى إلى تلجرام
            telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            }
            requests.post(telegram_url, data=data)

        print("📢 تم إرسال محتوى الصفحة إلى تلجرام!")

    else:
        print(f"⚠️ فشل تحميل الصفحة، الكود: {response.status_code}")

    # ✅ الانتظار 60 ثانية قبل البحث مرة أخرى
    print("⏳ سيتم البحث مرة أخرى بعد دقيقة...")
    time.sleep(60)  # انتظار دقيقة واحدة
