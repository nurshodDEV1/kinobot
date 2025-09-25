# 🎬 Kino Bot

Bu Telegram bot kino kodlari orqali kinolarni tarqatish uchun mo'ljallangan.

## ✨ Xususiyatlar

- 🔒 Majburiy kanal a'zoligi tekshiruvi
- 🎬 Kino kodlari orqali kino yuborish
- 👨‍💼 Admin panel
- 📊 Statistika
- 🌐 Ko'p tilli qo'llab-quvvatlash

## 🚀 O'rnatish

### Lokal o'rnatish:

1. **Repozitoriyani klonlash:**
```bash
git clone <repository-url>
cd kino-bot
```

2. **Kerakli kutubxonalarni o'rnatish:**
```bash
pip install -r requirements.txt
```

3. **Environment variables sozlash:**
- `.env` faylida `BOT_TOKEN` va `ADMIN_ID` ni o'zgartiring

4. **Botni ishga tushirish:**
```bash
python bot.py
```

### Railway.ga deploy qilish:

1. **Railway.app saytiga kiring**
2. **Yangi project yarating**
3. **GitHub repositoriyani ulang**
4. **Environment variables larni Railway sozlamalarida qo'shing:**
   - `BOT_TOKEN` - @BotFather dan olingan token
   - `ADMIN_ID` - Admin user ID
   - `CHANNELS` - Kanallar ro'yxati JSON formatida

5. **Deploy avtomatik boshlanadi**

## ⚙️ Sozlash

### Bot Token olish:
1. @BotFather ga murojaat qiling
2. `/newbot` komandasi bilan yangi bot yarating
3. Token ni `.env` fayliga qo'ying

### Environment Variables:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_admin_id_here
CHANNELS=[{"username": "@your_channel", "title": "Kanal Nomi"}]
```

### Kanallar qo'shish:
`CHANNELS` environment variable da kanallaringizni JSON formatida qo'shing:

```json
[{"username": "@your_channel", "title": "Kanal Nomi"}]
```

### Kino qo'shish:
`movies.json` fayliga yoki admin komandalar orqali:

```json
{
    "001": {
        "file_id": "BAACAgIAAxkDAAI...",
        "title": "Film nomi"
    }
}
```

## 🎯 Foydalanish

### Oddiy foydalanuvchi:
1. Botni ishga tushiring
2. Barcha kanallarga a'zo bo'ling
3. Kino kodini yuboring (masalan: `001`)

### Admin komandalar:
- `/add_movie 001 file_id Film nomi` - Yangi kino qo'shish
- `/del_movie 001` - Kinoni o'chirish
- `/list_movies` - Barcha kinolar
- `/stats` - Statistika

## 📁 Fayl tuzilishi

```
kino-bot/
├── bot.py              # Asosiy bot fayli
├── .env                # Environment variables
├── movies.json         # Kino ma'lumotlari
├── requirements.txt    # Python kutubxonalar
├── railway.json        # Railway konfiguratsiya
├── nixpacks.Dockerfile # Docker fayl
├── README.md          # Dokumentatsiya
└── admin.py           # Admin funksiyalar (ixtiyoriy)
```

## 🛠️ Muammolarni hal qilish

### Bot ishlamayapti:
- Token to'g'riligini tekshiring
- Internet aloqasini tekshiring
- Python versiyasini tekshiring (3.7+)

### Kanallar ishlamayapti:
- Bot kanal admini ekanligini tekshiring
- Kanal username to'g'riligini tekshiring
- Kanal ochiq/private ekanligini tekshiring

### Kinolar yuborilmayapti:
- File ID to'g'riligini tekshiring
- Fayl hajmi limitini tekshiring
- Bot ruxsatlarini tekshiring

## 🤝 Yordam

Savollar yoki muammolar bo'lsa:
- Issue yarating
- Dokumentatsiyani o'qing
- Admin bilan bog'laning

## 📄 Litsenziya

MIT License