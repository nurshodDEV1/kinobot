# 🎬 Kino Bot

Bu Telegram bot kino kodlari orqali kinolarni tarqatish uchun mo'ljallangan.

## ✨ Xususiyatlar

- 🔒 Majburiy kanal a'zoligi tekshiruvi
- 🎬 Kino kodlari orqali kino yuborish
- 👨‍💼 Admin panel
- 📊 Statistika
- 🌐 Ko'p tilli qo'llab-quvvatlash

## 🚀 O'rnatish

1. **Repozitoriyani klonlash:**
```bash
git clone <repository-url>
cd kino-bot
```

2. **Kerakli kutubxonalarni o'rnatish:**
```bash
pip install -r requirements.txt
```

3. **Bot sozlamalari:**
- `config.py` faylida `BOT_TOKEN` ni o'zgartiring
- Kanallar ro'yxatini to'ldiring
- Admin ID ni belgilang

4. **Botni ishga tushirish:**
```bash
python bot.py
```

## ⚙️ Sozlash

### Bot Token olish:
1. @BotFather ga murojaat qiling
2. `/newbot` komandasi bilan yangi bot yarating
3. Token ni `config.py` ga qo'ying

### Kanallar qo'shish:
`config.py` faylida `CHANNELS` ro'yxatiga kanallaringizni qo'shing:

```python
CHANNELS = [
    {
        "username": "@your_channel",
        "title": "Kanal Nomi",
        "id": -1001234567890
    }
]
```

### Kino qo'shish:
`movies.json` fayliga yoki admin komandalar orqali:

```json
{
    "KINO001": {
        "file_id": "BAACAgIAAxkDAAI...",
        "title": "Film nomi"
    }
}
```

## 🎯 Foydalanish

### Oddiy foydalanuvchi:
1. Botni ishga tushiring
2. Barcha kanallarga a'zo bo'ling
3. Kino kodini yuboring (masalan: `KINO001`)

### Admin komandalar:
- `/add_movie KINO001 file_id Film nomi` - Yangi kino qo'shish
- `/del_movie KINO001` - Kinoni o'chirish
- `/list_movies` - Barcha kinolar
- `/stats` - Statistika

## 📁 Fayl tuzilishi

```
kino-bot/
├── bot.py              # Asosiy bot fayli
├── config.py           # Sozlamalar
├── movies.json         # Kino ma'lumotlari
├── requirements.txt    # Python kutubxonalar
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