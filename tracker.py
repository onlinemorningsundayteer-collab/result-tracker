import hashlib
import os
import requests
from bs4 import BeautifulSoup

# আপনার টেলিগ্রাম ক্রেডেনশিয়াল
BOT_TOKEN = "8600395273:AAHkBESMupTIXel70sG1R7nyNZvQI95YAaI"
CHAT_ID = "8875207406"

# আপনার দেওয়া ১৭টি ওয়েবসাইটের সম্পূর্ণ তালিকা
WEBSITES = [
    {
        "name": "1. Juwai Teer (teerresults.com)",
        "url": "https://www.teerresults.com/",
    },
    {
        "name": "2. Khanapara Teer (khanaparateerresult.tv)",
        "url": "https://khanaparateerresult.tv/",
    },
    {
        "name": "3. Bhutan Teer (shillongteergrounds.in)",
        "url": "https://shillongteergrounds.in/bhutan-teer-result-today/",
    },
    {
        "name": "4. Shillong Teer (shillongteerground.com)",
        "url": "https://shillongteerground.com/",
    },
    {
        "name": "5. Juwai Night Teer (juwai.in)",
        "url": "https://juwai.in/juwai-night-teer-result/",
    },
    {
        "name": "6. Juwai Morning Teer (juwai.in)",
        "url": "https://juwai.in/juwai-morning-teer-results/",
    },
    {
        "name": "7. Manipur Teer (teermanipur.com)",
        "url": "https://teermanipur.com/",
    },
    {
        "name": "8. Khanapara Morning Teer",
        "url": "https://khanaparateeresult.com/#khanapara-morning-teer",
    },
    {
        "name": "9. Khanapara Night Teer",
        "url": "https://khanaparateeresult.com/#khanapara-night-teer",
    },
    {
        "name": "10. Bhutan Morning Teer",
        "url": "https://www.teerbhutanmorning.com/index.php",
    },
    {
        "name": "11. Bhutan Teer Afternoon",
        "url": "https://shillongteergrounds.in/bhutan-teer-result-today/",
    },
    {
        "name": "12. Night Teer Bhutan",
        "url": "https://nightteerbhutan.com/",
    },
    {
        "name": "13. Shillong Morning (morningsundeyteer.com)",
        "url": "https://morningsundeyteer.com/",
    },
    {
        "name": "14. Nagaland State Lottery",
        "url": "https://nagalandstatelottery.in/lottery-sambad-live-draw/",
    },
    {
        "name": "15. Haryana State Lottery",
        "url": "https://harianastatelottery.com/",
    },
    {
        "name": "16. Rajshree Lottery Results",
        "url": "https://rajshreelotteryresult.com/",  # আপনার ১৬ নম্বর রেজাল্ট পেজটির স্ট্যান্ডার্ড লিংক
    },
    {
        "name": "17. Maharashtra Lottery",
        "url": "https://lottery.maharashtra.gov.in/mhlotteryresults.aspx",
    },
]


def send_telegram_notification(site_name, url):
    message = (
        f"🚨 <b>NEW RESULT UPDATED!</b> 🚨\n\n"
        f"📌 <b>Target Site:</b> {site_name}\n"
        f"🔗 <b>Link:</b> {url}\n\n"
        f"⚡ <i>নির্ধারিত সময়ের পর ওয়েবসাইটে নতুন রেজাল্ট চলে এসেছে!</i>"
    )
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(telegram_url, data=payload, timeout=10)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")


def get_site_hash(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # অনাকাঙ্ক্ষিত скрипт বাদ দিয়ে মূল রেজাল্ট ডাটা রাখা
            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text()
            return hashlib.md5(text.encode("utf-8")).hexdigest()
    except Exception as e:
        print(f"Error checking {url}: {e}")
    return None


def main():
    for i, site in enumerate(WEBSITES):
        current_hash = get_site_hash(site["url"])
        if not current_hash:
            continue

        filename = f"site_hash_{i}.txt"
        old_hash = ""

        if os.path.exists(filename):
            with open(filename, "r") as f:
                old_hash = f.read().strip()

        # আগের রেজাল্টের সাথে নতুন রেজাল্ট না মিললেই ইনস্ট্যান্ট মেসেজ যাবে
        if old_hash and old_hash != current_hash:
            send_telegram_notification(site["name"], site["url"])

        # বর্তমান রেজাল্টের হ্যাশ ফাইলে লিখে রাখা
        with open(filename, "w") as f:
            f.write(current_hash)


if __name__ == "__main__":
    main()

