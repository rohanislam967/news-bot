import telebot
from telebot import types
import requests
import time
import feedparser
import os
from threading import Thread
from flask import Flask

# --- ওয়েব সার্ভার সেটিংস (রেন্ডার ফ্রিতে চালানোর জন্য) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- তোর প্রোজেক্ট কনফিগারেশন ---
TOKEN = '8151034575:AAGpsgO_q9xov-jsIDU0vDWXP1AhuL8UnPA'
CHANNEL_ID = '@ivesportshd'
BLOG_ID = '6755711535964707453' 
API_KEY = 'AIzaSyBDkVd3A4S8wY6pXtG-5F9A8dVrkdpcx24'
BLOGGER_LINK = "https://kheladekhasorasori.blogspot.com"
SMART_LINK = "https://www.effectivegatecpm.com/r2n09n9b?key=e51ca645e44a14cfa732aea360938f54"
LOGO_URL = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiYpa4l92c_zob8DVVoMIDAvYsaLnGhB5zLzbaaJC4rQOv6YEMLRyYF3L3r8qSBAy3EyI3FWiM6L4aUSyifFzmg6VGmoABn5V9D1PsnsPanuqo3jZ1lKQyi4uA0URcLDyRG1tXsYMNemZCCQ5m91iVlhVzsaf2VwQCFBpcdG4iGgxcpvSlGiU0xtKmK9ek/s640/8877.jpg"

bot = telebot.TeleBot(TOKEN)
RSS_URL = "https://news.google.com/rss/search?q=sports+news&hl=bn&gl=BD&ceid=BD:bn"

posted_titles = set()

def post_to_blogger(title, content):
    try:
        url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
        blog_content = f"""
        <div style="text-align: center; font-family: Arial, sans-serif;">
            <img src="{LOGO_URL}" style="width: 100%; max-width: 600px; border-radius: 15px;" alt="News"/>
            <h1 style="color: #1a1a1a; margin-top: 20px;">{title}</h1>
            <div style="font-size: 18px; line-height: 1.6; color: #444; text-align: justify; padding: 0 15px;">
                {content}
            </div>
            <br/><br/>
            <a href="{SMART_LINK}" style="background-color: #e21b1b; color: #ffffff; padding: 18px 35px; text-decoration: none; font-weight: bold; border-radius: 50px; font-size: 22px; display: inline-block;">
                সরাসরি খেলা দেখতে এখানে ক্লিক করুন
            </a>
        </div>
        """
        payload = {"kind": "blogger#post", "title": title, "content": blog_content}
        requests.post(url, json=payload, params={'key': API_KEY})
    except: pass

def post_to_channel():
    global posted_titles
    try:
        feed = feedparser.parse(RSS_URL)
        if feed.entries:
            for entry in feed.entries[:3]:
                title = entry.title
                if title not in posted_titles:
                    summary = entry.summary
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton("📺 সরাসরি খেলা দেখুন", url=BLOGGER_LINK))
                    markup.add(types.InlineKeyboardButton("📢 জয়েন টেলিগ্রাম", url="https://t.me/ivesportshd"))
                    
                    bot.send_message(CHANNEL_ID, f"🆕 **{title}**\n\nবিস্তারিত আপডেট পেতে নিচের বাটনে ক্লিক করুন।", reply_markup=markup, parse_mode="Markdown")
                    post_to_blogger(title, summary)
                    posted_titles.add(title)
                    break
    except: pass

if __name__ == "__main__":
    keep_alive() # রেন্ডারকে খুশি রাখার জন্য ভুয়া সার্ভার চালু
    while True:
        post_to_channel()
        time.sleep(1800)
