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
            cursorclass=DictCursor
            )
            
        self.cur = self.con.cursor()

    def insert_id_lang(self, id, lang):
        self.cur.execute("INSERT INTO members(id, lang) VALUES (%s, %s)", (id, lang))
        self.con.commit()

# Insert or Update members info
    def update_member_info(self, id, name=None, age=None, gender=None, interested=None, city=None, about=None, avatar=None, avatar_type=None):
        if name:
            self.cur.execute("UPDATE members SET name = %s WHERE id = %s", (name, id))
            self.con.commit()

        if age:
            self.cur.execute("UPDATE members SET age = %s WHERE id = %s", (age, id))
            self.con.commit()

        if gender:
            self.cur.execute("UPDATE members SET gender = %s WHERE id = %s", (gender, id))
            self.con.commit()

        if interested:
            self.cur.execute("UPDATE members SET interesting = %s WHERE id = %s", (interested, id))
            self.con.commit()

        if city:
            self.cur.execute("UPDATE members SET city = %s WHERE id = %s", (city, id))
            self.con.commit()

        if about:
            self.cur.execute("UPDATE members SET about = %s WHERE id = %s", (about, id))
            self.con.commit()

        if avatar:
            self.cur.execute("UPDATE members SET avatar = %s WHERE id = %s", (avatar, id))
            self.con.commit()

        if avatar_type:
            self.cur.execute("UPDATE members SET avatar_type = %s WHERE id = %s", (avatar_type, id))
            self.con.commit()

    def del_member(self, id):
        self.cur.execute("DELETE FROM members WHERE id LIKE %s", (id, ))
        self.con.commit()

    def get_member_info(self, id, name=None, age=None, gender=None, interested=None, city=None, about=None, avatar=None, avatar_type=None):
        info = {}
        if name:
            self.cur.execute("SELECT name FROM members WHERE id = %s", (id, ))
            info['name'] = self.cur.fetchone()['name']
        if age:
            self.cur.execute("SELECT age FROM members WHERE id = %s", (id, ))
            info['age'] = self.cur.fetchone()['age']
        if gender:
            self.cur.execute("SELECT gender FROM members WHERE id = %s", (id,))
            info['gender'] = self.cur.fetchone()['gender']
        if interested:
            self.cur.execute("SELECT interesting FROM members WHERE id = %s", (id,))
            info['interested'] = self.cur.fetchone()['interested']
        if city:
            self.cur.execute("SELECT city FROM members WHERE id = %s", (id,))
            info['city'] = self.cur.fetchone()['city']
        if about:
            self.cur.execute("SELECT about FROM members WHERE id = %s", (id,))
            info['about'] = self.cur.fetchone()['about']
        if avatar:
            self.cur.execute("SELECT avatar FROM members WHERE id = %s", (id,))
            info['avatar'] = self.cur.fetchone()['avatar']
        if avatar:
            self.cur.execute("SELECT avatar FROM members WHERE id = %s", (id,))
            info['avatar'] = self.cur.fetchone()['avatar']
        if avatar_type:
            self.cur.execute("SELECT avatar_type FROM members WHERE id = %s", (id,))
            info['avatar_type'] = self.cur.fetchone()['avatar_type']
        return info

# Returns True if in table members exists id
    def check_member_exist (self, id):
        self.cur.execute("SELECT id FROM members WHERE id=%s", (id, ))
        if self.cur.fetchone():
            return True
        else:
            return False

# Retuns lang (ru, eng, uk)
    def get_lang(self, id):
        self.cur.execute("SELECT lang FROM members WHERE id = %s", (id, ))
        return self.cur.fetchone()['lang']

# Gets all bot's messages in three language
    def get_bot_messages(self, message, lang=None):
        self.cur.execute("SELECT ru, eng, uk FROM bot_messages WHERE message = %s", (message,))
        if lang:
            return self.cur.fetchone()[lang]
        else:
            return self.cur.fetchone()



