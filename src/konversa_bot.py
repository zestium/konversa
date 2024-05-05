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

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler will be called when user sends `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

@dp.message()
async def echo_handler(message: Message) -> None:
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    #
    
    conv_manager = konversa.ConversationManager()

    the_intent = intent_engine.classify_intent(message.text)

    user_id = message.from_user.id
    user_name = message.from_user.username
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name

    conv_manager.set_user_data("user_id", user_id)
    conv_manager.set_user_data("user_name", user_name)
    conv_manager.set_user_data("user_first_name", user_first_name)
    conv_manager.set_user_data("user_last_name", user_last_name)

    f_name = conv_manager.get_user_data("user_first_name")
    l_name = conv_manager.get_user_data("user_last_name")


    if len(the_intent) < 1:
        the_reply = "I don't understand what you mean, could you rephrase?"
    else:

        the_data = []
        ner = intent_engine.get_ner(message.text, False)
        the_data.append(ner)

        #the_reply = 'Hi ' + f_name + ' ' + l_name + '!\nNER: ' + ner + '\nYour intention: ' + the_intent[0][0]

        conv_processor = konversa.ConversationProcessor(the_intent[0][0], the_data)

        the_reply = conv_processor.answer_who()

        #x = conv_processor.get_steps()
        #print(x)

        #for a in x:
        #   the_reply = the_reply + a
        #
        #the_reply = the_reply + ' nos = ' + str(conv_processor.get_number_of_steps())

    await message.answer(the_reply)

async def main() -> None: 
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
