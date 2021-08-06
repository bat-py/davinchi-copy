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
#            cursorclass=DictCursor
            )
            
        self.cur = self.con.cursor()


    def insert_id_lang(self, id, lang):
        self.cur.execute("INSERT INTO members(id, lang) VALUES (%s, %s)", (id, lang))
        self.con.commit()

    def update_members(self, id, lang=None, name=None, age=None, gender=None, interesting=None, city=None, about=None, avatar=None):
        if lang:
            self.cur.execute("UPDATE members SET lang=%s WHERE id = %s", (lang, id))
            self.con.commit()
        if name:
            self.cur.execute("UPDATE members SET name=%s WHERE id = %s", (name, id))
            self.con.commit()
        if age:
            self.cur.execute("UPDATE members SET age=%s WHERE id = %s", (age, id))
            self.con.commit()
        if gender:
            self.cur.execute("UPDATE members SET gender=%s WHERE id = %s", (gender, id))
            self.con.commit()
        if interesting:
            self.cur.execute("UPDATE members SET interesting=%s WHERE id = %s", (interesting, id))
            self.con.commit()
        if city:
            self.cur.execute("UPDATE members SET city=%s WHERE id = %s", (city, id))
            self.con.commit()
        if about:
            self.cur.execute("UPDATE members SET about=%s WHERE id = %s", (about, id))
            self.con.commit()
        if avatar:
            self.cur.execute("UPDATE members SET =%s WHERE id = %s", (avatar, id))
            self.con.commit()


