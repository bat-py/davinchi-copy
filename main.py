import mimetypes

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
#        if data.check_member_exist(message.chat.id):
#            data.del_member(message.chat.id)
#        else:
        welcome_message = data.get_bot_messages('after_start_new', 'eng')

        choose_lang_list = data.get_bot_messages(message='langs')
        lang_list_for_create_button = [[i[1] for i in choose_lang_list.items()]]
        buttons = reply_keyboard_creator(all_buttons=lang_list_for_create_button, one_time_keyboard=True)

        msg = bot.send_message(message.chat.id, welcome_message, reply_markup=buttons)
        bot.register_next_step_handler(msg, askLang)


# Works if members didn't choose one of the language button
    def askLang(message):
        answear = message.text
        chat_id = message.chat.id
        if answear == '🇷🇺 Начать':
            data.insert_id_lang(chat_id, 'ru')
            bot_message = data.get_bot_messages('age', 'ru')

        elif answear == '🇺🇸 Start':
            data.insert_id_lang(chat_id, 'eng')
            bot_message = data.get_bot_messages('age', 'eng')

        elif answear == '🇺🇦 Почати':
            data.insert_id_lang(chat_id, 'uk')
            bot_message = data.get_bot_messages('age', 'uk')
        else:
            warning_message = data.get_bot_messages(message='warning_choose_lang', lang='eng')

            choose_lang_list = data.get_bot_messages(message='langs')
            lang_list_for_create_button = [[i[1] for i in choose_lang_list.items()]]
            buttons = reply_keyboard_creator(all_buttons=lang_list_for_create_button, one_time_keyboard=True)

            msg = bot.send_message(chat_id, warning_message, reply_markup=buttons)
            bot.register_next_step_handler(msg, askLang)


        msg = bot.send_message(message.chat.id, bot_message)
        bot.register_next_step_handler(msg, askAge)


