import telebot
import konversa

bot = telebot.TeleBot("2091428419:AAG4kwTpFcwv7rYozl5zHae-NmotTog5_AY")


@bot.message_handler(func=lambda message: True)
def echo_all(message):

    # intent = konversa.IntentEngine(message.text)
    conv_manager = konversa.ConversationManager()

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

    the_reply = 'Hi ' + f_name + ' ' + l_name + '!'

    # bot.reply_to(message, intent.get_ner())
    bot.reply_to(message, the_reply)


print("Zestium Bot: started ...")
bot.infinity_polling()
print("Zestium Bot: finished ...")
