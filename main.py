# -*- coding: utf-8 -*-

# --- BƯỚC 1: NHẬP CÁC THƯ VIỆN CẦN THIẾT ---
import os
import smtplib
import feedparser
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from urllib.parse import urlparse
import time
import calendar # Thêm thư viện calendar để xử lý múi giờ UTC chính xác nhất

# --- BƯỚC 2: NẠP CẤU HÌNH VÀ CÁC THÔNG TIN BÍ MẬT ---
print("Đang nạp các thông tin cấu hình...")
load_dotenv()

# Cấu hình Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Cấu hình Email
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
# Lấy danh sách email Cc từ biến môi trường
CC_RECIPIENT_EMAILS = os.getenv("CC_RECIPIENT_EMAILS", "")

<<<<<<< HEAD

=======
>>>>>>> e491c37fe0dba49406cd8c6bea8dafb53fa5a55d
# Danh sách các "quầy báo" (RSS feed)
RSS_FEEDS = [
    {'name': 'The Hacker News', 'url': 'https://feeds.feedburner.com/TheHackersNews'},
    {'name': 'Bleeping Computer', 'url': 'https://www.bleepingcomputer.com/feed/'},
    {'name': 'Cyberpress', 'url': 'https://cyberpress.org/feed/'},
    {'name': 'Security Online', 'url': 'https://securityonline.info/feed/'},
    {'name': 'SecurityWeek', 'url': 'http://feeds.feedburner.com/Securityweek'},
    {'name': 'Dark Reading', 'url': 'https://www.darkreading.com/rss.xml'}
]


# --- BƯỚC 3: XÂY DỰNG CÁC "CÔNG NHÂN" CHUYÊN BIỆT ---

def get_article_text(url):
<<<<<<< HEAD
    """Chỉ cố gắng lấy nội dung trực tiếp bằng requests."""
=======
    """
    Hàm này chỉ cố gắng lấy nội dung trực tiếp bằng requests.
    Nếu thất bại vì bất kỳ lý do gì, nó sẽ trả về None và bỏ qua.
    """
>>>>>>> e491c37fe0dba49406cd8c6bea8dafb53fa5a55d
    print(f"  ...Thử lấy trực tiếp từ: {url[:70]}...")
    SITE_SELECTORS = {
        'thehackernews.com': 'div.articlebody',
        'bleepingcomputer.com': 'div.article_section',
        'cyberpress.org': 'div.tdb_single_content',
        'securityonline.info': 'div.entry-content',
        'securityweek.com': 'div.zox-post-body',
        'darkreading.com': 'div.ArticleBase-BodyContent',
    }
    domain = urlparse(url).netloc
    selector = next((s for k, s in SITE_SELECTORS.items() if k in domain), 'article')
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.select_one(selector)
        if main_content:
            paragraphs = main_content.find_all('p')
            full_text = ' '.join([p.get_text() for p in paragraphs])
            if len(full_text) > 150:
                print("    -> Lấy trực tiếp thành công!")
                return full_text
<<<<<<< HEAD
=======
        
        # Nếu không có main_content hoặc text quá ngắn, nó sẽ đi xuống và trả về None
>>>>>>> e491c37fe0dba49406cd8c6bea8dafb53fa5a55d
        print(f"    -> Lấy trực tiếp thất bại (không tìm thấy selector '{selector}' hoặc nội dung quá ngắn). Bỏ qua.")
        return None
    except Exception as e:
        print(f"    -> Lỗi khi lấy trực tiếp: {e}. Bỏ qua bài viết này.")
        return None

def summarize_with_gemini(text_content, article_title):
<<<<<<< HEAD
    """Tóm tắt và định dạng nội dung bằng AI."""
    print("  ...Gửi cho AI tóm tắt và định dạng...")
    
    # Sử dụng model flash để tối ưu tốc độ và chi phí
    model = genai.GenerativeModel('gemini-1.5-flash')
=======
    """
    Tóm tắt và định dạng nội dung bằng AI.
    """
    print("  ...Gửi cho AI tóm tắt và định dạng...")
    
    # Sử dụng model flash để tối ưu tốc độ và chi phí
    model = genai.GenerativeModel('gemini-2.5-flash')
