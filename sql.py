import pymysql
from pymysql.cursors import DictCursor 
import random

def create_connection():
    connection = pymysql.connect(
        host='84.252.74.115',
        user='crow',
        password='crow999',
        db='telegrambot',
        charset='utf8mb4',
        cursorclass=DictCursor
    )
    return connection

class SqlRequests:
    def insert_id_lang(self, id, lang):
        connection = create_connection()
        cur = connection.cursor()

        cur.execute("INSERT INTO members(id, lang) VALUES (%s, %s)", (id, lang))
        connection.commit()
        connection.close()

    def update_member_info(self, id, lang=None, name=None, age=None, gender=None, interested=None, city=None, about=None, avatar=None, avatar_type=None):
        ''' Insert or Update members info '''
        connection = create_connection()
        cur = connection.cursor()

        if lang:
            cur.execute("UPDATE members SET lang = %s WHERE id = %s", (lang, id))
            connection.commit()

        if name:
            cur.execute("UPDATE members SET name = %s WHERE id = %s", (name, id))
            connection.commit()

        if age:
            cur.execute("UPDATE members SET age = %s WHERE id = %s", (age, id))
            connection.commit()

        if gender:
            cur.execute("UPDATE members SET gender = %s WHERE id = %s", (gender, id))
            connection.commit()

        if interested:
            cur.execute("UPDATE members SET interested = %s WHERE id = %s", (interested, id))
            connection.commit()

        if city:
            cur.execute("UPDATE members SET city = %s WHERE id = %s", (city, id))
            connection.commit()

        if about:
            cur.execute("UPDATE members SET about = %s WHERE id = %s", (about, id))
            connection.commit()

        if avatar:
            cur.execute("UPDATE members SET avatar = %s WHERE id = %s", (avatar, id))
            connection.commit()

        if avatar_type:
            cur.execute("UPDATE members SET avatar_type = %s WHERE id = %s", (avatar_type, id))
            connection.commit()
        connection.close()

    def del_member(self, id):
        connection = create_connection()
        cur = connection.cursor()

        cur.execute("DELETE FROM members WHERE id LIKE %s", (id, ))
        connection.commit()
        connection.close()

    def get_member_info(self, id, name=None, age=None, gender=None, interested=None, city=None, about=None, avatar=None, avatar_type=None, likes=None, dislikes=None):
        ''' Returns dict data '''
        connection = create_connection()
        cur = connection.cursor()

        info = {}
        if name:
            cur.execute("SELECT name FROM members WHERE id = %s", (id, ))
            info['name'] = cur.fetchone()['name']
        if age:
            cur.execute("SELECT age FROM members WHERE id = %s", (id, ))
            info['age'] = cur.fetchone()['age']
        if gender:
            cur.execute("SELECT gender FROM members WHERE id = %s", (id,))
            info['gender'] = cur.fetchone()['gender']
        if interested:
            cur.execute("SELECT interested FROM members WHERE id = %s", (id,))
            info['interested'] = cur.fetchone()['interested']
        if city:
            cur.execute("SELECT city FROM members WHERE id = %s", (id,))
            info['city'] = cur.fetchone()['city']
        if about:
            cur.execute("SELECT about FROM members WHERE id = %s", (id,))
            info['about'] = cur.fetchone()['about']
        if avatar:
            cur.execute("SELECT avatar FROM members WHERE id = %s", (id,))
            info['avatar'] = cur.fetchone()['avatar']
        if avatar_type:
            cur.execute("SELECT avatar_type FROM members WHERE id = %s", (id,))
            info['avatar_type'] = cur.fetchone()['avatar_type']
        if likes:
            cur.execute("SELECT likes FROM members WHERE id = %s", (id, ))
            info['likes'] = cur.fetchone()['likes']
        if dislikes:
            cur.execute("SELECT dislikes FROM members WHERE id = %s", (id,))
            info['dislikes'] = cur.fetchone()['dislikes']

        connection.close()
        return info

    def check_member_exist (self, id):
        ''' Returns True if in table members exists id '''
        connection = create_connection()
        cur = connection.cursor()

        cur.execute("SELECT id FROM members WHERE id=%s", (id, ))
        if cur.fetchone():
            connection.close()
            return True
        else:
            connection.close()
            return False

    def get_lang(self, id):
        ''' Retuns lang (ru, eng, uk) '''
        connection = create_connection()
        cur = connection.cursor()

        cur.execute("SELECT lang FROM members WHERE id = %s", (id, ))
        responce = cur.fetchone()['lang']
        connection.close()
        return responce

    def get_bot_messages(self, message, lang=None):
        ''' Gets all bot's messages in three language or in one language if lang if not None'''
        connection = create_connection()
        cur = connection.cursor()

        cur.execute("SELECT ru, eng, uk FROM bot_messages WHERE message = %s", (message,))
        responce = cur.fetchone()
        connection.close()

        if lang:
            return responce[lang]
        else:
            return responce

    def random_profile_select(self, chat_id, interested, city=None):
        connection = create_connection()
        cur = connection.cursor()
        while True:
            #self.cur.execute("SELECT * FROM members WHERE interested = %s", (interested, ))
            #profile_list = self.cur.fetchall()
            #if not profile_list:
            cur.execute("SELECT * FROM members")
            profile_list = cur.fetchall()
            connection.close()
            member = random.choice(profile_list)
            if member['avatar'] and member['age'] and member['name'] and member['city'] and member['id'] != chat_id:
                return member

    def plus_like(self, id):
        connection = create_connection()
        cur = connection.cursor()
        cur.execute("UPDATE members SET likes = likes+1 WHERE id = %s", (id, ))
        connection.commit()
        connection.close()

    def plus_dislike(self, id):
        connection = create_connection()
        cur = connection.cursor()
        cur.execute("UPDATE members SET dislikes = dislikes+1 WHERE id = %s", (id, ))
        connection.commit()
        connection.close()

    def check_exist_id_name_city_avatar(self, id):
        ''' Returns True if member's avatar, age, name, city are exist '''
        connection = create_connection()
        cur = connection.cursor()
        while True:
            cur.execute("SELECT * FROM members WHERE id = %s", (id,))
            member = cur.fetchone()
            connection.close()
            if member:
                if member['avatar'] and member['age'] and member['name'] and member['city']:
                    return True
                else:
                    return False
            else:
                return False


