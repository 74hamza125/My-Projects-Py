
import requests
from bs4 import BeautifulSoup
import time
from collections import Counter

# ✅ إعدادات بوت التلجرام
TELEGRAM_BOT_TOKEN = "7865254826:AAGrw61kugnvNTqfT0ayCoT1BqCst9WBRqg"  # ضع التوكن الخاص بك هنا
TELEGRAM_CHAT_ID = "1210701503"  # ضع chat_id هنا

# ✅ الكلمات المفتاحية المستهدفة
keywords = [
    "Power BI", "تقارير", "تحليلية", "تصميم لوحات تحكم تفاعلية", "Dashboards",
    "تعرض بيانات", "Data Visualization", "تقارير ديناميكية", "DAX", "Power Query",
    "داش بورد", "داش بورد تفاعلي", "Data Analyst", "ملف اكسل", "اكسل", "Excel",
    "لوحة تحكم", "داشبورد", "pivot table", "لوحة مؤشرات تفاعلية",
    "قاعدة البيانات", "البيانات", "سيرة ذاتية", "Sheet", "رسومات بيانية"
]

# ✅ رابط الصفحة المستهدفة
url = "https://mostaql.com/projects"

# ✅ تهيئة هيدر يشبه متصفح حقيقي لتجنب الحظر
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

# ✅ متغير لتخزين النتيجة السابقة مع عدد مرات ظهور كل كلمة
previous_search_result = Counter()

# ✅ تشغيل الكود بشكل مستمر
while True:
    print("\n🔍 جاري البحث عن الكلمات المفتاحية...")

    # ✅ إرسال الطلب وجلب الصفحة
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # ✅ تحليل المحتوى باستخدام BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # استخراج النصوص
        text_content = soup.get_text(separator=" ", strip=True).lower()

        # ✅ حساب عدد مرات ظهور كل كلمة مفتاحية في المحتوى الجديد
        current_search_result = Counter({word: text_content.count(word.lower()) for word in keywords if word.lower() in text_content})

        # ✅ إيجاد الكلمات الجديدة أو الكلمات التي زادت مرات ظهورها
        new_keywords = {word: count for word, count in current_search_result.items() if word not in previous_search_result or count > previous_search_result[word]}

        if new_keywords:
            # ✅ تجهيز رسالة التنبيه
            message = "🔍 تم العثور على تحديث جديد في مستقل:\n\n"
            for word, count in new_keywords.items():
                message += f"🔹 {word}: {count} مرات\n"

            # ✅ إرسال الإشعار إلى التلجرام
            telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            }
            requests.post(telegram_url, data=data)

            print(f"📢 تم إرسال الإشعار إلى التلجرام! الكلمات الجديدة أو المتكررة أكثر: {new_keywords}")

            # ✅ تحديث النتيجة السابقة بالنتيجة الجديدة
            previous_search_result = current_search_result.copy()

        else:
            print("❌ لم يتم العثور على كلمات جديدة أو زيادات في التكرار.")

    else:
        print(f"⚠️ فشل تحميل الصفحة، الكود: {response.status_code}")

    # ✅ الانتظار 5 دقائق قبل البحث مرة أخرى
    print("⏳ سيتم البحث مرة أخرى بعد 5 دقائق...")
    time.sleep(5)  # انتظار 5 دقائق
