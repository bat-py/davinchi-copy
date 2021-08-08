import telebot

#Reply_Keyboard_Creator
def reply_keyboard_creator(all_buttons, one_time_keyboard):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time_keyboard)
    for one_row in all_buttons:
        row_bottons = []
        for button in one_row:
                row_bottons.append(button)
        keyboard.row(*row_bottons)

    return keyboard