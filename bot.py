import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import json
from dotenv import load_dotenv

# .env faylni yuklash
load_dotenv()

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

# Bot token va sozlamalar
BOT_TOKEN = os.getenv('BOT_TOKEN', '7690677258:AAEmVb9VFEEACKYCIliR9N0KT6EPEIBA_Kc')  # @BotFather dan olingan token
ADMIN_ID = int(os.getenv('ADMIN_ID', '5082127676'))  # Admin user ID

# Majburiy kanallar ro'yxati
CHANNELS_JSON = os.getenv('CHANNELS', '[{"username": "@goal10sec", "title": "Obuna 1"}]')
CHANNELS = json.loads(CHANNELS_JSON)

# Bot va dispatcher yaratish
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class MovieBot:
    def __init__(self):
        self.movies_db = {}  # Kino kodlari bazasi
        self.load_movies()
    
    def load_movies(self):
        """Kino ma'lumotlarini yuklash"""
        try:
            if os.path.exists('movies.json'):
                with open('movies.json', 'r', encoding='utf-8') as f:
                    self.movies_db = json.load(f)
        except Exception as e:
            logging.error(f"Kino ma'lumotlarini yuklashda xato: {e}")
    
    def save_movies(self):
        """Kino ma'lumotlarini saqlash"""
        try:
            with open('movies.json', 'w', encoding='utf-8') as f:
                json.dump(self.movies_db, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"Kino ma'lumotlarini saqlashda xato: {e}")
    
    def add_movie(self, code, file_id, title=""):
        """Yangi kino qo'shish"""
        self.movies_db[code] = {
            "file_id": file_id,
            "title": title
        }
        self.save_movies()
    
    def get_movie(self, code):
        """Kino kodiga qarab kino topish"""
        return self.movies_db.get(code.upper())

# MovieBot obyekti yaratish
movie_bot = MovieBot()

async def check_user_subscription(user_id):
    """Foydalanuvchi barcha kanallarga a'zo ekanligini tekshirish"""
    not_subscribed = []
    
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel["username"], user_id)
            # A'zolik statuslarini tekshirish
            if member.status in ['left', 'kicked', 'restricted']:
                not_subscribed.append(channel)
            # Agar status 'member', 'administrator', 'creator' bo'lsa - a'zo hisoblanadi
        except Exception as e:
            # Kanalda foydalanuvchi topilmasa ham a'zo emas deb hisoblaymiz
            logging.error(f"Kanal tekshirishda xato {channel['username']}: {e}")
            not_subscribed.append(channel)
    
    return not_subscribed

