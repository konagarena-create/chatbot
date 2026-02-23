import os
import re
import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ================== TOKEN ==================
BOT_TOKEN = os.getenv("8354054394:AAFaH11TE2p3Wht8Z7XmLo0P8p9OVKw-9B8")
bot = telebot.TeleBot(BOT_TOKEN)

# ================== GOOGLE SHEETS ==================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
{
  "type": "service_account",
  "project_id": "focus-reality-488313-f9",
  "private_key_id": "4ed26a768622ae08dde11111560cab067a20ee5a",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDXRGxH+TwUJK+B\nOwBre+7HQN7xy9tyTaD3Hzx3muQeEYUJGpYMcZ0lDEAXY4V0VrwOeHpFArveGeCJ\nk+GZrE/XKJrxX5DKY8ObrA/d1lBWNDlWN7jF50HGpCrUAvLheaWqBPBJYQEc2Tfh\nE2bk5aFPfeZQLOQ+MuYkhGkgcXOqNlKZ2itswqv1ugTdvOvhEh8/hoG6bvZ5aNvQ\nXXCgtRSu2rJ1/ol46bjQkMd+hYLjv6618B0qGpkHPKoLOGiZyqa7o3oTKD8MQ8Zt\nC2xqdU27JXYCXXVD1zk8p9sdj111zIdVLnKHmgrf5zzNR4GoZj/XPBY0Juzyf3Ow\naI4DbrJdAgMBAAECggEAEs0rF+4wzSGXIpZgpwKgDE8iKcRAWm9lS7Ayu8+PdQDa\nubzUtimGLCIxxtkuYsbgjfL/2t8uQWvJLLr5zU47evNU9Rf/sW2dPA9/I0UAp0bQ\nazNatA5KtGrKQtIvHHpfecYMppwOWNKwCryDFCLqP+MjJoWFOdmAOFhIRkkibQ9A\nhKyfrnnuNbaulQnjhBSLgNuJDbISG4VgACV/XSUNUkXw16Tu+FlwNVpNHeX4/eKJ\nhlUWUC9wmSZL5YbwjBvh8NR0se7QjsAVDFTPzmZtLNHjnwZv7DhOBqV5VNOwSwY9\nA8baDAm40s/DMw1YPh8tXPMLTUaC0lHmfsErshJ3AQKBgQD0xZ3HZWEWLryqXd4g\nKYQpH37DNCy+5p13iMuvdVigu6fOU3Ezs3az2JivF354FronxEdJDsFqVKgTyFRD\nc3WvAbgyCCwwcxPys0bmRZG1jRnC5SQAA8fYnRb4CaNwOSb8WfiFp32PNXQtU0Fs\nsmnYqUN6moI/6EXlKAUKWx9U7QKBgQDhJFSGmJKSZOoyzA8Spo6ESNyLe+v/ggBd\nxXHu2Tq10FjbTFWU3Tlj1mdCE4Ybn5plGAFaZpXLBrX+YvcxtwoY+BFRauUMBhsV\ninS69CEnVIzXvzZI8bGJGcYy8P3EJf4YOAqNCXJQhy5GRZU66SGi7NW2Pcnhxu19\nVFhQK1gVMQKBgQDPF0NeqI9zzScinTiJzZZblKITVdllyof/0mVCle3eT+ax0jc8\nnuIXV3IW8bG2uMPXUWFelnVeGTH7SsrAJrey0amd6vw4IaUG+ldKDCIzkKXzFxtW\nR9yVkJMWWFFHaZNqflSeAA9jUr5wergn1utmvA6zdHYuy74XG7zn/iCMIQKBgFG+\nch4oeVdD4rCs3HAmHyqylbjjNo2fsuhZDwPsxV9MFWcSMSSKqhKwvu8DzbZr3ZAF\nBkC/bHW5qwyA/EWFstnb/9Wy3RTfhqfsjHNwvjTcgwK2f0w+zPn9bLQEQe8c6EP8\n3P/WRTYtzsRe8U7hZIAWQ4YWqx0ZsBLINARvqFyRAoGBAJWOTg8KGhYGQJIKwQ6d\nsh7TfMyi4OJXUUq2ae0gbbCSSmQTKA3zAhwXU+pTxoxgFbd6ZZsJESlcqWCRMmGh\nAEirUZo70D0fGlSk+nI8kZpjOtGyEGAQI7ZeCwyf0R6LwJTMxuP2eU5v9QCbYbgJ\ncXiCT53TNBo4qpjmVxLujYEn\n-----END PRIVATE KEY-----\n",
  "client_email": "bot-sheets@focus-reality-488313-f9.iam.gserviceaccount.com",
  "client_id": "107242277645726690444",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bot-sheets%40focus-reality-488313-f9.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

client = gspread.authorize(creds)
sheet = client.open("BaoCaoCaTruc").sheet1


# ================== HÀM TIỆN ÍCH ==================

def get_value(label, text):
    pattern = rf"{label}:\s*(.+)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def sum_con(text):
    """
    Chỉ lấy số đứng trước chữ 'mức'
    Ví dụ:
    3 mức 1, 2 mức 2, 2 mức 3 -> 7
    """
    matches = re.findall(r"(\d+)\s*mức", text.lower())
    if matches:
        return sum(int(m) for m in matches)

    numbers = re.findall(r"\d+", text)
    return sum(int(n) for n in numbers)


def parse_toc_do(text):
    match = re.search(r"(\d+)\s*biên bản.*?(\d+)\s*nguội", text, re.IGNORECASE)
    if match:
        return int(match.group(1)), int(match.group(2))
    return 0, 0


# ================== LỆNH TỔNG NGÀY ==================

@bot.message_handler(commands=['tongngay'])
def tong_ngay(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Vui lòng nhập: /tongngay dd/mm/yyyy")
            return

        ngay_can_tinh = parts[1]
        data = sheet.get_all_values()

        tong_bb = tong_con = tong_qkqt = 0
        tong_tocdo_bb = tong_tocdo_nguoi = 0
        tong_khac = tong_gplx = tong_tamgiu = 0

        for row in data[1:]:
            if row[0] == ngay_can_tinh:
                tong_bb += int(row[3] or 0)
                tong_con += int(row[4] or 0)
                tong_qkqt += int(row[5] or 0)
                tong_tocdo_bb += int(row[6] or 0)
                tong_tocdo_nguoi += int(row[7] or 0)
                tong_khac += int(row[10] or 0)
                tong_gplx += int(row[12] or 0)
                tong_tamgiu += int(row[13] or 0)

        msg = f"""📊 TỔNG NGÀY {ngay_can_tinh}

BB: {tong_bb}
Cồn: {tong_con}
QKQT: {tong_qkqt}
Tốc độ: {tong_tocdo_bb} biên bản, {tong_tocdo_nguoi} nguội
Khác: {tong_khac}
GPLX: {tong_gplx}
Tạm giữ: {tong_tamgiu}
"""
        bot.reply_to(message, msg)

    except Exception as e:
        bot.reply_to(message, f"Lỗi: {e}")


# ================== NHẬN BÁO CÁO ==================

@bot.message_handler(func=lambda m: m.text and "Ngày:" in m.text)
def handle_report(message):
    try:
        text = message.text

        ngay = get_value("Ngày", text)
        ca = get_value("Ca", text)
        to = get_value("Tổ", text)
        bb = int(get_value("Bb", text) or 0)

        con_raw = get_value("Cồn", text)
        con = sum_con(con_raw)

        qkqt = int(get_value("QKQT", text) or 0)

        toc_do_raw = get_value("Tốc độ", text)
        toc_do_bb, toc_do_nguoi = parse_toc_do(toc_do_raw)

        xe_khach = int(get_value("Xe khách", text) or 0)
        vach = int(get_value("Vạch kẻ đường", text) or 0)
        khac = int(get_value("Khác", text) or 0)
        hoc_sinh = int(get_value("Học sinh", text) or 0)
        gplx = int(get_value("GPLX", text) or 0)
        tam_giu = int(get_value("Tạm giữ", text) or 0)

        dkp_raw = get_value("DKP", text)
        dkp = dkp_raw.replace(",", ".") if dkp_raw else "0"

        row = [
            ngay, ca, to, bb,
            con, qkqt,
            toc_do_bb, toc_do_nguoi,
            xe_khach, vach,
            khac, hoc_sinh,
            gplx, tam_giu,
            dkp
        ]

        sheet.append_row(row)

        bot.reply_to(message, "✅ Đã lưu báo cáo thành công!")

    except Exception as e:
        bot.reply_to(message, f"Lỗi xử lý báo cáo: {e}")


# ================== CHẠY BOT ==================

if __name__ == "__main__":
    print("Bot running...")
    bot.infinity_polling()


