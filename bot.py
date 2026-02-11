import telebot
import requests
import time
import feedparser

# তোর দেওয়া তথ্য
TOKEN = '8151034575:AAGpsgO_q9xov-jsIDU0vDWXP1AhuL8UnPA'
CHANNEL_ID = '@ivesportshd'
BLOGGER_LINK = "https://kheladekhasorasori.blogspot.com"

bot = telebot.TeleBot(TOKEN)

# গুগল নিউজ আরএসএস ফিড (স্পোর্টস নিউজ)
RSS_URL = "https://news.google.com/rss/search?q=sports+news&hl=bn&gl=BD&ceid=BD:bn"

def get_latest_news():
    try:
        feed = feedparser.parse(RSS_URL)
        if feed.entries:
            # একদম লেটেস্ট খবরের টাইটেল নিবে
            entry = feed.entries[0]
            return entry.title
    except:
        return "আজকের সেরা স্পোর্টস আপডেট দেখে নিন!"
    return "লাইভ স্কোর এবং ব্রেকিং নিউজ আপডেট!"

def post_to_channel():
    try:
        headline = get_latest_news()
        message = f"📢 ব্রেকিং নিউজ: {headline}\n\nবিস্তারিত পড়ুন এখানে:\n👉 {BLOGGER_LINK}\n\nসব আপডেট পেতে জয়েন থাকুন: {CHANNEL_ID}"
        bot.send_message(CHANNEL_ID, message)
        print("News posted successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        post_to_channel()
        # ১ ঘণ্টা (৩৬০০ সেকেন্ড) পরপর পোস্ট হবে। তুই চাইলে ১৮০০ (৩০ মিনিট) দিতে পারিস।
        time.sleep(3600)
