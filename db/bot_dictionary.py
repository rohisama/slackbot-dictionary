import sqlite3
import json

class BotDictionary:
 
    def __init__(self, path='db/bot_dictionary.sqlite'):
        # データベースファイルのパス
        self.dbpath = path
        # データベース接続とカーソル生成
        self.connection = sqlite3.connect(self.dbpath)
        # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
        # connection.isolation_level = None
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def _create_tables(self):
        try:
            # CREATE
            self.cursor.execute(
                '''CREATE TABLE IF NOT EXISTS bot_dictionary (
                    word TEXT PRIMARY KEY,
                    description TEXT)''')
    
        except sqlite3.Error as e:
            print('sqlite3.Error occurred:', e.args[0])

    def insert_word(self, word, desc):
        self._create_tables()
        sql = f"INSERT OR REPLACE INTO bot_dictionary VALUES (\'{word}\', \'{desc}\')"
        print(sql)
        try:
            self.cursor.execute(sql)
            return "登録できたよ"
        except sqlite3.Error as e:
            print(f"insert error {word}\n {e}")
            return "登録できなかったよ"

    def get_word(self, word):
        sql = f"SELECT description FROM bot_dictionary WHERE word=\'{word}\'"
        print(sql)
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            if data is None:
                return "登録されていません！"
            else:
                return data['description']

        except sqlite3.Error as e:
            print(e)

    def get_list(self):
        sql = "SELECT word from bot_dictionary"
        print(sql)
        try:
            self.cursor.execute(sql)
            words = self.cursor.fetchall()
            if words is None:
                return "登録されていません！"
            else:
                res = "これだけ登録されているよ！\n"
                for word in words:
                    res += f"{word['word']}, "
                return res
        except sqlite3.Error as e:
            print(e)
            return "なんかエラー出た"

    def release(self):
        # 保存を実行（忘れると保存されないので注意）
        self.connection.commit()
        
        # 接続を閉じる
        self.connection.close()
