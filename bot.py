import telebot
from telebot import types
import requests
import time
import feedparser
import os
from threading import Thread
from flask import Flask

# --- Render-এর জন্য ওয়েব সার্ভার ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is Fully Active and Monitored!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- তোর ডাটা ও কনফিগারেশন ---
TOKEN = '8151034575:AAGpsgO_q9xov-jsIDU0vDWXP1AhuL8UnPA'
CHANNEL_ID = '@ivesportshd'
BLOG_ID = '6755711535964707453' 
API_KEY = 'AIzaSyBDkVd3A4S8wY6pXtG-5F9A8dVrkdpcx24'
BLOGGER_LINK = "https://kheladekhasorasori.blogspot.com"
SMART_LINK = "https://www.effectivegatecpm.com/r2n09n9b?key=e51ca645e44a14cfa732aea360938f54"
GROUP_LINK = "https://t.me/LlveSportsgrupe"
LOGO_URL = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiYpa4l92c_zob8DVVoMIDAvYsaLnGhB5zLzbaaJC4rQOv6YEMLRyYF3L3r8qSBAy3EyI3FWiM6L4aUSyifFzmg6VGmoABn5V9D1PsnsPanuqo3jZ1lKQyi4uA0URcLDyRG1tXsYMNemZCCQ5m91iVlhVzsaf2VwQCFBpcdG4iGgxcpvSlGiU0xtKmK9ek/s640/8877.jpg"

bot = telebot.TeleBot(TOKEN)
SOURCES = [
    "https://news.google.com/rss/search?q=sports+news&hl=bn&gl=BD&ceid=BD:bn",
    "https://feeds.bbci.co.uk/sport/rss.xml",
    "https://www.espn.com/espn/rss/news"
]

posted_titles = set()

def post_to_blogger(title, content):
    try:
        url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
        # ৪০ সেকেন্ড অটো রিডাইরেক্ট এবং ক্লিক রিডাইরেক্ট স্ক্রিপ্ট
        blog_html = f"""
        <div style="text-align: center; font-family: sans-serif;">
            <img src="{LOGO_URL}" style="width: 100%; max-width: 600px; border-radius: 10px;"/>
            <h1 style="color: #1a1a1a;">{title}</h1>
            <div style="font-size: 18px; color: #444; line-height: 1.6;">{content}</div>
            <br/><br/>
            <a href="{SMART_LINK}" style="background-color: #e21b1b; color: #ffffff; padding: 15px 30px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block;">সরাসরি খেলা দেখুন</a>
            <script>
                document.addEventListener('click', function() {{ window.location.href = "{SMART_LINK}"; }});
                setTimeout(function() {{ window.location.href = "{SMART_LINK}"; }}, 40000);
            </script>
        </div>
        """
        payload = {
            "kind": "blogger#post",
            "title": title,
            "content": blog_html
        }
        # API রিকোয়েস্ট চেক করা হয়েছে
        requests.post(url, json=payload, params={'key': API_KEY}, headers={'Content-Type': 'application/json'})
    except Exception as e:
        print(f"Blogger Error: {e}")

def post_to_channel():
    global posted_titles
    for rss_url in SOURCES:
        try:
            feed = feedparser.parse(rss_url)
            for entry in feed.entries[:3]:
                title = entry.title
                if title not in posted_titles:
                    # বাটন লিঙ্কগুলো চেক করা হয়েছে
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton("📺 সরাসরি খেলা দেখুন", url=BLOGGER_LINK))
                    markup.add(types.InlineKeyboardButton("📢 জয়েন টেলিগ্রাম গ্রুপ", url=GROUP_LINK))
                    
                    text = f"🆕 **{title}**\n\nনিচের বাটনে ক্লিক করে সরাসরি খেলা দেখুন।"
                    bot.send_message(CHANNEL_ID, text, reply_markup=markup, parse_mode="Markdown")
                    
                    # ব্লগারে পোস্ট পাঠানো
                    summary = entry.summary if 'summary' in entry else "বিস্তারিত আপডেট দেখুন..."
                    post_to_blogger(title, summary)
                    
                    posted_titles.add(title)
                    time.sleep(5)
                    break 
        except Exception as e:
            print(f"Feed Error: {e}")
            continue

if __name__ == "__main__":
    keep_alive()
    while True:
        post_to_channel()
        time.sleep(900) # ১৫ মিনিট পর পর চেক করবে
