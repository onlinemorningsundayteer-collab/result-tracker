import os
import requests
from bs4 import BeautifulSoup

# আপনার টেলিগ্রাম ক্রেডেনশিয়াল
BOT_TOKEN = "8600395273:AAHkBESMupTIXel70sG1R7nyNZvQI95YAaI"
CHAT_ID = "8875207406"

# ১৭টি ওয়েবসাইটের তালিকা
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
        "url": "https://rajshreelotteryresult.com/",
    },
    {
        "name": "17. Maharashtra Lottery",
        "url": "https://lottery.maharashtra.gov.in/mhlotteryresults.aspx",
    },
]


def send_telegram_message(text):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(telegram_url, data=payload, timeout=10)
    except Exception as e:
        print(f"Error sending message: {e}")


def get_clean_numbers(url):
    # রিয়েল ব্রাউজার হেডার
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # পেজের টেবিল ও ডিভ ট্যাগ থেকে শুধু সংখ্যা ও মূল টেক্সট বের করা
            text_blocks = []
            for tag in soup.find_all(["table", "tr", "td", "div"]):
                t = tag.get_text(strip=True)
                if t and len(t) < 300:
                    text_blocks.append(t)

            return " ".join(text_blocks)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None


def main():
    updated_count = 0
    checked_count = 0

    for i, site in enumerate(WEBSITES):
        current_data = get_clean_numbers(site["url"])
        if not current_data:
            continue

        checked_count += 1
        filename = f"site_data_{i}.txt"
        old_data = ""

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                old_data = f.read()

        # যদি ডাটা চেঞ্জ হয়
        if old_data and old_data != current_data:
            msg = (
                f"🚨 <b>RESULT UPDATED!</b> 🚨\n\n📌 <b>Site:</b>"
                f" {site['name']}\n🔗 <b>Link:</b> {site['url']}\n\n⚡"
                " <i>ওয়েবসাইটে রেজাল্ট আপডেট হয়েছে!</i>"
            )
            send_telegram_message(msg)
            updated_count += 1

        # নতুন ডাটা সেভ রাখা
        with open(filename, "w", encoding="utf-8") as f:
            f.write(current_data)

    # এটি প্রতি রান শেষে বটের স্ট্যাটাস জানানোর জন্য টেস্ট বার্তা পাঠাবে
    debug_msg = f"⚙️ <b>Tracker Check Done!</b>\n\n✅ Checked Sites: {checked_count}/{len(WEBSITES)}\n🔔 Updates Found: {updated_count}"
    send_telegram_message(debug_msg)


if __name__ == "__main__":
    main()
