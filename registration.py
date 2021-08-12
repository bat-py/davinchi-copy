from keyboar_creators import *

# Works if members didn't choose one of the language button
class Registration:
    def __init__(self, bot, data, random_profile_sender):
        self.bot = bot
        self.data = data
        self.random_profile_sender = random_profile_sender

    def askLang(self, message):
        answear = message.text
        chat_id = message.chat.id
        if answear == '🇷🇺 Начать':
            self.data.insert_id_lang(chat_id, 'ru')
            bot_message = self.data.get_bot_messages('age', 'ru')
            msg = self.bot.send_message(message.chat.id, bot_message)
            self.bot.register_next_step_handler(msg, self.askAge)

        elif answear == '🇺🇸 Start':
            self.data.insert_id_lang(chat_id, 'eng')
            bot_message = self.data.get_bot_messages('age', 'eng')
            msg = self.bot.send_message(message.chat.id, bot_message)
            self.bot.register_next_step_handler(msg, self.askAge)

        elif answear == '🇺🇦 Почати':
            self.data.insert_id_lang(chat_id, 'uk')
            bot_message = self.data.get_self.bot_messages('age', 'uk')
            msg = self.bot.send_message(message.chat.id, bot_message)
            self.bot.register_next_step_handler(msg, self.askAge)
        else:
            choose_lang_list = self.data.get_self.bot_messages(message='langs')
            lang_list_for_create_button = [[i[1] for i in choose_lang_list.items()]]
            buttons = reply_keyboard_creator(all_buttons=lang_list_for_create_button, one_time_keyboard=True)
            warning_message = self.data.get_bot_messages(message='warning_choose_lang', lang='eng')
            msg = self.bot.send_message(message.chat.id, warning_message, reply_markup=buttons)
            self.bot.register_next_step_handler(msg, self.askLang)


    # Ask member's age
    def askAge(self, message):
        lang = self.data.get_lang(message.chat.id)
        try:
            age = int(message.text)
            self.data.update_member_info(message.chat.id, age=age)
            ask_gender_message = self.data.get_bot_messages('gender', lang=lang)
            button_man = self.data.get_bot_messages('button_man', lang=lang)
            button_girl = self.data.get_bot_messages('button_girl', lang=lang)
            buttons = reply_keyboard_creator([[button_man, button_girl]], one_time_keyboard=False)
            msg = self.bot.send_message(message.chat.id, ask_gender_message, reply_markup=buttons)
            self.bot.register_next_step_handler(msg, self.askGender)
        except:
            wrong_age = self.data.get_bot_messages('wrong_age', lang)
            msg = self.bot.send_message(message.chat.id, wrong_age)
            self.bot.register_next_step_handler(msg, self.askAge)

    def askGender(self, message):
        lang = self.data.get_lang(message.chat.id)
        gender = message.text

        if gender == self.data.get_bot_messages('button_man', lang=lang):
            self.data.update_member_info(message.chat.id, gender='man')
            ask_interested = self.data.get_bot_messages('interested', lang=lang)

            interested_button_man = self.data.get_bot_messages('interested_button_man', lang=lang)
            interested_button_girl = self.data.get_bot_messages('interested_button_girl', lang=lang)
            interested_button_all = self.data.get_bot_messages('interested_button_all', lang=lang)
            interested_buttons = reply_keyboard_creator([[interested_button_girl, interested_button_man, interested_button_all]], one_time_keyboard=True)
            msg = self.bot.send_message(message.chat.id, ask_interested, reply_markup=interested_buttons)
            self.bot.register_next_step_handler(msg, self.askInterested)
        elif gender == self.data.get_bot_messages('button_girl', lang=lang):
            self.data.update_member_info(message.chat.id, gender='girl')

            ask_interested = self.data.get_bot_messages('interested', lang=lang)
            interested_button_man = self.data.get_bot_messages('interested_button_man', lang=lang)
            interested_button_girl = self.data.get_bot_messages('interested_button_girl', lang=lang)
            interested_button_all = self.data.get_bot_messages('interested_button_all', lang=lang)
            interested_buttons = reply_keyboard_creator([[interested_button_girl, interested_button_man, interested_button_all]], one_time_keyboard=True)
            msg = self.bot.send_message(message.chat.id, ask_interested, reply_markup=interested_buttons)
            self.bot.register_next_step_handler(msg, self.askInterested)
        else:
            wrong_gender = self.data.get_bot_messages('wrong_gender', lang=lang)
            button_man = self.data.get_bot_messages('button_man', lang=lang)
            button_girl = self.data.get_bot_messages('button_girl', lang=lang)
            buttons = reply_keyboard_creator([[button_man, button_girl]], one_time_keyboard=False)

            msg = self.bot.send_message(message.chat.id, wrong_gender, reply_markup=buttons)
            self.bot.register_next_step_handler(msg, self.askGender)

    def askInterested(self, message):
        lang = self.data.get_lang(message.chat.id)
        interested = message.text

        if interested  == self.data.get_bot_messages('interested_button_man', lang=lang):
            self.data.update_member_info(message.chat.id, interested='man')

            which_city = self.data.get_bot_messages(message='which_city', lang=lang)
            msg = self.bot.send_message(message.chat.id, which_city)
            self.bot.register_next_step_handler(msg, self.askCity)

        elif interested == self.data.get_bot_messages('interested_button_girl', lang=lang):
            self.data.update_member_info(message.chat.id, interested='girl')

            which_city = self.data.get_bot_messages(message='which_city', lang=lang)
            msg = self.bot.send_message(message.chat.id, which_city)
            self.bot.register_next_step_handler(msg, self.askCity)

        elif interested == self.data.get_bot_messages('interested_button_all', lang=lang):
            self.data.update_member_info(message.chat.id, interested='all')

            which_city = self.data.get_bot_messages(message='which_city', lang=lang)
            msg = self.bot.send_message(message.chat.id, which_city)
            self.bot.register_next_step_handler(msg, self.askCity)

        else:
            wrong_interested = self.data.get_bot_messages('wrong_interested', lang=lang)
            interested_button_man = self.data.get_bot_messages('interested_button_man', lang=lang)
            interested_button_girl = self.data.get_bot_messages('interested_button_girl', lang=lang)
            interested_button_all = self.data.get_bot_messages('interested_button_all', lang=lang)
            interested_buttons = reply_keyboard_creator([[interested_button_girl, interested_button_man, interested_button_all]], one_time_keyboard=True)
            msg = self.bot.send_message(message.chat.id, wrong_interested, reply_markup=interested_buttons)
            self.bot.register_next_step_handler(msg, self.askInterested)

    def askCity(self, message):
        lang = self.data.get_lang(message.chat.id)
        city = message.text

        if city:
            self.data.update_member_info(message.chat.id, city=city)
            members_name = message.chat.first_name
            name_button = reply_keyboard_creator([[members_name]], one_time_keyboard=True)
            get_name_message = self.data.get_bot_messages('get_name', lang=lang)
            msg = self.bot.send_message(message.chat.id, get_name_message, reply_markup=name_button)
            self.bot.register_next_step_handler(msg, self.askName)
        else:
            which_city = self.data.get_bot_messages(message='which_city', lang=lang)
            msg = self.bot.send_message(message.chat.id, which_city)
            self.bot.register_next_step_handler(msg, self.askCity)

    # Ask member's name and creates button with member's name
    def askName(self, message):
        lang = self.data.get_lang(message.chat.id)
        name = message.text

        if name:
            self.data.update_member_info(message.chat.id, name=name)
            abouts = self.data.get_bot_messages('about', lang=lang)
            skip_button_text = self.data.get_bot_messages('skip_button', lang=lang)
            skip_button = reply_keyboard_creator([[skip_button_text]], one_time_keyboard=True)
            msg = self.bot.send_message(message.chat.id, abouts, reply_markup=skip_button)
            self.bot.register_next_step_handler(msg, self.askAbout)
        else:
            members_name = message.chat.first_name
            name_button = reply_keyboard_creator([[members_name]], one_time_keyboard=True)
            get_name_message = self.data.get_bot_messages('get_name', lang=lang)
            msg = self.bot.send_message(message.chat.id, get_name_message, reply_markup=name_button)
            self.bot.register_next_step_handler(msg, self.askName)

    def askAbout(self, message):
        lang = self.data.get_lang(message.chat.id)

        about = message.text
        if about == self.data.get_bot_messages('skip_button', lang=lang):
            get_photo_video = self.data.get_bot_messages('get_photo_video', lang=lang)
            msg = self.bot.send_message(message.chat.id, get_photo_video)
            self.bot.register_next_step_handler(msg, self.askAvatar)
        elif about:
            self.data.update_member_info(message.chat.id, about=about)

            get_photo_video = self.data.get_bot_messages('get_photo_video', lang=lang)
            msg = self.bot.send_message(message.chat.id, get_photo_video)
            self.bot.register_next_step_handler(msg, self.askAvatar)
        else:
            about = self.data.get_bot_messages('about', lang=lang)
            skip_button_text = self.data.get_bot_messages('skip_button', lang=lang)
            skip_button = reply_keyboard_creator([[skip_button_text]], one_time_keyboard=True)
            msg = self.bot.send_message(message.chat.id, about, reply_markup=skip_button)
            self.bot.register_next_step_handler(msg, self.askAbout)

    def askAvatar(self, message):
        lang = self.data.get_lang(message.chat.id)

        if message.content_type == 'photo':
            file_id = message.json['photo'][0]['file_id']
            self.data.update_member_info(message.chat.id, avatar=file_id)
            self.data.update_member_info(message.chat.id, avatar_type='photo')

            m = self.data.get_bot_messages('profile_looks_like', lang=lang)
            self.bot.send_message(message.chat.id, m)

            info = self.data.get_member_info(message.chat.id, name=True, age=True, city=True, about=True)
            caption = f"{info['name']}, {info['age']}, {info['city']}\n{info['about']}"

            photo_video_id = self.data.get_member_info(message.chat.id, avatar=True)['avatar']
            self.bot.send_photo(message.chat.id, photo_video_id, caption=caption)

            yes_button = self.data.get_bot_messages('yes_button', lang=lang)
            edit_profile_button = self.data.get_bot_messages('edit_profile_button', lang=lang)
            buttons = reply_keyboard_creator([[yes_button, edit_profile_button]], one_time_keyboard=True)
            confirm_profile = self.data.get_bot_messages('confirm_profile', lang=lang)
            msg = self.bot.send_message(message.chat.id, confirm_profile, reply_markup=buttons)
            self.bot.register_next_step_handler(msg, self.askConfirm)

        elif message.content_type == 'video':
            file_id = message.json['video']['thumb']['file_id']
            self.data.update_member_info(message.chat.id, avatar=file_id)
            self.data.update_member_info(message.chat.id, avatar_type='video')

            m = self.data.get_bot_messages('profile_looks_like', lang=lang)
            self.bot.send_message(message.chat.id, m)

            info = self.data.get_member_info(message.chat.id, name=True, age=True, city=True, about=True)
            caption = f"{info['name']}, {info['age']}, {info['city']}\n{info['about']}"

            photo_video_id = self.data.get_member_info(message.chat.id, avatar=True)['avatar']
            self.bot.send_video(message.chat.id, photo_video_id, caption=caption)

            yes_button = self.data.get_bot_messages('yes_button', lang=lang)
            edit_profile_button = self.data.get_bot_messages('edit_profile_button', lang=lang)
            buttons = reply_keyboard_creator([[yes_button, edit_profile_button]], one_time_keyboard=True)
            confirm_profile = self.data.get_bot_messages('confirm_profile', lang=lang)
            msg = self.bot.send_message(message.chat.id, confirm_profile, reply_markup=buttons)
            self.bot.register_next_step_handler(msg, self.askConfirm)

        else:
            get_photo_video = self.data.get_bot_messages('get_photo_video', lang=lang)
            msg = self.bot.send_message(message.chat.id, get_photo_video)
            self.bot.register_next_step_handler(msg, self.askAvatar)

    def askConfirm(self, message):
        lang = self.data.get_lang(message.chat.id)

        if message.text == self.data.get_bot_messages('yes_button', lang=lang):
            self.random_profile_sender(message.chat.id)
        elif message.text == self.data.get_bot_messages('edit_profile_button', lang=lang):
            bot_message = self.data.get_bot_messages('age', lang=lang)
            msg = self.bot.send_message(message.chat.id, bot_message)
            self.bot.register_next_step_handler(msg, self.askAge)
        else:
            wrong_confirm = self.data.get_bot_messages('wrong_confirm', lang=lang)
            yes_button = self.data.get_bot_messages('yes_button', lang=lang)
            edit_profile_button = self.data.get_bot_messages('edit_profile_button', lang=lang)
            buttons = reply_keyboard_creator([[yes_button, edit_profile_button]], one_time_keyboard=True)
            msg = self.bot.send_message(message.chat.id, wrong_confirm, reply_markup=buttons)
            self.bot.register_next_step_handler(msg, self.askConfirm)


