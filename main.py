#import mimetypes
import telebot
from sql import SqlRequests
from keyboar_creators import *
from registration import Registration
from members_settings import *


def main():
    @bot.message_handler(commands=['start'])
    def start_command(message):
        r = Registration(bot, data, random_profile_sender)

        if data.check_member_exist(message.chat.id):
            data.del_member(message.chat.id)

        welcome_message = data.get_bot_messages('after_start_new', 'eng')

        choose_lang_list = data.get_bot_messages(message='langs')
        lang_list_for_create_button = [[i[1] for i in choose_lang_list.items()]]
        buttons = reply_keyboard_creator(all_buttons=lang_list_for_create_button, one_time_keyboard=True)


        msg = bot.send_message(message.chat.id, welcome_message, reply_markup=buttons)
        bot.register_next_step_handler(msg, r.askLang)

    def random_profile_sender(chat_id):
        ''' Возврашает случайную анкету '''

        lang = data.get_lang(chat_id)
        interested = data.get_member_info(chat_id, interested=True)['interested']

        member = data.random_profile_select(chat_id, interested)
        member_profile = f"{member['name']}, {member['age']}, {member['city']}\n{member['about']}"

        like_emoji = data.get_bot_messages('like_emoji', lang=lang)
        send_message_emoji = data.get_bot_messages('send_message_emoji', lang=lang)
        dislike_emoji = data.get_bot_messages('dislike_emoji', lang=lang)
        zzz_emoji = data.get_bot_messages('zzz_emoji', lang=lang)
        main_menu_buttons = [like_emoji, send_message_emoji, dislike_emoji, zzz_emoji]
        four_buttons = reply_keyboard_creator([main_menu_buttons], one_time_keyboard=True)
        
        if member['avatar_type'] == 'photo':
            msg = bot.send_photo(chat_id, member['avatar'], caption=member_profile, reply_markup=four_buttons)
        elif member['avatar_type'] == 'video':
            msg = bot.send_video(chat_id, member['avatar'], caption=member_profile, reply_markup=four_buttons)
        else:
            pass
            # photo or video not found
        bot.register_next_step_handler(msg, press_four_buttons, lang, member, main_menu_buttons)

    def press_four_buttons(message, lang, member, main_menu_buttons):
        ''' Вызывается когда пользователь нажимает на одну из 4 кнопок(like_emoji, send_message_emoji, dislike_emoji, zzz_emoji) главного меню '''

        # Если пользователь нажал на like_emoji, перенаправляет на главное меню обратно
        if message.text == main_menu_buttons[0]:
            count_likes = data.like(member['id'], message.chat.id)
            if count_likes:
                someone_like_you(member, lang)

            random_profile_sender(message.chat.id)


        # Если пользователь нажал на кнопку send_message_emoji, перенаправляет на функцию send_members_message_to_another_member
        elif message.text == main_menu_buttons[1]:
            mesg = data.get_bot_messages('send_message_to_another_member', lang=lang)
            go_back_button_text = data.get_bot_messages('go_back', lang=lang)
            button = reply_keyboard_creator([[go_back_button_text]], one_time_keyboard=True)
            msg = bot.send_message(message.chat.id, mesg, reply_markup=button)
            bot.register_next_step_handler(msg, send_members_message_to_another_member, member, go_back_button_text)

        # Если пользователь нажал на dislike_emoji, перенаправляет на главное меню обратно
        elif message.text == main_menu_buttons[2]:
            data.dislike(member['id'], message.chat.id)
            random_profile_sender(message.chat.id)

        # Если пользователь нажал на zzz_emoji, перенаправляет на функцию ...
        elif message.text == main_menu_buttons[3]:
            zzz_caption = data.get_bot_messages('after_press_zzz_caption', lang=lang)
            bot.send_message(message.chat.id, zzz_caption)

            zzz_body = data.get_bot_messages('after_press_zzz_body', lang=lang)
            buttons = reply_keyboard_creator([['1 🚀', '2', '3', '4']], one_time_keyboard=True)
            msg = bot.send_message(message.chat.id, zzz_body, reply_markup=buttons)
            bot.register_next_step_handler(msg, after_press_1234, lang)

        # Если пользователь отправил какой-то текст или файлы, происходит рекурсия
        else:
            mesg = data.get_bot_messages('wrong_main_menu_button', lang=lang)
            four_buttons = reply_keyboard_creator([main_menu_buttons], one_time_keyboard=False)
            msg = bot.send_message(message.chat.id, mesg, reply_markup=four_buttons)
            bot.register_next_step_handler(msg, press_four_buttons, lang, member, main_menu_buttons)

    def send_members_message_to_another_member(message, member, go_back_button_text):
        ''' Вызывается когда пользователь нажамает на send_message_emoji '''
        if message.content_type == 'text':
            if message.text == go_back_button_text:
                random_profile_sender(message.chat.id)
            else:
                lang = data.get_lang(member['id'])
                random_profile_sender(message.chat.id)
                sender = f'<a href="tg://user?id={message.chat.id}"> {message.chat.first_name} </a>'

                message_from = data.get_bot_messages('message_from', lang=lang)
                mesg = f"{message_from} {sender}:\n{message.text}"
                bot.send_message(member['id'], mesg,parse_mode='html')

        else:
            mesg = data.get_bot_messages('only_message', lang=lang)
            button = reply_keyboard_creator([[go_back_button_text]], one_time_keyboard=True)
            msg = bot.send_message(message.chat.id, mesg, reply_markup=button)
            bot.register_next_step_handler(msg, send_members_message_to_another_member, lang, member, go_back_button_text)

    def after_press_1234(message, lang):
        ''' После нажатия zzz_emoji бот будет ожидать в ответ 4 кнопки (1 🚀, 2, 3, 4)'''
        # 1. Смотреть анкеты.
        if message.text == '1 🚀':
            random_profile_sender(message.chat.id)

        # 2. Моя анкета.
        elif message.text == '2':
            settings = MembersSettings(bot, start_command=start_command, random_profile_sender=random_profile_sender)
            settings.profile_looks_like(message, lang=lang)

        # 3. Я больше не хочу никого искать.
        elif message.text == '3':
            settings = MembersSettings(bot, after_press_1234=after_press_1234)
            settings.turn_off_profile_menu(message, lang=lang)

        # 4. Пригласи друзей - получи больше лайков
        elif message.text == '4':
            go_back= data.get_bot_messages('go_back', lang=lang)
            go_back_button = reply_keyboard_creator([[go_back]], one_time_keyboard=True)

            invite_friends = data.get_bot_messages('invite_friends', lang=lang)
            your_statistic = data.get_bot_messages('your_statistic', lang=lang)
            in_seven_day = data.get_bot_messages('in_seven_day', lang=lang)
            bonus = data.get_bot_messages('bonus', lang=lang)
            your_link = data.get_bot_messages('your_link', lang=lang)

            msg = f"{invite_friends}\n\n{your_statistic}\n{in_seven_day}\n{bonus}\n\n{your_link}"
            bot.send_message(message.chat.id, msg, reply_markup=go_back_button)
            
        else:
            wrong_answear_text = data.get_bot_messages('wrong_answear', lang=lang)
            buttons = reply_keyboard_creator([['1 🚀', '2', '3', '4']], one_time_keyboard=True)
            msg = bot.send_message(message.chat.id, wrong_answear_text, reply_markup=buttons)
            bot.register_next_step_handler(msg, after_press_1234, lang)



    def someone_like_you(member, lang):
        '''
        Отравит сообщения такого типа:

        Ты понравился 1 девушке, показать её?
        1. Показать.
        2. Не хочу больше никого смотреть.
        '''

        list_liked_members = data.likes_count(member['id'])

        if member['gender'] == 'man':
            # Ты понравился
            you_liked_to = data.get_bot_messages('you_man_liked_to', lang=member['lang'])
        else:
            # Ты понравилась
            you_liked_to = data.get_bot_messages('you_girl_liked_to', lang=member['lang'])

        if list_liked_members:
            if int(list_liked_members) == 1:
                if member['gender'] == 'man':
                    # девушке
                    to = data.get_bot_messages('to_one_girl', lang=member['lang'])
                else:
                    # парню
                    to = data.get_bot_messages('to_one_guy', lang=member['lang'])
            else:
                if member['gender'] == 'man':
                    # девушкам
                    to = data.get_bot_messages('to_many_girls', lang=member['lang'])
                else:
                    # парням
                    to = data.get_bot_messages('to_many_guys', lang=member['lang'])

        show_or_no = data.get_bot_messages('show_or_no', lang=member['lang'])
        like_emoji = data.get_bot_messages('like_emoji', lang=member['lang'])
        zzz_emoji = data.get_bot_messages('zzz_emoji', lang=member['lang'])
        show_or_no_buttons = reply_keyboard_creator([[like_emoji, zzz_emoji]], one_time_keyboard=True)
        mesg = f"{you_liked_to} {list_liked_members} {to}\n\n{show_or_no}"

        msg = bot.send_message(member['id'], mesg, reply_markup=show_or_no_buttons)
        bot.register_next_step_handler(msg, after_press_show_yes_or_no, like_emoji, zzz_emoji)


    def after_press_show_yes_or_no(message, like_emoji, zzz_emoji):
        lang = data.get_lang(message.chat.id)

        # Из базы берем ид человека который его лайкнул. Если лайков несолько, тогда берется самый старый
        if message.text == like_emoji:
            show_liked_memeber(message, lang)
        else:
            zzz_caption = data.get_bot_messages('after_press_zzz_caption', lang=lang)
            bot.send_message(message.chat.id, zzz_caption)

            zzz_body = data.get_bot_messages('after_press_zzz_body', lang=lang)
            buttons = reply_keyboard_creator([['1 🚀', '2', '3', '4']], one_time_keyboard=True)
            msg = bot.send_message(message.chat.id, zzz_body, reply_markup=buttons)
            bot.register_next_step_handler(msg, after_press_1234, lang)


    def show_liked_memeber(message, lang):
        first_sender_id = data.first_sender(message.chat.id)
        first_sender = data.get_member_info(first_sender_id, name=True, age=True, city=True, about=True, avatar=True, avatar_type=True)
        first_sender_lang = data.get_lang(first_sender_id)

        like_count = data.likes_count(message.chat.id)

        someone_liked_your_profile_text = data.get_bot_messages('someone_liked_your_profile', lang=lang)

        first_sender_profile = f"{first_sender['name']}, {first_sender['age']}, {first_sender['city']}\n{first_sender['about']}"

        show_or_no = data.get_bot_messages('show_or_no', lang=lang)
        like_emoji = data.get_bot_messages('like_emoji', lang=lang)
        dislike_emoji = data.get_bot_messages('dislike_emoji', lang=lang)
        complaint = data.get_bot_messages('complaint', lang=lang)
        zzz_emoji = data.get_bot_messages('zzz_emoji', lang=lang)
        buttons_texts = [like_emoji, dislike_emoji, complaint, zzz_emoji]
        buttons = reply_keyboard_creator([[like_emoji, dislike_emoji, complaint, zzz_emoji]], one_time_keyboard=True)

        # Покажем анкету человека кто его лайкнул:
        caption = f"{someone_liked_your_profile_text} {like_count})\n\n{first_sender_profile}"
        if first_sender['avatar_type'] == 'photo':
            msg = bot.send_photo(message.chat.id, first_sender['avatar'], caption=caption, reply_markup=buttons)
        else:
            msg = bot.send_video(message.chat.id, first_sender['avatar'], caption=caption, reply_markup=buttons)

        bot.register_next_step_handler(msg, sympathy, lang, first_sender_id, first_sender_lang, first_sender, buttons_texts)


    def sympathy(message, lang, first_sender_id, first_sender_lang, first_sender, buttons_texts):
        if message.text  == buttons_texts[0]:
            complaint_inline_keyboard_text = data.get_bot_messages('complaint_inline_keyboard', lang=lang)
            complaint_inline_button = telebot.types.InlineKeyboardMarkup()
            complaint_inline_button.add(telebot.types.InlineKeyboardButton(text=complaint_inline_keyboard_text, callback_data='complaint'))

            url = f'<a href="tg://user?id={first_sender_id}">{first_sender["name"]}</a>'
            mesg = f"{data.get_bot_messages('responce_to_sympathy', lang=lang)} {url}"
            bot.send_message(message.chat.id, mesg, parse_mode='html')
            random_profile_sender(message.chat.id)



            # Теперь отправим сообщение человеку который первым лайкнул о том что ему лайкнули в ответ и отправим ссылка на аккаунт
            sympathy_text = data.get_bot_messages('sympathy')
            link_to_account_who_answeared_you = f'<a href="tg://user?id={message.chat.id}"> {message.chat.first_name} </a>'
            sympathy = f"{sympathy_text[first_sender_lang]} {link_to_account_who_answeared_you}"
            bot.send_message(first_sender_id, sympathy, parse_mode='html')

            answeared_member = data.get_member_info(message.chat.id, name=True, age=True, city=True, about=True,
                                                avatar=True, avatar_type=True)

            caption = f"{answeared_member['name']}, {answeared_member['age']}, {answeared_member['city']}\n{answeared_member['about']}"
            if answeared_member['avatar_type'] == 'photo':
                bot.send_photo(first_sender_id, answeared_member['avatar'], caption=caption, reply_markup=complaint_inline_button)
            else:
                bot.send_video(first_sender_id, answeared_member['avatar'], caption=caption, reply_markup=complaint_inline_button)

            zzz_body = data.get_bot_messages('after_press_zzz_body', lang=first_sender_lang)
            buttons = reply_keyboard_creator([['1 🚀', '2', '3', '4']], one_time_keyboard=True)
            msg = bot.send_message(first_sender_id, zzz_body, reply_markup=buttons)
            bot.register_next_step_handler(msg, after_press_1234, first_sender_lang)


    @bot.message_handler(content_types=['text'])
    def text_message_handler(message):
        ''' Функция понадобиться чтобы пользователь мог вернуться на главный экран(или на раеистрацию) если бот перезагрузиться '''

        if data.check_exist_id_name_city_avatar(message.chat.id):
            random_profile_sender(message.chat.id)
        else:
            r = Registration(bot, data, random_profile_sender)

            welcome_message = data.get_bot_messages('after_start_new', 'eng')

            choose_lang_list = data.get_bot_messages(message='langs')
            lang_list_for_create_button = [[i[1] for i in choose_lang_list.items()]]
            buttons = reply_keyboard_creator(all_buttons=lang_list_for_create_button, one_time_keyboard=True)

            msg = bot.send_message(message.chat.id, welcome_message, reply_markup=buttons)
            bot.register_next_step_handler(msg, r.askLang)



if __name__ == "__main__":
    bot = telebot.TeleBot('1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ')
    data = SqlRequests()
    main()
    bot.polling()