# Ask member's age
    def askAge(message):
        lang = data.get_lang(message.chat.id)
        try:
            age = int(message.text)
            data.update_member_info(message.chat.id, age=age)
        except:
            members_name = message.chat.first_name
            name_button = reply_keyboard_creator([[members_name]], one_time_keyboard=True)
            wrong_age = data.get_bot_messages('wrong_age', lang)
            msg = bot.send_message(message.chat.id, wrong_age, reply_markup=name_button)
            bot.register_next_step_handler(msg, askAge)

        ask_gender_message = data.get_bot_messages('gender', lang=lang)
        button_man = data.get_bot_messages('button_man', lang=lang)
        button_girl = data.get_bot_messages('button_girl', lang=lang)
        buttons = reply_keyboard_creator([[button_man, button_girl]], one_time_keyboard=False)
        msg = bot.send_message(message.chat.id, ask_gender_message, reply_markup=buttons)
        bot.register_next_step_handler(msg, askGender)


    def askGender(message):
        lang = data.get_lang(message.chat.id)
        gender = message.text

        if gender == data.get_bot_messages('button_man', lang=lang):
            man = data.get_bot_messages('man', lang=lang)
            data.update_member_info(message.chat.id, gender=man)
        elif gender == data.get_bot_messages('button_girl', lang=lang):
            girl = data.get_bot_messages('girl', lang=lang)
            data.update_member_info(message.chat.id, gender=girl)
        else:
            wrong_gender = data.get_bot_messages('wrong_gender', lang=lang)
            msg = bot.send_message(message.chat.id, wrong_gender)
            bot.register_next_step_handler(msg, askGender)

        ask_interested = data.get_bot_messages('interested', lang=lang)
        interested_button_man = data.get_bot_messages('interested_button_man', lang=lang)
        interested_button_girl = data.get_bot_messages('interested_button_girl', lang=lang)
        interested_button_all = data.get_bot_messages('interested_button_all', lang=lang)
        interested_buttons = reply_keyboard_creator([[interested_button_girl, interested_button_man, interested_button_all]], one_time_keyboard=True)
        msg = bot.send_message(message.chat.id, ask_interested, reply_markup=interested_buttons)
        bot.register_next_step_handler(msg, askInterested)

    def askInterested(message):
        lang = data.get_lang(message.chat.id)
        interested = message.text

        interested_list = [data.get_bot_messages('interested_button_man', lang=lang),
                           data.get_bot_messages('interested_button_girl', lang=lang),
                           data.get_bot_messages('interested_button_all', lang=lang)
                           ]
        if interested in interested_list:
            data.update_member_info(message.chat.id, interested=interested)

            which_city = data.get_bot_messages(message='which_city', lang=lang)
            msg = bot.send_message(message.chat.id, which_city)
            bot.register_next_step_handler(msg, askCity)
        else:
            wrong_interested = data.get_bot_messages('wrong_interested', lang=lang)
            interested_button_man = data.get_bot_messages('interested_button_man', lang=lang)
            interested_button_girl = data.get_bot_messages('interested_button_girl', lang=lang)
            interested_button_all = data.get_bot_messages('interested_button_all', lang=lang)
            interested_buttons = reply_keyboard_creator([[interested_button_girl, interested_button_man, interested_button_all]], one_time_keyboard=True)
            msg = bot.send_message(message.chat.id, wrong_interested, reply_markup=interested_buttons)
            bot.register_next_step_handler(msg, askInterested)



    def askCity(message):
        lang = data.get_lang(message.chat.id)
        city = message.text

        if city:
            data.update_member_info(message.chat.id, city=city)
            members_name = message.chat.first_name
            name_button = reply_keyboard_creator([[members_name]], one_time_keyboard=False)
            get_name_message = data.get_bot_messages('get_name', lang=lang)
            msg = bot.send_message(message.chat.id, get_name_message, reply_markup=name_button)
            bot.register_next_step_handler(msg, askName)
        else:
            which_city = data.get_bot_messages(message='which_city', lang=lang)
            msg = bot.send_message(message.chat.id, which_city)
            bot.register_next_step_handler(msg, askCity)


    # Ask member's name and creates button with member's name
    def askName(message):
        lang = data.get_lang(message.chat.id)
        name = message.text

        if name:
            data.update_member_info(message.chat.id, name=name)
            about = data.get_bot_messages('about', lang=lang)
            skip_button_text = data.get_bot_messages('skip_button', lang=lang)
            skip_button = reply_keyboard_creator([[skip_button_text]], one_time_keyboard=True)
            msg = bot.send_message(message.chat.id, about, reply_markup=skip_button)
            bot.register_next_step_handler(msg, askAbout)
        else:
            get_name_message = data.get_bot_messages('get_name', lang=lang)
            msg = bot.send_message(message.chat.id, get_name_message)
            bot.register_next_step_handler(msg, askName)

    def askAbout(message):
        lang = data.get_lang(message.chat.id)
        about = message.text

        if about == data.get_bot_messages('skip_button', lang=lang):
            pass
        elif about:
                data.update_member_info(message.chat.id, about=about)
        else:
            about = data.get_bot_messages('about', lang=lang)
            skip_button_text = data.get_bot_messages('skip_button', lang=lang)
            skip_button = reply_keyboard_creator([[skip_button_text]], one_time_keyboard=True)
            msg = bot.send_message(message.chat.id, about, reply_markup=skip_button)
            bot.register_next_step_handler(msg, askAbout)

        get_photo_video = data.get_bot_messages('get_photo_video', lang=lang)
        msg = bot.send_message(message.chat.id, get_photo_video)
        bot.register_next_step_handler(msg, askAvatar)

    def askAvatar(message):
        lang = data.get_lang(message.chat.id)

        if message.content_type == 'photo':
            file_id = message.json['photo'][0]['file_id']
            data.update_member_info(message.chat.id, avatar=file_id)
            data.update_member_info(message.chat.id, avatar_type='photo')
        elif message.content_type == 'video':
            file_id = message.json['video']['thumb']['file_id']
            data.update_member_info(message.chat.id, avatar=file_id)
            data.update_member_info(message.chat.id, avatar_type='video')
        else:
            get_photo_video = data.get_bot_messages('get_photo_video', lang=lang)
            msg = bot.send_message(message.chat.id, get_photo_video)
            bot.register_next_step_handler(msg, askAvatar)

        m = data.get_bot_messages('your_profile_looks_like', lang=lang)
        bot.send_message(message.chat.id, m)

        info = data.get_member_info(message.chat.id, name=True, age=True, city=True, about=True)
        caption = f"{info['name']}, {info['age']}, {info['city']}\n{info['about']}"

        photo_video_id = data.get_member_info(message.chat.id, avatar=True)['avatar']

        if message.content_type == 'photo':
            bot.send_photo(message.chat.id, photo_video_id, caption=caption)
        elif message.content_type == 'video':
            bot.send_video(message.chat.id, photo_video_id, caption=caption)


        yes_button = data.get_bot_messages('yes_button', lang=lang)
        edit_profile_button = data.get_bot_messages('edit_profile_button', lang=lang)
        buttons = reply_keyboard_creator([[yes_button, edit_profile_button]], one_time_keyboard=True)
        confirm_profile = data.get_bot_messages('confirm_profile', lang=lang)
        msg = bot.send_message(message.chat.id, confirm_profile, reply_markup=buttons)

        bot.register_next_step_handler(msg, askConfirm)

    def askConfirm(message):
        pass


    bot.polling()




if __name__ == "__main__":
    main()
