#import mimetypes
import telebot
from sql import SqlRequests
from keyboar_creators import *
from registration import Registration

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
        else:
            msg = bot.send_video(chat_id, member['avatar'], caption=member_profile, reply_markup=four_buttons)

        bot.register_next_step_handler(msg, press_four_buttons, lang, member, main_menu_buttons)

    def press_four_buttons(message, lang, member, main_menu_buttons):
        ''' Вызывается когда пользователь нажимает на одну из 4 кнопок(like_emoji, send_message_emoji, dislike_emoji, zzz_emoji) главного меню '''

        # Если пользователь нажал на like_emoji, перенаправляет на главное меню обратно
        if message.text == main_menu_buttons[0]:
            data.plus_like(member['id'])
            random_profile_sender(message.chat.id)
        # Если пользователь нажал на кнопку send_message_emoji, перенаправляет на функцию send_members_message_to_another_member
        elif message.text == main_menu_buttons[1]:
            mesg = data.get_bot_messages('send_message_to_another_member', lang=lang)
            go_back_button_text = data.get_bot_messages('go_back', lang=lang)
            button = reply_keyboard_creator([[go_back_button_text]], one_time_keyboard=True)
            msg = bot.send_message(message.chat.id, mesg, reply_markup=button)
            bot.register_next_step_handler(msg, send_members_message_to_another_member, lang, member, go_back_button_text)
        # Если пользователь нажал на dislike_emoji, перенаправляет на главное меню обратно
        elif message.text == main_menu_buttons[2]:
            data.plus_dislike(member['id'])
            random_profile_sender(message.chat.id)

        # Если пользователь нажал на zzz_emoji, перенаправляет на функцию ...
        elif message.text == main_menu_buttons[3]:
            pass

        # Если пользователь отправил какой-то текст или файлы, происходит рекурсия
        else:
            mesg = data.get_bot_messages('wrong_main_menu_button', lang=lang)
            four_buttons = reply_keyboard_creator([main_menu_buttons], one_time_keyboard=False)
            msg = bot.send_message(message.chat.id, mesg, reply_markup=four_buttons)
            bot.register_next_step_handler(msg, press_four_buttons, lang, member, main_menu_buttons)


    def send_members_message_to_another_member(message, lang, member, go_back_button_text):
        ''' Вызывается когда пользователь нажамает на send_message_emoji '''
        if message.content_type == 'text':
            if message.text == go_back_button_text:
                random_profile_sender(message.chat.id)
            else:
                random_profile_sender(message.chat.id)

                message_from = data.get_bot_messages('message_from', lang=lang)
                sender_name = data.get_member_info(message.chat.id, name=True)['name']
                mesg = f"{message_from} {sender_name}:\n{message.text}"
                bot.send_message(member['id'], mesg)

        else:
            mesg = data.get_bot_messages('only_message', lang=lang)
            button = reply_keyboard_creator([[go_back_button_text]], one_time_keyboard=True)
            msg = bot.send_message(message.chat.id, mesg, reply_markup=button)
            bot.register_next_step_handler(msg, send_members_message_to_another_member, lang, member, go_back_button_text)



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