>>>>>>> e491c37fe0dba49406cd8c6bea8dafb53fa5a55d

    prompt = f"""
    Bạn là một chuyên gia phân tích an ninh mạng. Hãy phân tích nội dung bài báo có tiêu đề "{article_title}" và tóm tắt lại theo định dạng HTML nghiêm ngặt dưới đây.
    Chỉ trả về mã HTML của phần div, không thêm bất kỳ văn bản nào khác hay giải thích gì. Lưu ý tất cả bài viết phải được dịch ra tiếng Việt hoàn toàn.

    NỘI DUNG BÀI BÁO: {text_content[:8000]}

    MẪU ĐỊNH DẠNG HTML (sử dụng màu đỏ #d9534f cho mức độ nghiêm trọng):
    <div style="border-left: 4px solid #d9534f; padding-left: 15px; margin-bottom: 25px; background-color: #f9f9f9; padding: 5px 15px 15px 15px;">
        <p><strong>📝 Mô tả:</strong> [Mô tả ngắn gọn về lỗ hổng, sản phẩm bị ảnh hưởng và mã CVE. Nếu không phải tin về lỗ hổng thì mô tả sự kiện chính.]</p>
        <p><strong>💥 Mức độ ảnh hưởng:</strong> <strong style="color: #d9534f;">[Đánh giá mức độ, ví dụ: Nghiêm trọng/Cao/Trung bình/thấp]</strong> [Hậu quả chính nếu bị khai thác hoặc tầm quan trọng của tin tức.].</p>
        <p><strong>✅ Hành động Đề xuất:</strong></p>
        <ul style="margin-top: -10px;"><li>[Hành động 1, ví dụ: Cập nhật bản vá X.]</li><li>[Hành động 2, nếu có, ví dụ: Rà soát hệ thống Y.]</li></ul>
    </div>"""
    try:
        response = model.generate_content(prompt)
        raw_text = response.text
        cleaned_text = raw_text.replace("```html", "").replace("```", "").strip()
        return cleaned_text
    except Exception as e:
        print(f"  -> Lỗi khi tóm tắt bằng Gemini: {e}")
        return f"<p>Lỗi khi tóm tắt bài viết '{article_title}'. Lý do: {e}</p>"

def send_email(subject, html_body):
    """
<<<<<<< HEAD
    "Người đưa thư" phiên bản Microsoft, sử dụng máy chủ SMTP của Office 365.
=======
    Gửi email tổng hợp đi.
>>>>>>> e491c37fe0dba49406cd8c6bea8dafb53fa5a55d
    """
    print("\nChuẩn bị gửi email tổng hợp...")

    # Lấy danh sách email Cc từ biến môi trường (nếu có)
    cc_emails_str = os.getenv("CC_RECIPIENT_EMAILS", "")
    cc_list = [email.strip() for email in cc_emails_str.split(',') if email.strip()]

    msg = MIMEMultipart('alternative')
    msg['From'] = SENDER_EMAIL
    msg['Subject'] = subject
    msg['To'] = RECIPIENT_EMAIL
    if cc_list:
        msg['Cc'] = ", ".join(cc_list)

    msg.attach(MIMEText(html_body, 'html', 'utf-8'))
    all_recipients = [RECIPIENT_EMAIL] + cc_list
    
    try:
        # THAY ĐỔI CHÍNH NẰM Ở ĐÂY:
        # Sử dụng máy chủ và cổng của Microsoft/Outlook
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls() # Bật chế độ bảo mật
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        server.sendmail(SENDER_EMAIL, all_recipients, msg.as_string())
        
        server.quit()
        print(f"✅ Email tổng hợp đã được gửi thành công đến: {', '.join(all_recipients)}")
    except Exception as e:
        print(f"❌ Lỗi khi gửi email: {e}")

<<<<<<< HEAD
=======

>>>>>>> e491c37fe0dba49406cd8c6bea8dafb53fa5a55d
# --- BƯỚC 4: "QUẢN ĐỐC" ĐIỀU PHỐI CÔNG VIỆC ---
def main():
    """Hàm chính, điều phối toàn bộ quy trình."""
    print("\n🚀 Bắt đầu ca làm việc! Lấy và tóm tắt tin tức...")
    TIMESTAMP_FILE = "last_run_timestamp.txt"
    current_run_timestamp = datetime.now(timezone.utc)
    last_run_timestamp = datetime.fromtimestamp(0, tz=timezone.utc)
<<<<<<< HEAD
=======

