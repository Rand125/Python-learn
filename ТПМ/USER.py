from flask import Flask, request
import pymysql

app = Flask(__name__)

# 2. Класс Database
class Database:
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost', 
            user='root', 
            password='ваш_пароль', # <-- Укажите пароль от MySQL
            database='flask_auth'
        )
        self.cursor = self.conn.cursor()

    # 3. Метод получения данных
    def get_user(self, username):
        self.cursor.execute("SELECT * FROM users WHERE user_name = %s", (username,))
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()

# 4. Проверка в роуте login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        db = Database()
        user = db.get_user(username)
        db.close()

        # Проверка: если юзер есть и пароль совпадает
        if user and user[2] == password:  # user[2] - это user_password
            return "Успешный вход!"
        else:
            return "Ошибка: неверный логин или пароль"
            
    # Простая форма для теста
    return '''
        <form method="post">
            Логин: <input name="username"><br>
            Пароль: <input name="password"><br>
            <button>Войти</button>
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
