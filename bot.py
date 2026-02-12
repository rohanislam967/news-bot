import telebot
from telebot import types
import requests
import time
import feedparser

# --- তোর প্রোজেক্ট সেটিংস ---
TOKEN = '8151034575:AAGpsgO_q9xov-jsIDU0vDWXP1AhuL8UnPA'
CHANNEL_ID = '@ivesportshd'
BLOG_ID = '6755711535964707453' 
API_KEY = 'AIzaSyBDkVd3A4S8wY6pXtG-5F9A8dVrkdpcx24'
BLOGGER_LINK = "https://kheladekhasorasori.blogspot.com"
SMART_LINK = "https://www.effectivegatecpm.com/r2n09n9b?key=e51ca645e44a14cfa732aea360938f54"
LOGO_URL = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiYpa4l92c_zob8DVVoMIDAvYsaLnGhB5zLzbaaJC4rQOv6YEMLRyYF3L3r8qSBAy3EyI3FWiM6L4aUSyifFzmg6VGmoABn5V9D1PsnsPanuqo3jZ1lKQyi4uA0URcLDyRG1tXsYMNemZCCQ5m91iVlhVzsaf2VwQCFBpcdG4iGgxcpvSlGiU0xtKmK9ek/s640/8877.jpg"

bot = telebot.TeleBot(TOKEN)
RSS_URL = "https://news.google.com/rss/search?q=sports+news&hl=bn&gl=BD&ceid=BD:bn"

# একই পোস্ট বারবার আসা বন্ধ করতে মেমোরি
posted_titles = set()

def post_to_blogger(title, content):
    try:
        url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
        blog_content = f"""
        <div style="text-align: center; font-family: Arial, sans-serif;">
            <img src="{LOGO_URL}" style="width: 100%; max-width: 600px; border-radius: 15px;" alt="Sports News"/>
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
        payload = {{"kind": "blogger#post", "title": title, "content": blog_content}}
        requests.post(url, json=payload, params={{'key': API_KEY}})
    except Exception as e:
        print(f"Blogger Error: {{e}}")

def post_to_channel():
    global posted_titles
    try:
        feed = feedparser.parse(RSS_URL)
        if feed.entries:
            for entry in feed.entries[:3]:
                title = entry.title
                if title not in posted_titles:
                    summary = entry.summary
                    
                    # টেলিগ্রাম বাটন সেটআপ (একদম ঠিকঠাক)
                    markup = types.InlineKeyboardMarkup()
                    btn_blog = types.InlineKeyboardButton("📺 সরাসরি খেলা দেখুন", url=BLOGGER_LINK)
                    btn_tele = types.InlineKeyboardButton("📢 জয়েন টেলিগ্রাম", url="https://t.me/ivesportshd")
                    markup.add(btn_blog)
                    markup.add(btn_tele)
                    
                    bot.send_message(CHANNEL_ID, f"🆕 **{{title}}**\n\nবিস্তারিত আপডেট পেতে নিচের বাটনে ক্লিক করুন।", reply_markup=markup, parse_mode="Markdown")
                    
                    # ব্লগারেও পোস্ট হবে
                    post_to_blogger(title, summary)
                    
                    posted_titles.add(title)
                    break
    except Exception as e:
        print(f"Telegram Error: {{e}}")

if __name__ == "__main__":
    while True:
        post_to_channel()
        time.sleep(1800) # ৩০ মিনিট পর পর চেক করবে
