import telebot
import requests
import time
from datetime import datetime, timedelta

# Điền token bot 
TOKEN = "8216004292:AAHNWPVbBBbs51hElngcNRZ879chsYPtQrQ"
bot = telebot.TeleBot(TOKEN)


# Lệnh start giới thiệu bot và các lệnh
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f"""📑<b>HƯỚNG DẪN SỬ DỤNG</b>\n
<blockquote>Danh Sách Các Lệnh Của Bot 🎉</blockquote>\n
<blockquote> Tiện Ích ✨ 
/reghotmail - Tạo tài khoản Hotmail \n
/demngay - Đếm số ngày đến các dịp lễ \n
/getidfb - Lấy UID Facebook từ link \n
/videoanime - Lấy video anime ngẫu nhiên \n
/videogai - Lấy video gái ngẫu nhiên \n
</blockquote>
<blockquote> Công Cụ Spam 📨 
/sms - Spam SMS Siêu Nhanh Nhiều tin \n                 
</blockquote>
                 
<blockquote> Thông Tin 👑
/admin - Giới thiệu admin \n
          </blockquote>       
""",
                     parse_mode="HTML")





# Lưu thời gian người dùng chạy lệnh /sms lần cuối
last_sms_time = {}
# Lệnh spam sms 
@bot.message_handler(commands=['sms'])
def sms(message):
    try:
        user_id = message.from_user.id
        parts = message.text.split(" ", 1)

        # Kiểm tra tham số
        if len(parts) < 2:
            bot.send_message(
                message.chat.id,
                "<blockquote>❌ Vui lòng nhập số điện thoại!\n\nVí dụ:\n<code>/sms 0987654321</code></blockquote>",
                parse_mode="HTML"
            )
            return

        phone = parts[1].strip()

        # 🔹 Kiểm tra phone có đủ 10 số không
        if not phone.isdigit() or len(phone) != 10:
            bot.send_message(
                message.chat.id,
                "<blockquote>⚠️ Số điện thoại phải là 10 số!</blockquote>",
                parse_mode="HTML"
            )
            return

        # 🔹 Kiểm tra cooldown 2 phút
        now = datetime.now()
        if user_id in last_sms_time:
            elapsed = now - last_sms_time[user_id]
            if elapsed < timedelta(minutes=2):
                remaining = 120 - int(elapsed.total_seconds())
                bot.send_message(
                    message.chat.id,
                    f"<blockquote>⏳ Bạn phải chờ <b>{remaining} giây</b> nữa mới dùng lại được lệnh!</blockquote>",
                    parse_mode="HTML"
                )
                return

        # Cập nhật thời gian chạy lệnh
        last_sms_time[user_id] = now

        bot.send_message(
            message.chat.id,
            f"""<blockquote>📨 <b>SPAM SMS </b></blockquote>\n
<blockquote>💥 Đang gửi SMS tới:\n{phone}</blockquote>""",
            parse_mode="HTML"
        )

        # Chạy script Python
        import subprocess
        result = subprocess.run(
            ["python", "sms.py", phone, "10"],
            capture_output=True,
            text=True
        )

        output = result.stdout if result.stdout else "Không có phản hồi từ script!"

        bot.send_message(
            message.chat.id,
            f"""<blockquote>✅ <b>HOÀN THÀNH</b>\n
📱 Số: <code>{phone}</code>""",
            parse_mode="HTML"
        )

    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"<blockquote>Buff MXH https://ductuyensub.site</blockquote>",
            parse_mode="HTML"
        )


# /reghotmail – tạo tài khoản Hotmail
@bot.message_handler(commands=['reghotmail'])
def reghotmail(message):
    try:
        api_url = "https://keyherlyswar.x10.mx/Apidocs/reghotmail.php"
        response = requests.get(api_url).json()

        bot.send_message(
            message.chat.id,
            """<blockquote>📧 <b>TẠO HOTMAIL </b></blockquote>\n
<blockquote>⏳ Đang tạo tài khoản...</blockquote>""",
            parse_mode="HTML"
        )

        if response.get("status") and response.get("result"):
            email = response["result"].get("email")
            password = response["result"].get("password")

            bot.send_message(
                message.chat.id,
                f"""<blockquote>✅ <b>TẠO HOTMAIL THÀNH CÔNG</b>\n
📩 Email: <code>{email}</code>
🔑 Mật khẩu: <code>{password}</code></blockquote>""",
                parse_mode="HTML"
            )
        else:
            bot.send_message(
                message.chat.id,
                "<blockquote>❌ Không tạo được Hotmail!</blockquote>",
                parse_mode="HTML"
            )

    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"<blockquote>⚠️ Lỗi khi gọi API:\n<code>{e}</code></blockquote>",
            parse_mode="HTML"
        )

