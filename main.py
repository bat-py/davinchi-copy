import telebot 

bot = telebot.TeleBot('1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ')

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "I'll find you a true love or new friends!\nMay I ask smth?")




bot.polling()
