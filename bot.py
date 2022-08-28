from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ParseMode
from aiogram.utils.markdown import text, bold
import signal
import sys

from config import TOKEN, STUFF_CHATS_ID
from utils import print_info_for_console
# from requests import requests, request_registration, deleting_request
from database import RequestsDb


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = RequestsDb()
db.create_database()


# def signal_handler(signal, frame):
#     db.close_connection()
#     sys.exit(0)
#
#
# signal.signal(signal.SIGINT, signal_handler)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    msg = text("Добро пожаловать, ", message.from_user.username, ", в чат поддержки ",
               bold("RetextAI"), "! Задавайте возникающие вопросы в нашем чате.", sep='')
    await bot.send_message(message.from_user.id, msg, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler()
async def activity(message: types.Message):
    print_info_for_console(message)

    # Клиент или ответ из чата поддержки?
    if message.chat.id not in STUFF_CHATS_ID:
        # Что пишем клиенту
        msg_for_client = "Наш сотрудник уже приступил к решению вопроса. Ожидайте несколько минут."
        await bot.send_message(message.from_user.id, msg_for_client)

        # Что пишем в чат поддержки
        question = message.text
        msg_for_stuff = text("Заявка #", bold(str(message.message_id)), " от ", bold(message.from_user.username),
                             " создал(а) вопрос:\n", question, sep="")
        id_message_in_stuff_group = await bot.send_message(STUFF_CHATS_ID[0], msg_for_stuff, parse_mode=ParseMode.MARKDOWN)

        # Регистрация вопроса
        db.add_request(id_message_in_stuff_group.message_id, message.from_user.username, message.from_user.id)

    elif message.chat.id in STUFF_CHATS_ID:
        # Если поддержка ответила на сообщение
        if message.reply_to_message != None:
            # И если это сообщение вообще наше и тот запрос актуален
            forwared_message_id = message.reply_to_message.message_id
            if db.existence_request(forwared_message_id):
                # Письмо клиенту
                answer = message.text
                name_client, id_client = db.find_name_client_for_request(forwared_message_id)
                msg_for_client = text(name_client,
                                      ",\n\n", answer, "\n\nНадеемся, наш ответ вам помог :3\n"
                                                       "Задавайте возникающие вопросы в нашем чате.", sep='')
                await bot.send_message(id_client, msg_for_client)

                # сообщение чату поддержки об отправке ответа клиенту
                msg_for_stuff = text("Сообщение было отправлено",
                                     name_client)
                await message.reply(msg_for_stuff)

                # Удаление вопроса из очереди
                db.remove_request(forwared_message_id)


if __name__ == '__main__':
    executor.start_polling(dp)
