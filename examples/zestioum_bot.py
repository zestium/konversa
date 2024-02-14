import telebot

bot = telebot.TeleBot("2091428419:AAG4kwTpFcwv7rYozl5zHae-NmotTog5_AY")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
