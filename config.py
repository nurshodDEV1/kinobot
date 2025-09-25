# Bot konfiguratsiya sozlamalari

# Bot token - @BotFather dan olinadi
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Admin ID - bot egasi
ADMIN_ID = 123456789

# Majburiy kanallar ro'yxati
CHANNELS = [
    {
        "username": "@your_channel1",  # Kanal username'i
        "title": "Birinchi Kanal",    # Kanal nomi
        "id": -1001234567890          # Kanal ID'si (ixtiyoriy)
    },
    {
        "username": "@your_channel2",
        "title": "Ikkinchi Kanal",
        "id": -1001234567891
    },
    {
        "username": "@your_channel3",
        "title": "Uchinchi Kanal",
        "id": -1001234567892
    }
]

# Xabar matnlari
MESSAGES = {
    "welcome": """
🎬 **Kino Bot**ga xush kelibsiz!

📝 **Qanday ishlaydi:**
1. Avval barcha kanallarga a'zo bo'ling
2. Kino kodini yuboring (masalan: KINO001)
3. Kino sizga yuboriladi

🔍 Boshlash uchun pastdagi tugmani bosing
    """,
    
    "not_subscribed": "❌ **Kino olish uchun quyidagi kanallarga a'zo bo'ling:**",
    
    "subscribed": """
✅ **Ajoyib! Barcha kanallarga a'zo bo'lgansiz!**

📝 Endi kino kodini yuboring:
• KINO001, KINO002
• FILM123, FILM456  
• UZBEK001, UZBEK002
• va boshqalar...
    """,
    
    "movie_not_found": """
❌ **Kino kodi topilmadi!**

✅ Kod to'g'ri yozilganligini tekshiring
📝 Masalan: KINO001, FILM123, UZBEK001
    """,
    
    "error": "❌ Xato yuz berdi. Iltimos qaytadan urinib ko'ring.",
    
    "admin_help": """
👨‍💼 **Admin komandalar:**

/add_movie [kod] [file_id] [title] - Yangi kino qo'shish
/del_movie [kod] - Kinoni o'chirish  
/list_movies - Barcha kinolar ro'yxati
/stats - Bot statistikasi
    """
}

# Tugma matnlari
BUTTONS = {
    "search_movie": "🔍 Kino qidirish",
    "check_subscription": "✅ A'zolikni tekshirish",
    "subscribe": "📢 {}ga a'zo bo'lish"
}