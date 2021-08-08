import telebot
from sql import SqlRequests as SR

#pymysql.err.OperationalError: (2013, 'Lost connection to MySQL server during query')


bot = telebot.TeleBot('1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ')


def main():
    @bot.message_handler(commands=['start'])
    def start_command(message):
        ms = 'hello, send photo'
        bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAITrmEODO7STFiWh7u9km0k-GdqETv_AAKYsjEbXINwSEEu1WhpZkViAQADAgADbQADIAQ', caption='hello')

        #msg = bot.send_message(message.chat.id, ms)
        #bot.register_next_step_handler(msg, photo)

    def photo(message):
        bot.send_message()
        print(message)

    bot.polling()



if __name__ == "__main__":
    main()

