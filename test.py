import telebot
from sql import SqlRequests as SR

#pymysql.err.OperationalError: (2013, 'Lost connection to MySQL server during query')


bot = telebot.TeleBot('1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ')


def main():
    @bot.message_handler(commands=['start'])
    def start_command(message):
        ms = 'hello, send photo'
        #bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAITrmEODO7STFiWh7u9km0k-GdqETv_AAKYsjEbXINwSEEu1WhpZkViAQADAgADbQADIAQ', caption='hello')

        sympathy = f"Hello {message.from_user.id}"

        #msg = bot.send_message(message.chat.id, ms)
        bot.send_message(message.chat.id, f'hello <a href="tg://user?id=571777912"> day </a>', parse_mode='html')

    def photo(message):
        bot.send_message()
        print(message)

    bot.polling()



if __name__ == "__main__":
    main()

