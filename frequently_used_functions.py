from keyboar_creators import reply_keyboard_creator

class ImportantFunctions:
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data


    def profile_looks_like(self, message, random_profile_sender, lang):
        profile_looks_like = self.data.get_bot_messages('profile_looks_like', lang=lang)
        self.bot.send_message(message.chat.id, profile_looks_like)

        member = self.data.get_member_info(message.chat.id, name=True, age=True, city=True, avatar=True, avatar_type=True, about=True)
        member_profile = f"{member['name']}, {member['age']}, {member['city']}\n{member['about']}"
        if member['avatar_type'] == 'photo':
            self.bot.send_photo(message.chat.id, member['avatar'], caption=member_profile)
        elif member['avatar_type'] == 'video':
            self.bot.send_video(message.chat.id, member['avatar'], caption=member_profile)

        mesg = self.data.get_bot_messages('profile_settings', lang=lang)