>>>>>>> e491c37fe0dba49406cd8c6bea8dafb53fa5a55d
    try:
        with open(TIMESTAMP_FILE, "r") as f:
            timestamp_from_file = float(f.read().strip())
            last_run_timestamp = datetime.fromtimestamp(timestamp_from_file, tz=timezone.utc)
        print(f"Đã tìm thấy lần chạy trước, sẽ chỉ lấy tin tức sau: {last_run_timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    except FileNotFoundError:
        print("Không tìm thấy file timestamp, đây là lần chạy đầu tiên. Sẽ lấy tin trong 24 giờ qua.")
        last_run_timestamp = datetime.now(timezone.utc) - timedelta(days=1)
    except Exception as e:
        print(f"Lỗi khi đọc file timestamp, sẽ lấy tin trong 24 giờ qua. Lỗi: {e}")
        last_run_timestamp = datetime.now(timezone.utc) - timedelta(days=1)

    summaries_html_list = []
    for feed_info in RSS_FEEDS:
        print(f"\n🔍 Ghé thăm quầy báo: {feed_info['name']}")
        try:
            feed = feedparser.parse(feed_info['url'])
            for entry in feed.entries:
<<<<<<< HEAD
                # CẢI TIẾN: Dùng calendar.timegm để đảm bảo luôn xử lý thời gian theo UTC
                published_time_ts = calendar.timegm(entry.published_parsed)
                published_time = datetime.fromtimestamp(published_time_ts, tz=timezone.utc)
                
=======
                published_time = datetime.fromtimestamp(time.mktime(entry.published_parsed), tz=timezone.utc)

>>>>>>> e491c37fe0dba49406cd8c6bea8dafb53fa5a55d
                if published_time > last_run_timestamp:
                    print(f"  📰 Phát hiện tin mới: {entry.title}")
                    article_text = get_article_text(entry.link)
                    if article_text:
                        summary_html = summarize_with_gemini(article_text, entry.title)
                        article_block_html = f"""
                        <h2 style="font-size: 20px; margin-bottom: 5px; color: #003366;"><a href="{entry.link}" style="color: #0056b3; text-decoration: none;" target="_blank">{entry.title}</a></h2>
                        <p style="font-size: 14px; color: #555; margin-top: -15px; font-style: italic;">Nguồn: {feed_info['name']}</p>
                        {summary_html}"""
                        summaries_html_list.append(article_block_html)
                        print("    -> Tạm nghỉ 15 giây để chờ lượt API tiếp theo...")
<<<<<<< HEAD
                        time.sleep(15)
=======
                        time.sleep(15) 
>>>>>>> e491c37fe0dba49406cd8c6bea8dafb53fa5a55d
        except Exception as e:
            print(f"  -> Lỗi khi xử lý RSS feed của {feed_info['name']}: {e}")

    if summaries_html_list:
<<<<<<< HEAD
        # === SỬA LỖI MÚI GIỜ ===
=======
        # Chuyển đổi thời gian sang múi giờ Việt Nam (GMT+7)
>>>>>>> e491c37fe0dba49406cd8c6bea8dafb53fa5a55d
        utc_now = datetime.now(timezone.utc)
        gmt7 = timezone(timedelta(hours=7))
        vn_time = utc_now.astimezone(gmt7)
        run_time_str = vn_time.strftime("%H:%M ngày %d/%m/%Y")
<<<<<<< HEAD
=======
        
>>>>>>> e491c37fe0dba49406cd8c6bea8dafb53fa5a55d
        subject = f"Bản tin An ninh mạng cập nhật lúc {run_time_str}"
        
        final_body = "<hr style='border: 0; border-top: 1px solid #eee;'>".join(summaries_html_list)
        full_email_body = f"""
        <html><head></head>
        <body style="font-family: Arial, sans-serif; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
            <h1 style="color: #003366; text-align: center;">Bản tin An ninh mạng</h1>
            <p style="text-align: center;">Các tin tức mới nhất kể từ lần cập nhật trước, được tóm tắt bởi Trợ lý AI.</p>
            {final_body}
            <p style="text-align: center; margin-top: 30px; font-size: 12px; color: #999;">Email được tạo tự động bởi hệ thống tóm tắt tin tức.</p>
        </body></html>"""
        send_email(subject, full_email_body)
        
        try:
            with open(TIMESTAMP_FILE, "w") as f:
                f.write(str(current_run_timestamp.timestamp()))
            print(f"\n✅ Đã cập nhật timestamp cho lần chạy tiếp theo: {current_run_timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        except Exception as e:
            print(f"❌ Lỗi khi ghi file timestamp: {e}")
    else:
        print("\nKhông có tin tức mới nào kể từ lần chạy trước. Kết thúc ca làm việc.")

# --- BƯỚC 5: KHỞI ĐỘNG CỖ MÁY ---
if __name__ == "__main__":
    main()
