import telebot 
from sql import SqlRequests as SR

bot = telebot.TeleBot('1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ')
data = SR()


#Reply_Keyboard_Creator
def reply_keyboard_creator(all_buttons, one_time_keyboard: bool = None):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time_keyboard) 
    for one_row in all_buttons:
        row_bottons = []
        for button in one_row:
                row_bottons.append(button)
        keyboard.row(*row_bottons)

    return keyboard




def main():
    @bot.message_handler(commands=['start'])
    def start_command(message):
        if not data.check_member_exist(message.chat.id):
            welcome_message = data.get_bot_messages('after_start_new', 'eng')
            choose_lang_list = data.get_bot_messages(message='langs')
            lang_list_for_create_button = [[i[1] for i in choose_lang_list.items()]]

            buttons = reply_keyboard_creator(all_buttons=lang_list_for_create_button, one_time_keyboard=False)
            bot.send_message(message.chat.id, welcome_message, reply_markup=buttons)
        else:
            pass



    bot.polling()




if __name__ == "__main__":
    main()
