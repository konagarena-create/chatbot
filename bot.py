import telebot
import gspread
import re
from oauth2client.service_account import ServiceAccountCredentials

# ================== TOKEN ==================
BOT_TOKEN = "8354054394:AAFaH11TE2p3Wht8Z7XmLo0P8p9OVKw-9B8"
bot = telebot.TeleBot(BOT_TOKEN)

# ================== GOOGLE SHEETS ==================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope)

client = gspread.authorize(creds)

sheet = client.open("BaoCaoCaTruc").sheet1


# ================== HÀM TIỆN ÍCH ==================

def get_value(label, text):
    pattern = rf"{label}:\s*(.+)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def sum_numbers(text):
    numbers = re.findall(r"\d+", text)
    return sum(int(n) for n in numbers) if numbers else 0


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

        tong_bb = 0
        tong_con = 0
        tong_qkqt = 0
        tong_tocdo_bb = 0
        tong_tocdo_nguoi = 0
        tong_khac = 0
        tong_gplx = 0
        tong_tamgiu = 0

        for row in data[1:]:  # bỏ dòng tiêu đề
            if row[0] == ngay_can_tinh:
                tong_bb += int(row[3])
                tong_con += int(row[4])
                tong_qkqt += int(row[5])
                tong_tocdo_bb += int(row[6])
                tong_tocdo_nguoi += int(row[7])
                tong_khac += int(row[10])
                tong_gplx += int(row[12])
                tong_tamgiu += int(row[13])

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

@bot.message_handler(func=lambda message: message.text and "Ngày:" in message.text)
def handle_report(message):
    try:
        text = message.text

        ngay = get_value("Ngày", text)
        ca = get_value("Ca", text)
        to = get_value("Tổ", text)
        bb = int(get_value("Bb", text) or 0)

        # CỒN → cộng tất cả mức
        con_raw = get_value("Cồn", text)
        con = sum_numbers(con_raw)

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
            ngay,
            ca,
            to,
            bb,
            con,
            qkqt,
            toc_do_bb,
            toc_do_nguoi,
            xe_khach,
            vach,
            khac,
            hoc_sinh,
            gplx,
            tam_giu,
            dkp
        ]

        sheet.append_row(row)

        bot.reply_to(message, "✅ Đã lưu báo cáo thành công!")

    except Exception as e:
        bot.reply_to(message, f"Lỗi xử lý báo cáo: {e}")


# ================== CHẠY BOT ==================

print("Bot đang chạy...")
bot.polling()