import logging

from aiogram import Bot, Dispatcher, executor, types

import konversa

API_TOKEN = "2091428419:AAG4kwTpFcwv7rYozl5zHae-NmotTog5_AY"

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

intent_engine = konversa.IntentEngine('dataset.csv')
intent_engine.train_intent()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm Konversa Bot, pleased to meet you!")

@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
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
        the_reply = 'Hi ' + f_name + ' ' + l_name + '!\n' + intent_engine.get_ner(message.text) + 'Your intention: ' + the_intent[0][0]

    conv_processor = konversa.ConversationProcessor(the_intent[0][0])

    x = conv_processor.get_steps()
    print(x)

    for a in x:
        the_reply = the_reply + a

    the_reply = the_reply + ' nos = ' + str(conv_processor.get_number_of_steps())

    await message.answer(the_reply)

if __name__ == '__main__':

    print("Konversa Bot: started ...")
    executor.start_polling(dp, skip_updates=True)
    print("Konversa Bot: finished ...")

