from keyboar_creators import *

class MembersSettings:
    def __init__(self, start_command, bot, data):
        self.start_command = start_command
        self.bot = bot
        self.data = data

    def member_settings(self, message, lang):
        buttons = ['1', '2', '3', '4', '5 🚀']

        # 1. Заполнить анкету заново.
        if message.text == buttons[0]:
            self.start_command(message)

        # 2.Изменить фото / видео.
        elif message.text == buttons[1]:
            get_photo_video = self.data.get_bot_messages('get_photo_video', lang=lang)
            msg = self.bot.send_message(message.chat.id, get_photo_video)
            self.bot.register_next_step_handler(msg, self.update_avatar, lang)

        # 3. Изменить текст анкеты.
        elif message.text == buttons[2]:
            pass

        # 4. Привязка Instagram.
        elif message.text == buttons[3]:
            pass

        # 5. Смотреть анкеты.
        elif message.text == buttons[4]:
            pass

        else:
            #warning

    def update_avatar(self, message, lang):
        if message.content_type == 'photo':
            file_id = message.json['photo'][0]['file_id']
            self.data.update_member_info(message.chat.id, avatar=file_id)
            self.data.update_member_info(message.chat.id, avatar_type='photo')

            saved_message =

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
            #elf.bot.register_next_step_handler(msg, self.askConfirm)

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
