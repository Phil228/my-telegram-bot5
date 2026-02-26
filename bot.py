import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

logging.basicConfig(level=logging.INFO)

# 1. Твой токен
TOKEN = "8263296266:AAH1SUsq7DnOZKeZXqBSK_dOtHpl65Z7N-k"
# 2. Твой ID группы
GROUP_ID = -1003815878569 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для создания быстрых кнопок под полем ввода
def get_main_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text="/start")
    builder.button(text="/information")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# Команда /start
@dp.message(Command("start"), F.chat.type == "private")
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Пришли мне что угодно, и я анонимно отправлю это в группу.\n"
        "Твои сообщения здесь будут удаляться для приватности.",
        reply_markup=get_main_kb()
    )

# Команда /information
@dp.message(Command("information"), F.chat.type == "private")
async def cmd_info(message: types.Message):
    await message.answer(
        "привет меня зовут Петя меня создал Ілля Пухальський\n"
        "каждое твое соопщение будет отпровляца в групу\n"
        "https://web.telegram.org/a/#-1003815878569\n"
        "каждое твое соопщение,фото,видео приватное ни кто не узнает",
        reply_markup=get_main_kb()
    )

# Логика удаления всех чужих сообщений в ГРУППЕ
@dp.message(F.chat.id == GROUP_ID)
async def delete_in_group(message: types.Message):
    try:
        await message.delete()
    except Exception as e:
        logging.error(f"Ошибка удаления в группе: {e}")

# Логика работы в ЛИЧКЕ (Анонимная пересылка)
@dp.message(F.chat.type == "private")
async def anonymous_sender(message: types.Message):
    # Игнорируем текст кнопок, чтобы они сами себя не пересылали
    if message.text in ["/start", "/information"]:
        return

    try:
        # 1. Копируем в группу
        await message.copy_to(chat_id=GROUP_ID)
        
        # 2. Удаляем сообщение пользователя в ЛИЧКЕ с ботом
        await message.delete()
        
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        # Если не удалось удалить или отправить, бот напишет в личку (чтобы ты знал о проблеме)
        await message.answer(f"⚠️ Произошла ошибка: {e}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("🚀 Бот запущен (без лишних уведомлений и с авто-удалением в личке)")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
