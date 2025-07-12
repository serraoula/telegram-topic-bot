import os
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ChatType
from aiogram.types import ForumTopicClosed, ForumTopicOpened
from aiogram.utils.token import TokenValidationError

TOKEN = os.getenv("BOT_TOKEN")  # تأكد من تعيين متغير البيئة
TOPICS = {
    0: -1000000000000,  # الأحد: وصف صورة
    1: -1000000000001,  # الإثنين: تمرين كتابة
    2: -1000000000002,  # الثلاثاء: سؤال محادثة
    3: -1000000000003,  # الأربعاء: كلمات يومية
    4: -1000000000004,  # الخميس: فيديو واستماع
    5: -1000000000005,  # الجمعة: مراجعة وتصحيح
    6: -1000000000006,  # السبت: راحة أو دردشة
}

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def manage_topics():
    while True:
        now = datetime.utcnow()
        current_day = now.weekday()
        for day, topic_id in TOPICS.items():
            try:
                if day == current_day:
                    await bot.open_forum_topic(chat_id="@your_channel_or_group", message_thread_id=topic_id)
                else:
                    await bot.close_forum_topic(chat_id="@your_channel_or_group", message_thread_id=topic_id)
            except Exception as e:
                print(f"Error managing topic {topic_id}: {e}")
        await asyncio.sleep(86400)  # كل 24 ساعة

@dp.startup()
async def startup_handler(dispatcher: Dispatcher):
    await manage_topics()

if __name__ == "__main__":
    try:
        import asyncio
        asyncio.run(dp.start_polling(bot))
    except TokenValidationError:
        print("توكن البوت غير صالح. تأكد من BOT_TOKEN.")
