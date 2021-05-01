import sentry_sdk
from aiogram.types import Message
from bot import dp, bot
from bot.api import TikTokAPI
from bot.exception import HandleException
from settings import DOWNLOAD_ERROR


platforms = [TikTokAPI()]


@dp.message_handler()
async def get_message(message: Message):
    for api in platforms:
        for video in await api.handle_message(message):
            if video and video.content:
                return await bot.send_video(
                    message.chat.id, video.content, reply_to_message_id=message.message_id
                )
            else:
                sentry_sdk.capture_exception(HandleException(message.text))
                return await bot.send_message(
                    message.chat.id, DOWNLOAD_ERROR, reply_to_message_id=message.message_id
                )
