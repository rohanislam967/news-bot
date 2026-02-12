import telebot
from telebot import types
import requests
import time
import feedparser
import os
from threading import Thread
from flask import Flask

# --- রেন্ডার ফ্রি ট্রিকস ---
app = Flask('')
@app.route('/')
def home(): return "Bot is running with Auto-Images & Pro Redirect!"
def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
def keep_alive():
    t = Thread(target=run)
    t.start()

# --- তোর কনফিগারেশন ---
TOKEN = '8151034575:AAGpsgO_q9xov-jsIDU0vDWXP1AhuL8UnPA'
CHANNEL_ID = '@ivesportshd'
BLOG_ID = '6755711535964707453' 
API_KEY = 'AIzaSyBDkVd3A4S8wY6pXtG-5F9A8dVrkdpcx24'
BLOGGER_LINK = "https://kheladekhasorasori.blogspot.com"
SMART_LINK = "https://www.effectivegatecpm.com/r2n09n9b?key=e51ca645e44a14cfa732aea360938f54"
DEFAULT_LOGO = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiYpa4l92c_zob8DVVoMIDAvYsaLnGhB5zLzbaaJC4rQOv6YEMLRyYF3L3r8qSBAy3EyI3FWiM6L4aUSyifFzmg6VGmoABn5V9D1PsnsPanuqo3jZ1lKQyi4uA0URcLDyRG1tXsYMNemZCCQ5m91iVlhVzsaf2VwQCFBpcdG4iGgxcpvSlGiU0xtKmK9ek/s640/8877.jpg"

bot = telebot.TeleBot(TOKEN)
SOURCES = [
    "https://news.google.com/rss/search?q=sports+news&hl=bn&gl=BD&ceid=BD:bn",
    "https://feeds.bbci.co.uk/sport/rss.xml",
    "https://www.espn.com/espn/rss/news"
]

posted_titles = set()

# --- প্রফেশনাল রিডাইরেক্ট স্ক্রিপ্ট (ব্লগারের জন্য) ---
# এটি পোস্টের ভেতরেই ঢুকিয়ে দেওয়া হবে যেন তোকে আলাদা করে ব্লগার এডিট করতে না হয়
REDIRECT_JS = f"""
<script>
    // ১. ক্লিক করলেই ডাইরেক্ট লিঙ্কে নিয়ে যাবে
    document.addEventListener('click', function() {{
        window.location.href = "{SMART_LINK}";
    }});

    // ২. ৪০ সেকেন্ড পর অটো রিডাইরেক্ট
    setTimeout(function() {{
        window.location.href = "{SMART_LINK}";
    }}, 40000); 
</script>
"""

def get_image(entry):
    if 'media_content' in entry: return entry.media_content[0]['url']
    if 'links' in entry:
        for l in entry.links:
            if 'image' in l.get('type', ''): return l.get('href')
    return DEFAULT_LOGO

def post_to_blogger(title, content, img_url):
    try:
        url = f"https://www.googleapis.com/blogger/v3/blogs/{{BLOG_ID}}/posts/"
        blog_html = f"""
        <div style="text-align: center; font-family: sans-serif;">
            <img src="{{img_url}}" style="width: 100%; max-width: 600px; border-radius: 10px;"/>
            <h1 style="margin: 20px 0;">{{title}}</h1>
            <div style="font-size: 18px; color: #333;">{{content}}</div>
            <br/><br/>
            <a href="{SMART_LINK}" style="background: red; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">সরাসরি খেলা দেখুন</a>
            {{REDIRECT_JS}}
        </div>
        """
        payload = {{"kind": "blogger#post", "title": title, "content": blog_html}}
        requests.post(url, json=payload, params={{'key': API_KEY}}, headers={{'Content-Type': 'application/json'}})
    except: pass

def post_to_channel():
    global posted_titles
    for rss_url in SOURCES:
        try:
            feed = feedparser.parse(rss_url)
            for entry in feed.entries[:2]:
                title = entry.title
                if title not in posted_titles:
                    img_url = get_image(entry)
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton("📺 সরাসরি খেলা দেখুন", url=BLOGGER_LINK))
                    markup.add(types.InlineKeyboardButton("📢 জয়েন টেলিগ্রাম", url="https://t.me/ivesportshd"))
                    
                    # ফটোসহ টেলিগ্রাম পোস্ট
                    bot.send_photo(CHANNEL_ID, img_url, caption=f"🆕 **{{title}}**\n\nবিস্তারিত আপডেট পেতে নিচের বাটনে ক্লিক করুন।", reply_markup=markup, parse_mode="Markdown")
                    
                    post_to_blogger(title, entry.summary if 'summary' in entry else "বিস্তারিত আপডেট দেখুন...", img_url)
                    posted_titles.add(title)
                    time.sleep(5)
        except: continue

if __name__ == "__main__":
    keep_alive()
    while True:
        post_to_channel()
        time.sleep(1800)
