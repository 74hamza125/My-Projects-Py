
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from collections import Counter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ✅ إعدادات بوت التلجرام
TELEGRAM_BOT_TOKEN = "7865254826:AAGrw61kugnvNTqfT0ayCoT1BqCst9WBRqg"  # ضع التوكن الخاص بك هنا
TELEGRAM_CHAT_ID = "1210701503"  # ضع chat_id هنا

# ✅ الكلمات المفتاحية المستهدفة
keywords = [
    "Power BI", "تقارير", "تحليلية", "تصميم لوحات تحكم تفاعلية", "Dashboards",
    "تعرض بيانات", "Data Visualization", "تقارير ديناميكية", "DAX", "Power Query",
    "داش بورد", "داش بورد تفاعلي", "Data Analyst", "ملف اكسل", "اكسل", "Excel",
    "لوحة تحكم", "داشبورد", "pivot table", "لوحة مؤشرات تفاعلية",
    "قاعدة البيانات", "البيانات", "سيرة ذاتية", "Sheet", "تصميم", "رسومات بيانية"
]

# ✅ رابط الصفحة المستهدفة
url = "https://mostaql.com/projects"

# ✅ إعداد `selenium` لجلب الصفحة بدون مشاكل
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ✅ تشغيل المتصفح
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# ✅ جلب الصفحة باستخدام `selenium`
driver.get(url)
html_content = driver.page_source
driver.quit()

# ✅ تحليل المحتوى باستخدام BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")
text_content = soup.get_text(separator=" ", strip=True).lower()

# ✅ حساب عدد مرات ظهور كل كلمة مفتاحية في المحتوى الجديد
current_search_result = Counter({word: text_content.count(word.lower()) for word in keywords if word.lower() in text_content})

# ✅ تحميل البيانات السابقة (من ملف مؤقت في GitHub Actions)
try:
    with open("previous_results.txt", "r", encoding="utf-8") as file:
        previous_search_result = Counter(eval(file.read()))
except FileNotFoundError:
    previous_search_result = Counter()

# ✅ إيجاد الكلمات الجديدة أو الكلمات التي زادت مرات ظهورها
new_keywords = {word: count for word, count in current_search_result.items() if word not in previous_search_result or count > previous_search_result[word]}

if new_keywords:
    # ✅ تجهيز رسالة التنبيه
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"🔍 تم العثور على تحديث جديد في مستقل بتاريخ {timestamp}:\n\n"
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

    # ✅ حفظ البيانات الحالية لتجنب تكرار نفس النتائج في البحث التالي
    with open("previous_results.txt", "w", encoding="utf-8") as file:
        file.write(str(dict(current_search_result)))
else:
    print("❌ لم يتم العثور على كلمات جديدة أو زيادات في التكرار.")
