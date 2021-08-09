import pymysql
from pymysql.cursors import DictCursor


class SqlRequests:
    def __init__(self):
        self.con = pymysql.connect(
            host='84.252.74.115',
            user='crow',
            password='crow999',
            db='telegrambot',
            charset='utf8mb4',
            cursorclass=DictCursor,
        )

        self.cur = self.con.cursor()

    def a(self):
        as2 = ("after_start_exist", "Мы тебя помним! Хочешь снова пообщаться с кем-то новым?",
               "We remember you! Do you want to talk to someone new again",
               "Ми тебе пам\'ятаємо! Хочеш знову поспілкуватися з кимось новим")

        as3 = ("langs",  '🇷🇺 Начать', '🇺🇸 Start', '🇺🇦 Почати')

        as4 = ("age", 'Сколько тебе лет?', 'How old are you?', "Скільки тобі років?")

        as5 = ('gender', 'Теперь определимся с полом', "Now let's decide on the gender", "Тепер визначимося з підлогою")

        as6 = ('interested', "Кто тебе интересен?", "Who are you interested in?", "Хто тобі цікавий?")

        as7 = ("button_man", "Я парень", "I'm a guy", "Я хлопець")

        as8 = ("button_girl", "Я девушка", "I'm a girl", "Я дівчина")

        #as9 = ("", "", "", "")
        as9 = ("interested_button_girl", "Девушки", "Girls", "Дівчата")
        as10 = ("interested_button_man", "Парни" , "Boys", "Хлопець")
        as100 = ("interested_button_all", "Все равно", "Anyway", "Все одно")
        as11 = ("which_city", "Из какого ты города?", "What city are you from?", "З якого ти міста?")
        as12 = ("get_name", "Как мне тебя называть?", "What should I call you?", "Як мені тебе називати?")
        as13 = ("about",
                 "Расскажи о себе и кого хочешь найти, чем предлагаешь заняться. Это поможет лучше подобрать тебе компанию.",
                 "Tell us about yourself and who you want to find, what you offer to do. This will help you find a better company for you.",
                 "Розкажи про себе і кого хочеш знайти, чим пропонуєш зайнятися. Це допоможе краще підібрати тобі компанію."
                 )
        as14 = ("skip_button", "Пропустить", "Skip", "Пропустивши")
        as15 = ("get_photo_video",
                "Теперь пришли фото или запиши видео 👍 (до 15 сек), его будут видеть другие пользователи",
                "Now send a photo or record a video 👍 (up to 15 seconds), it will be seen by other users",
                "Тепер прийшли фото або запиши відео 👍 (до 15 сек), його будуть бачити інші користувачі")
        as16 =  ("profile_looks_like", "Так выглядит твоя анкета:", "This is what your profile looks like:", "Так виглядає твоя анкета:")
        as17 = ("accept", "Все верно?", "Is that right?", "Все вірно?")
        as18 = ("yes_button", "Да", "Yes", "Да")
        as19 = ("edit_profile_button", "Изменить анкету", "Edit the questionnaire", "Змінити анкету")
        as19 = ("wrong_age", "Укажи правильный возраст, только цифры", "Specify the correct age, only numbers", "Вкажи правильний вік, тільки цифри")

        as20 = ("man", "Парень", "Guy" , "Хлопець")
        as21 = ("girl", "Девушка","Girl", "Дівчина" )
        as22 = ("wrong_gender", "Нет такого варианта ответа", "There is no such answer option", "Немає такого варіанту відповіді")
        as23 = ("wrong_interested", "Нет такого варианта ответа", "There is no such answer option", "Немає такого варіанту відповіді")
        as233 = ("wrong_confirm", "Нет такого варианта ответа", "There is no such answer option", "Немає такого варіанту відповіді")
        #as24 = ("your_profile_looks_like", "Так выглядит твоя анкета:", "This is what your profile looks like:", "Так виглядає твоя анкета:")
        as244 = ("confirm_profile", "Все верно?", "Is that right?", "Все вірно?")

        as25 = ("send_message_to_another_member",'Напиши сообщение для этого пользователя', "Write a message for this user", 'Напиши повідомлення для цього користувача')
        as26 = ('warning_short_message', 'Придумай что-то поинтереснее, таким сообщением никого не удивишь 😉',
                'Come up with something more interesting, this message will not surprise anyone 😉',
                'Придумай щось цікавіше, таким повідомленням нікого не здивуєш 😉')

        as27 = ("like_emoji", "❤️", "❤️", "❤️")
        as28 = ("send_message_emoji", "💌", "💌", "💌" )
        as29 = ("dislike_emoji", "👎", '👎', '👎')
        as30 = ("zzz_emoji", '💤', '💤', '💤')

        as31 = ("go_back", "Вернуться назад", "Go back", "Повернутися назад")
        as32 = ("only_message", "Можно отправить только сообщение", "You can only send a message", "Можна надіслати лише повідомлення")

        as55 = ('message_from', 'Сообщение от', 'Message from', 'Повідомлення від')

        as56 = ("wrong_main_menu_button", "Нет такого варианта ответа", "There is no such answer option", "Немає такого варіанту відповіді")
        as57 = ("after_press_zzz_caption", "Подождем пока кто-то увидит твою анкету", "Let's wait until someone sees your profile", "Почекаємо поки хтось побачить твою анкету")

        as58 = ("after_press_zzz_body", "1. Смотреть анкеты.\n2. Моя анкета.\n3. Я больше не хочу никого искать.\n***\n4. Пригласи друзей - получи больше лайков 😎",
                "1. View the questionnaires.\n2. My profile.\n3. I don't want to look for anyone else.\n***\n4. Invite your friends - get more likes 😎",
                "1. Дивитися анкети.\n2. Моя анкета.\n3. Я більше не хочу нікого Шукати.\n***\n4. Запроси друзів-Отримай більше лайків 😎"
                )

        as59 = ('profile_looks_like', 'Так выглядит твоя анкета:', 'Your profile looks like:', 'Так виглядає твоя анкета:')

        as60 = ('profile_settings',
                '1. Заполнить анкету заново.\n2. Изменить фото/видео.\n3. Изменить текст анкеты.\n4. Привязка Instagram.\n5. Смотреть анкеты.',
                '1. Fill out the questionnaire again.\n2. Change the photo/video.\n3. Change the text of the questionnaire.\n4.Snap Instagram.\n5. View the questionnaires.',
                "1. Заповнити анкету заново.\n2. Змінити фото / відео.\n3. Змінити текст анкети.\n4. Прив'язка Instagram.\n5. Дивитися анкети.")

        as61 = ('edit_avatar_button', )

        self.cur.execute("INSERT INTO bot_messages VALUES (%s, %s, %s, %s);", as58)
        self.con.commit()

    def b(self):
        self.cur.execute("SELECT ru FROM bot_messages WHERE message = %s", ("message_from", ))
        a = self.cur.fetchone()
        print(a)
s = SqlRequests()
s.a()

