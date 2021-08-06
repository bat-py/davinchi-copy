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
            buttons = reply_keyboard_creator(all_buttons=lang_list_for_create_button, one_time_keyboard=True)
            
            msg = bot.send_message(message.chat.id, welcome_message, reply_markup=buttons)
            bot.register_next_step_handler(msg, askLang)
        else:
            pass


# Works if members didn't choose one of the language button 
    def askLang(message):
        answear = message.text
        chat_id = message.chat.id
        if answear == '🇷🇺 Начать':
            data.insert_id_lang(chat_id, 'ru')

        elif answear == '🇺🇸 Start':
            data.insert_id_lang(chat_id, 'eng')
        elif answear == '🇺🇦 Почати':
            data.insert_id_lang(chat_id, 'uk')
        else:
            warning_message = data.get_bot_messages(message='warning_choose_lang', lang='eng')

            choose_lang_list = data.get_bot_messages(message='langs')
            lang_list_for_create_button = [[i[1] for i in choose_lang_list.items()]]
            buttons = reply_keyboard_creator(all_buttons=lang_list_for_create_button, one_time_keyboard=True)
            
            msg = bot.send_message(chat_id, warning_message, reply_markup=buttons)
            bot.register_next_step_handler(msg, askLang)

# Ask member's age
    def askAge(message):
        lang = data.get_lang(message.chat.id)
        members_name = message.chat.first_name

        



# Ask member's name and creates button with member's name
    def askName(message):
        pass


    bot.polling()




if __name__ == "__main__":
    main()