def create_subscription_keyboard(channels):
    """A'zo bo'lish tugmalarini yaratish"""
    keyboard = []
    for channel in channels:
        keyboard.append([InlineKeyboardButton(
            text=f"📢 {channel['title']}ga a'zo bo'lish",
            url=f"https://t.me/{channel['username'][1:]}"
        )])
    
    keyboard.append([InlineKeyboardButton(
        text="✅ A'zolikni tekshirish",
        callback_data="check_subscription"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """Start komandasi"""
    user_name = message.from_user.first_name or "Foydalanuvchi"
    welcome_text = f"""
👋 Assalomu alaykum {user_name} botimizga xush kelibsiz.

✍🏻 Kino kodini yuboring.
    """
    
    await message.answer(welcome_text, parse_mode="Markdown")

@dp.callback_query_handler(lambda c: c.data == "search_movie")
async def search_movie_callback(callback: types.CallbackQuery):
    """Kino qidirish callback"""
    # Avval a'zolikni tekshirish
    not_subscribed = await check_user_subscription(callback.from_user.id)
    
    if not_subscribed:
        text = "❌ **Kino olish uchun quyidagi kanallarga a'zo bo'ling:**\n\n"
        keyboard = create_subscription_keyboard(not_subscribed)
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        text = """
✅ **Barcha kanallarga a'zo bo'lgansiz!**
        Kino kodini yuboring.
        """
        await callback.message.edit_text(text, parse_mode="Markdown")

@dp.callback_query_handler(lambda c: c.data == "check_subscription")
async def check_subscription_callback(callback: types.CallbackQuery):
    """A'zolikni tekshirish callback"""
    not_subscribed = await check_user_subscription(callback.from_user.id)
    
    if not_subscribed:
        text = "❌ **Hali ham ba'zi kanallarga a'zo bo'lmadingiz:**\n\n"
        for channel in not_subscribed:
            text += f"• {channel['title']}\n"
        text += "\n👆 A'zo bo'lib, yana tekshiring"
        
        keyboard = create_subscription_keyboard(not_subscribed)
        try:
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
        except Exception as e:
            # Xabar o'zgarmasa xatolik berish
            if "Message is not modified" in str(e):
                pass  # Xabarni yangilash shart emas
            else:
                logging.error(f"Xabar yangilashda xato: {e}")
    else:
        text = """
✅ **Ajoyib! Barcha kanallarga a'zo bo'lgansiz!**

📝 Endi 3 xonali kino kodini yuboring:
• 001, 002, 003
• 123, 456, 789
• va boshqalar...
        """
        try:
            await callback.message.edit_text(text, parse_mode="Markdown")
        except Exception as e:
            # Xabar o'zgarmasa xatolik berish
            if "Message is not modified" in str(e):
                pass  # Xabarni yangilash shart emas
            else:
                logging.error(f"Xabar yangilashda xato: {e}")

@dp.message_handler(content_types=['video', 'document', 'photo', 'audio'])
async def get_file_id(message: types.Message):
    """Fayl ID olish uchun"""
    if message.from_user.id != ADMIN_ID:
        return
    
    # Fayl ID ni aniqlash
    if message.video:
        file_id = message.video.file_id
        file_type = "Video"
    elif message.document:
        file_id = message.document.file_id
        file_type = "Document"
    elif message.photo:
        file_id = message.photo[-1].file_id  # Eng yuqori sifatli rasm
        file_type = "Photo"
    elif message.audio:
        file_id = message.audio.file_id
        file_type = "Audio"
    else:
        await message.answer("❌ Noma'lum fayl turi")
        return
    
    # Ma'lumot yuborish
    info_text = f"""
📥 **File ID olingan!**

📁 **Fayl turi:** {file_type}
🔑 **File ID:** `{file_id}`

📝 **Kino qo'shish uchun:**
`/add_movie 001 {file_id} Film nomi`
    """
    
    await message.answer(info_text, parse_mode="Markdown")
async def debug_command(message: types.Message):
    """Debug uchun - kanal a'zolikni tekshirish"""
    if message.from_user.id != ADMIN_ID:
        return
    
    user_id = message.from_user.id
    debug_text = f"🔍 **Debug ma'lumotlar:**\n\n👤 User ID: `{user_id}`\n\n"
    
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel["username"], user_id)
            debug_text += f"\n📺 **{channel['title']}**\n"
            debug_text += f"   Username: {channel['username']}\n"
            debug_text += f"   Status: {member.status}\n"
            debug_text += f"   Can Join?: {member.can_join_groups if hasattr(member, 'can_join_groups') else 'N/A'}\n"
        except Exception as e:
            debug_text += f"\n❌ **{channel['title']}**\n"
            debug_text += f"   Xato: {str(e)}\n"
    
    await message.answer(debug_text, parse_mode="Markdown")
async def check_my_status(message: types.Message):
    """Foydalanuvchining a'zolik statusini tekshirish (debug uchun)"""
    user_id = message.from_user.id
    status_text = f"👤 **Sizning ID:** `{user_id}`\n\n📋 **Kanallar holati:**\n\n"
    
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel["username"], user_id)
            status = member.status
            
            if status == 'member':
                emoji = "✅"
                status_text += f"{emoji} {channel['title']}: A'zo\n"
            elif status == 'administrator':
                emoji = "👑"
                status_text += f"{emoji} {channel['title']}: Admin\n"
            elif status == 'creator':
                emoji = "👑"
                status_text += f"{emoji} {channel['title']}: Egasi\n"
            elif status == 'left':
                emoji = "❌"
                status_text += f"{emoji} {channel['title']}: A'zo emas\n"
            elif status == 'kicked':
                emoji = "🚫"
                status_text += f"{emoji} {channel['title']}: Bloklangan\n"
            else:
                emoji = "⚠️"
                status_text += f"{emoji} {channel['title']}: {status}\n"
                
        except Exception as e:
            status_text += f"❌ {channel['title']}: Xato - {str(e)}\n"
    
    await message.answer(status_text, parse_mode="Markdown")

@dp.message_handler(commands=['add_movie'])
async def add_movie_command(message: types.Message):
    """Admin uchun kino qo'shish komandasi"""
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda admin huquqi yo'q!")
        return
    
    # Komanda formatini tekshirish
    args = message.text.split(' ', 3)
    if len(args) < 4:
        await message.answer(
            "❌ **Noto'g'ri format!**\n\n"
            "✅ To'g'ri format:\n"
            "`/add_movie 001 file_id Film nomi`\n\n"
            "📝 Misol:\n"
            "`/add_movie 123 BAACAgIAAxk... Spiderman filmi`",
            parse_mode="Markdown"
        )
        return
    
    code = args[1]
    file_id = args[2]
    title = args[3]
    
    # Kod formatini tekshirish
    if not code.isdigit() or len(code) != 3:
        await message.answer(
            "❌ **Kod noto'g'ri!**\n\n"
            "✅ Kod 3 xonali raqam bo'lishi kerak\n"
            "📝 Masalan: 001, 123, 456",
            parse_mode="Markdown"
        )
        return
    
    # Kinoni qo'shish
    movie_bot.add_movie(code, file_id, title)
    
    await message.answer(
        f"✅ **Kino muvaffaqiyatli qo'shildi!**\n\n"
        f"🔑 Kod: `{code}`\n"
        f"🎬 Nomi: {title}\n"
        f"📁 File ID: `{file_id[:20]}...`",
        parse_mode="Markdown"
    )

@dp.message_handler(commands=['del_movie'])
async def del_movie_command(message: types.Message):
    """Admin uchun kinoni o'chirish komandasi"""
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda admin huquqi yo'q!")
        return
    
    args = message.text.split(' ', 1)
    if len(args) < 2:
        await message.answer(
            "❌ **Kod kiritilmadi!**\n\n"
            "✅ To'g'ri format:\n"
            "`/del_movie 001`",
            parse_mode="Markdown"
        )
        return
    
    code = args[1]
    
    if code in movie_bot.movies_db:
        title = movie_bot.movies_db[code].get('title', 'Noma\'lum')
        del movie_bot.movies_db[code]
        movie_bot.save_movies()
        
        await message.answer(
            f"✅ **Kino o'chirildi!**\n\n"
            f"🔑 Kod: `{code}`\n"
            f"🎬 Nomi: {title}",
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            f"❌ **'{code}' kodi topilmadi!**",
            parse_mode="Markdown"
        )

@dp.message_handler(commands=['list_movies'])
async def list_movies_command(message: types.Message):
    """Admin uchun kinolar ro'yxati"""
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda admin huquqi yo'q!")
        return
    
    if not movie_bot.movies_db:
        await message.answer("📝 Hech qanday kino yo'q!")
        return
    
    text = "📋 **Barcha kinolar:**\n\n"
    for code, movie in movie_bot.movies_db.items():
        title = movie.get('title', 'Nomalum')
        text += f"🔑 `{code}` - {title}\n"
    
    await message.answer(text, parse_mode="Markdown")

@dp.message_handler(commands=['admin'])
async def admin_help(message: types.Message):
    """Admin yordam"""
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda admin huquqi yo'q!")
        return
    
    help_text = """
👨‍💼 **Admin komandalar:**

📝 **Kino qo'shish:**
`/add_movie 001 file_id Film nomi`

🗑 **Kino o'chirish:**
`/del_movie 001`

📋 **Kinolar ro'yxati:**
`/list_movies`

❓ **Yordam:**
`/admin`

---

💡 **File ID olish:**
1. Kinoni botga yuboring
2. Forward qiling @userinfobot ga
3. File ID ni nusxalang
    """
    
    await message.answer(help_text, parse_mode="Markdown")

@dp.message_handler()
async def handle_movie_code(message: types.Message):
    """Kino kodini qayta ishlash"""
    # Avval a'zolikni tekshirish
    not_subscribed = await check_user_subscription(message.from_user.id)
    
    if not_subscribed:
        text = "❌ **Kino olish uchun quyidagi kanallarga a'zo bo'ling:**\n\n"
        keyboard = create_subscription_keyboard(not_subscribed)
        try:
            await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
        except Exception as e:
            logging.error(f"Xabar yuborishda xato: {e}")
        return
    
    # Kino kodini tekshirish - faqat raqamlar
    code = message.text.strip()
    
    # Faqat raqamlar ekanligini tekshirish
    if not code.isdigit():
        await message.answer(
            "❌ **Noto'g'ri kod formati!**\n\n"
            "✅ Kino kodi faqat raqamlardan iborat bo'lishi kerak\n"
            "📝 Masalan: 001, 123, 456",
            parse_mode="Markdown"
        )
        return
    
    # Kodning uzunligini tekshirish (3 ta raqam)
    if len(code) != 3:
        await message.answer(
            "❌ **Kod uzunligi noto'g'ri!**\n\n"
            "✅ Kino kodi 3 ta raqamdan iborat bo'lishi kerak\n"
            "📝 Masalan: 001, 123, 456",
            parse_mode="Markdown"
        )
        return
    
    movie = movie_bot.get_movie(code)
    
    if movie:
        try:
            # Kino yuborish
            await message.answer_video(
                video=movie["file_id"],
                caption=f"🎬 **{movie.get('title', 'Kino')}**\n\n🔑 Kod: `{code}`",
                parse_mode="Markdown"
            )
        except Exception as e:
            await message.answer(f"❌ Kino yuborishda xato: {str(e)}")
    else:
        await message.answer(
            f"❌ **'{code}' kodi topilmadi**\n\n"
            "✅ Kod to'g'ri yozilganligini tekshiring\n"
            "📝 Masalan: 001, 123, 456",
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    print("🤖 Bot ishga tushmoqda...")
    executor.start_polling(dp, skip_updates=True)