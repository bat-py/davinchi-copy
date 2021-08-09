from keyboar_creators import *
from sql import *
class MembersSettings:
    def __init__(self, bot, start_command=None, random_profile_sender=None, after_press_1234=None):
        self.start_command = start_command
        self.bot = bot
        self.data = SqlRequests()
        self.start_command = start_command
        self.random_profile_sender = random_profile_sender
        self.after_press_1234 = after_press_1234

    def profile_looks_like(self, message, lang):
        ''' Создает главное меню настроек. Показывает анкету с 5 кнопками и функция member_settings ждет ответ (1 или 2 ... или 5  '''
        buttons = ['1', '2', '3', '4', '5 🚀']
        profile_looks_like = self.data.get_bot_messages('profile_looks_like', lang=lang)
        self.bot.send_message(message.chat.id, profile_looks_like)

        member = self.data.get_member_info(message.chat.id, name=True, age=True, city=True, avatar=True,
                                      avatar_type=True, about=True)
        member_profile = f"{member['name']}, {member['age']}, {member['city']}\n{member['about']}"
        if member['avatar_type'] == 'photo':
            self.bot.send_photo(message.chat.id, member['avatar'], caption=member_profile)
        elif member['avatar_type'] == 'video':
            self.bot.send_video(message.chat.id, member['avatar'], caption=member_profile)

        mesg = self.data.get_bot_messages('profile_settings', lang=lang)

        buttons = reply_keyboard_creator([buttons], one_time_keyboard=True)
        msg = self.bot.send_message(message.chat.id, mesg, reply_markup=buttons)
        self.bot.register_next_step_handler(msg, self.member_settings, message, buttons, lang)

    def member_settings(self, message, buttons, lang):
        go_back_text = self.data.get_bot_messages('go_back', lang=lang)
        go_back_button = reply_keyboard_creator([[go_back_text]], one_time_keyboard=True)

        # 1. Заполнить анкету заново.
        if message.text == buttons[0]:
            self.start_command(message)

        # 2.Изменить фото / видео.
        elif message.text == buttons[1]:
            get_photo_video_text = self.data.get_bot_messages('get_photo_video', lang=lang)
            msg = self.bot.send_message(message.chat.id, get_photo_video_text, reply_markup=go_back_button)
            self.bot.register_next_step_handler(msg, self.update_avatar, go_back_text, lang)

        # 3. Изменить текст анкеты.
        elif message.text == buttons[2]:
            about_text = self.data.get_bot_messages('about', lang=lang)
            msg = self.bot.send_message(message.chat.id, about_text, reply_markup=go_back_button)
            self.bot.register_next_step_handler(msg, self.update_about, go_back_text, lang)

        # 4. Привязка Instagram.
        elif message.text == buttons[3]:
            send_me_instagram_profile_text = self.data.get_bot_messages('send_me_instagram_profile', lang=lang)
            msg = self.bot.send_message(message.chat.id, send_me_instagram_profile_text, reply_markup=go_back_button)
            self.bot.register_next_step_handler(msg, self.update_instagram, go_back_text, lang)

        # 5. Смотреть анкеты.
        elif message.text == buttons[4]:
            self.random_profile_sender(message.chat.id)

        else:
            self.profile_looks_like(message, lang=lang)

    def update_avatar(self, message, go_back_text, lang):
        ''' Эту функцию запускает member_settings. Срабатывает после нажатия кнопки "2.Изменить фото / видео." '''
        if message.text == go_back_text:
            self.profile_looks_like(message, lang=lang)

        elif message.content_type == 'photo':
            saved = self.data.get_bot_messages('saved', lang=lang)

            file_id = message.json['photo'][0]['file_id']
            self.data.update_member_info(message.chat.id, avatar=file_id)
            self.data.update_member_info(message.chat.id, avatar_type='photo')

            self.bot.send_message(message.chat.id, saved)
            self.profile_looks_like(message, lang=lang)

        elif message.content_type == 'video':
            saved = self.data.get_bot_messages('saved', lang=lang)

            file_id = message.json['video']['thumb']['file_id']
            self.data.update_member_info(message.chat.id, avatar=file_id)
            self.data.update_member_info(message.chat.id, avatar_type='video')

            self.bot.send_message(message.chat.id, saved)
            self.profile_looks_like(message, lang=lang)
        else:
            get_photo_video = self.data.get_bot_messages('get_photo_video', lang=lang)
            go_back_button = reply_keyboard_creator([[go_back_text]], one_time_keyboard=True)
            msg = self.bot.send_message(message.chat.id, get_photo_video, reply_markup=go_back_button)
            self.bot.register_next_step_handler(msg, self.update_avatar, go_back_text, lang)

    def update_about(self, message, go_back_text, lang):
        '''  Эту функцию запускает member_settings. Срабатывает после нажатия кнопки "3. Изменить текст анкеты." '''

        if message.text == go_back_text:
            self.profile_looks_like(message, lang=lang)

        elif message.text:
            saved = self.data.get_bot_messages('saved', lang=lang)
            self.data.update_member_info(message.chat.id, about=message.text)

            self.bot.send_message(message.chat.id, saved)
            self.profile_looks_like(message, lang=lang)

        else:
            about = self.data.get_bot_messages('about', lang=lang)
            go_back_button = reply_keyboard_creator([[go_back_text]], one_time_keyboard=True)
            msg = self.bot.send_message(message.chat.id, about, reply_markup=go_back_button)
            self.bot.register_next_step_handler(msg, self.update_about, go_back_text, lang)

    def update_instagram(self, message, go_back_text, lang):
        '''  Эту функцию запускает member_settings. Срабатывает после нажатия на кнопку 4. Привязка Instagram. '''
        if message.text == go_back_text:
            self.profile_looks_like(message, lang=lang)
        elif message.text:
            saved = self.data.get_bot_messages('saved', lang=lang)
            self.data.update_member_info(message.chat.id, instagram=message.text)

            self.bot.send_message(message.chat.id, saved)
            self.profile_looks_like(message, lang=lang)
        else:
            go_back_button = reply_keyboard_creator([[go_back_text]], one_time_keyboard=True)
            send_me_instagram_profile_text = self.data.get_bot_messages('send_me_instagram_profile', lang=lang)
            msg = self.bot.send_message(message.chat.id, send_me_instagram_profile_text, reply_markup=go_back_button)
            self.bot.register_next_step_handler(msg, self.update_instagram, go_back_text, lang)



    def turn_off_profile_menu(self, message, lang):
        turn_off_profile_confirm_text = self.data.get_bot_messages('turn_off_profile_confirm', lang=lang)
        buttons_1_2 = reply_keyboard_creator([['1', '2']], one_time_keyboard=True)

        msg = self.bot.send_message(message.chat.id, turn_off_profile_confirm_text, reply_markup=buttons_1_2)
        self.bot.register_next_step_handler(msg, self.turn_off_profile_answear, lang)

    def turn_off_profile_answear(self, message, lang):
        if message.text == '1':
            self.data.del_member(message.chat.id)

            your_profile_deleted_text = self.data.get_bot_messages('your_profile_deleted', lang=lang)
            start_button = reply_keyboard_creator([['/start']], one_time_keyboard=False)
            self.bot.send_message(message.chat.id, your_profile_deleted_text, reply_markup=start_button)

        elif message.text == '2':
            zzz_caption = self.data.get_bot_messages('after_press_zzz_caption', lang=lang)
            self.bot.send_message(message.chat.id, zzz_caption)

            zzz_body = self.data.get_bot_messages('after_press_zzz_body', lang=lang)
            buttons = reply_keyboard_creator([['1 🚀', '2', '3', '4']], one_time_keyboard=True)
            msg = self.bot.send_message(message.chat.id, zzz_body, reply_markup=buttons)
            self.bot.register_next_step_handler(msg, self.after_press_1234, lang)
        else:
            self.turn_off_profile_menu(message, lang=lang)