# /demngay – đếm số ngày đến các dịp lễ
@bot.message_handler(commands=['demngay'])
def demngay(message):
    try:
        api_url = "https://keyherlyswar.x10.mx/Apidocs/demngay.php"
        response = requests.get(api_url).json()

        bot.send_message(
            message.chat.id,
            """<blockquote>📅 <b>ĐẾM NGÀY CÁC SỰ KIỆN</b></blockquote>\n
<blockquote>⏳ Đang lấy dữ liệu...</blockquote>""",
            parse_mode="HTML"
        )

        # Tạo danh sách hiển thị
        result_text = ""
        for event, days in response.items():
            result_text += f"<blockquote>🎯 <b>{event}</b>: <code>{days}</code></blockquote>\n"

        bot.send_message(
            message.chat.id,
            result_text,
            parse_mode="HTML"
        )

    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"<blockquote>⚠️ Lỗi khi gọi API:\n<code>{e}</code></blockquote>",
            parse_mode="HTML"
        )


# /getidfb – lấy UID Facebook từ link
@bot.message_handler(commands=['getidfb'])
def getidfb(message):
    try:
        # Tách tham số link sau lệnh
        parts = message.text.split(" ", 1)

        # Nếu user chưa nhập link
        if len(parts) < 2:
            bot.send_message(
                message.chat.id,
                "<blockquote>❌ Vui lòng nhập link Facebook!\n\nVí dụ:\n<code>/getidfb https://facebook.com/zuck</code></blockquote>",
                parse_mode="HTML"
            )
            return

        fb_link = parts[1].strip()

        # API lấy UID
        api_url = f"https://keyherlyswar.x10.mx/Apidocs/getuidfb.php?link={fb_link}"
        response = requests.get(api_url).json()

        uid = response.get("uid")

        bot.send_message(
            message.chat.id,
            f"""<blockquote>🔎 <b>TRA UID FACEBOOK</b></blockquote>\n
<blockquote>📥 Đang xử lý link:\n{fb_link}</blockquote>""",
            parse_mode="HTML"
        )

        # Nếu có UID trả về
        if uid:
            bot.send_message(
                message.chat.id,
                f"""<blockquote>✅ <b>TRA UID THÀNH CÔNG</b>\n
🔗 Link: {fb_link}
🆔 UID: <code>{uid}</code></blockquote>""",
                parse_mode="HTML"
            )
        else:
            bot.send_message(
                message.chat.id,
                "<blockquote>❌ Không lấy được UID từ API!</blockquote>",
                parse_mode="HTML"
            )

    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"<blockquote>⚠️ Lỗi khi gọi API:\n<code>{e}</code></blockquote>",
            parse_mode="HTML"
        )



# /videogai – lấy video gái random
@bot.message_handler(commands=['videogai'])
def videogai(message):
    try:
        api_url = "https://keyherlyswar.x10.mx/Apidocs/videogai.php"
        response = requests.get(api_url).json()
        video_url = response.get("url")

        if video_url:
            bot.send_message(
                message.chat.id,
                f"""👧 <b>VIDEO GÁI RANDOM</b>\n
<blockquote>📥 Đang gửi video cho bạn...</blockquote>""",
                parse_mode="HTML"
            )

            bot.send_video(
                message.chat.id,
                video_url,
                caption="💕 Video gái random"
            )

        else:
            bot.send_message(message.chat.id, "❌ API không trả về video!")

    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"⚠️ Lỗi khi gọi API:\n<code>{e}</code>",
            parse_mode="HTML"
        )

# /videoanime – gọi API và gửi video anime ngẫu nhiên
@bot.message_handler(commands=['videoanime'])
def videoanime(message):
    try:
        # API gọi trực tiếp trong lệnh
        api_url = "https://keyherlyswar.x10.mx/Apidocs/videoanime.php"
        response = requests.get(api_url).json()
        video_url = response.get("url")

        if video_url:
            bot.send_message(
                message.chat.id,
                f"""🎬 <b>VIDEO ANIME RANDOM</b>\n
<blockquote>📥 Đang gửi video anime cho bạn...</blockquote>""",
                parse_mode="HTML"
            )

            bot.send_video(
                message.chat.id,
                video_url,
                caption="✨ Anime Video"
            )

        else:
            bot.send_message(message.chat.id, "❌ Không Có Video Tại Thời Điểm Này!")

    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"⚠️ Lỗi khi gọi API:\n<code>{e}</code>",
            parse_mode="HTML"
        )




# /admin – giới thiệu admin
@bot.message_handler(commands=['admin'])
def admin(message):
    bot.reply_to(message, f"""📑<b>THÔNG TIN ADMIN</b>\n
<blockquote> Admin Bot 🎉</blockquote>\n
<blockquote> Tên: Đặng Đức Tuyển \n
Facebook: https://www.facebook.com/ductuyen.737165 \n
Telegram: @ductuyendev \n
GitHub: https://github.com/Dangductuyen \n
Website Buff MXH: https://ductuyensub.site \n
Profile: https://ductuyen-info.pages.dev \n
</blockquote>
""",
                     parse_mode="HTML")





print("Bot đang chạy...")
bot.infinity_polling()
