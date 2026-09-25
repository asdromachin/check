import requests
from datetime import datetime

def check_token(token):
    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("ok"):
            return data["result"]
        return None
    except:
        return None

def main():
    print("=" * 55)
    print("چک کردن توکن ربات‌های تلگرام")
    print("=" * 55)
    print("همه توکن‌ها رو یکجا پیست کن (هر توکن در یک خط)")
    print("وقتی تموم شد دو بار Enter بزن:\n")

    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "" and lines and lines[-1].strip() == "":
                break
            lines.append(line)
        except EOFError:
            break

    # جدا کردن توکن‌ها
    text = "\n".join(lines)
    tokens = []
    for part in text.replace(",", "\n").replace(" ", "\n").split("\n"):
        token = part.strip()
        if token and ":" in token:  # توکن تلگرام معمولاً : داره
            tokens.append(token)

    # حذف تکراری‌ها
    tokens = list(dict.fromkeys(tokens))

    if not tokens:
        print("هیچ توکن معتبری پیدا نشد.")
        return

    print(f"\n{len(tokens)} توکن پیدا شد. در حال بررسی...\n")

    valid_bots = []
    invalid_count = 0

    for i, token in enumerate(tokens, 1):
        print(f"[{i}/{len(tokens)}] چک می‌کنم...", end=" ")
        bot_info = check_token(token)

        if bot_info:
            name = bot_info.get("first_name", "نامشخص")
            username = bot_info.get("username", "ندارد")
            bot_id = bot_info.get("id", "ندارد")
            print(f"✅ {name} | @{username}")
            valid_bots.append({
                "name": name,
                "username": username,
                "id": bot_id,
                "token": token
            })
        else:
            print("❌ اشتباه")
            invalid_count += 1

    # ذخیره فایل
    filename = f"valid_bots_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("لیست ربات‌های معتبر\n")
        f.write(f"تاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        f.write("توجه: تلگرام امکان گرفتن تعداد اعضای ربات را نمی‌دهد.\n")
        f.write("=" * 50 + "\n\n")

        if valid_bots:
            for idx, bot in enumerate(valid_bots, 1):
                f.write(f"ربات شماره {idx}\n")
                f.write(f"نام ربات     : {bot['name']}\n")
                f.write(f"یوزرنیم      : @{bot['username']}\n")
                f.write(f"آیدی ربات    : {bot['id']}\n")
                f.write(f"توکن         : {bot['token']}\n")
                f.write(f"تعداد اعضا   : قابل دریافت نیست\n")
                f.write("-" * 45 + "\n\n")
        else:
            f.write("هیچ توکن معتبری پیدا نشد.\n")

    print("\n" + "=" * 55)
    print(f"✅ توکن‌های درست  : {len(valid_bots)}")
    print(f"❌ توکن‌های اشتباه : {invalid_count}")
    print(f"📁 فایل ساخته شد   : {filename}")
    print("=" * 55)

if __name__ == "__main__":
    main()
