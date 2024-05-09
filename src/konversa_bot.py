from os import getenv

API_TOKEN = getenv("TELEGRAM_API_TOKEN")
if not API_TOKEN:
    print("You should put TELEGRAM_API_TOKEN environment variable first")
    exit(1)

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

import konversa

dp = Dispatcher()

intent_engine = konversa.IntentEngine('dataset.csv')
intent_engine.train_intent()
cm = konversa.ConversationManager()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler will be called when user sends `/start` command
    """
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    user_full_name = message.from_user.full_name

    cm.set_user_data("user_id", user_id)
    cm.set_user_data("user_name", user_name)
    cm.set_user_data("user_first_name", user_first_name)
    cm.set_user_data("user_last_name", user_last_name)
    cm.set_user_data("user_full_name", user_full_name)

    await message.answer(f"Hello, {html.bold(user_full_name)}!")

@dp.message()
async def echo_handler(message: Message) -> None:
    
    f_name = cm.get_user_data("user_first_name")
    l_name = cm.get_user_data("user_last_name")

    the_intent = intent_engine.classify_intent(message.text)

    cp = konversa.ConversationProcessor()

    match the_intent[0][0]:
        case "question_who":

            the_data = {}
            ner = intent_engine.get_ner(message.text, False)
            the_data['person_name'] = ner

            the_reply = cp.answer_who(the_data)

        case "reserve_meeting":

            if not cm.get_user_data("session"):
                cm.set_user_data("session", "reserve_meeting")
                cm.set_user_data("session_order", 'begin')
                cm.set_user_data("session_end", False)

                the_reply = cp.reserve_meeting_respond('begin')

            else:

                the_reply = "Meeting reservation in progress"

        case _:

            if not cm.get_user_data("session"):
                the_reply = "I don't understand what you mean, could you rephrase?"
            else:
                order = cm.get_user_data("session_order")
                if order == 'begin':
                    current_order = 1
                    current_order_str = str(current_order)
                    cm.set_user_data("session_order",current_order_str)
                else:
                    current_order = int(order) + 1
                    current_order_str = str(current_order)
                    cm.set_user_data("session_order",current_order_str)

                the_reply = cp.reserve_meeting_respond(current_order_str)

    await message.answer(the_reply)

async def main() -> None: 
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
