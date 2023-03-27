import sqlite3

new_login = None
new_password = None
new_code = None
check_login = None


class DataBase:
    """Класс для работы с базой данных"""

    def __init__(self, db_file):
        self.con = sqlite3.connect(db_file)
        self.cur = self.con.cursor()

    def create_table(self, request):
        """Создание таблицы"""
        with self.con:
            self.cur.execute(request)
            self.con.commit()
            return True

    def check_user(self, login):
        with self.con:
            result = self.cur.execute("""SELECT Login FROM users_data""").fetchall()
            if login not in (user[0] for user in result):
                return True
            else:
                print("Пользователь с таким именем уже существует")
                new_user_login()

    def insert_user(self, login, password, code):
        """Создание пользователя"""
        with self.con:
            result = self.cur.execute("""SELECT Login FROM users_data""").fetchall()
            if login not in (user[0] for user in result):
                self.cur.execute("""INSERT INTO 'users_data'
                ('Login', 'Password', 'Code') VALUES(?, ?, ?);""", (login, password, code,))
                self.con.commit()
                print(f'Создан новый пользователь: {login}')
                return True
            else:
                print("Пользователь с таким именем уже существует")
                return False

    def check_login(self):
        global check_login
        check_login = input("Введите логин: ").strip()
        with self.con:
            result = self.cur.execute("SELECT Login FROM users_data WHERE Login = ?", (check_login,)).fetchone()
            if result is None:
                print("Пользователь с таким логином не найден")
                self.check_login()
            else:
                print("Пользователь найден")
                return True

    def check_password(self, login):
        check_password = input("Введите пароль: ").strip()
        with self.con:
            result = self.cur.execute("SELECT Password FROM users_data WHERE Login = ?", (login,)).fetchone()
            if check_password != result[0]:
                print("Вы ввели неверный пароль")
                self.check_password(login)
            else:
                print("Пароль принят")
                return True

    def check_code(self, code, login):
        with self.con:
            result = self.cur.execute("SELECT Code FROM users_data WHERE Login = ?", (login,)).fetchone()
            if code == result[0]:
                print("Код принят")
                return True
            else:
                print("Вы ввели неверный код")
                new_user_code()
                self.check_code(code, login)

    def update_password(self, login, password):
        with self.con:
            self.cur.execute("UPDATE users_data SET Password = ? WHERE Login = ?", (password, login,))
            self.con.commit()
            print("Новый пароль успешно установлен")
            return True


def new_user_login():
    global new_login
    new_login = input("Введите логин: ")
    if len(new_login) < 4:
        print("Логин должен быть больше 3 символов")
        new_user_login()
    elif len(new_login) > 12:
        print("Логин не должен превышать 12 символов")
        new_user_login()
    elif not new_login.isascii() or ' ' in new_login:
        print("Логин должен содержать только латиницу, цифры или знаки ascii")
        new_user_login()
    elif new_login.isdigit():
        print("Логин должен содержать хотя бы 1 латинскую букву")
        new_user_login()
    else:
        return True


def new_user_password():
    global new_password
    new_password = input("Введите пароль: ")
    if len(new_password) < 8:
        print("Пароль должен быть больше 7 символов")
        new_user_password()
    elif not new_password.isascii() or ' ' in new_password:
        print("Пароль может содержать латинские буквы, цифры и знаки из таблицы ascii")
        new_user_password()
    else:
        return True


def new_user_code():

    global new_code
    new_code = input("Введите код: ")
    if len(new_code) == 4 and new_code.isdigit():
        return True
    else:
        print("Код должен состоять из 4 цифр")
        new_user_code()


def select_action():
    try:
        print()
        action = int(input("Выбери действие: \n"
                           "Регистрация в системе - 1 \n"
                           "Авторизоваться в системе - 2 \n"
                           "Изменить пароль в системе - 3 \n"
                           "Покинуть систему - 4 \n").strip())
        if action > 4 or action < 1:
            print("Вы ввели не корректное значение")
            select_action()
        return action
    except ValueError:
        print("Вы ввели не корректное значение")


def main():
    data = DataBase('registration.db')
    data.create_table("""CREATE TABLE IF NOT EXISTS users_data(
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Login TEXT NOT NULL,
    Password TEXT NOT NULL,
    Code INTEGER NOT NULL);""")
    data.insert_user("Ivan", "qwer1234", 1234)

    while True:
        action = select_action()
        if action == 1:
            new_user_login()
            data.check_user(new_login)
            new_user_password()
            new_user_code()
            data.insert_user(new_login, new_password, new_code)
            print("Регистрация прошла успешно")

        elif action == 2:
            data.check_login()
            data.check_password(check_login)
            print("Авторизация прошла успешно")

        elif action == 3:
            data.check_login()
            new_user_code()
            data.check_code(new_code, check_login)
            new_user_password()
            data.update_password(check_login, new_password)

        elif action == 4:
            print("До свидания!")
            break


if __name__ == '__main__':
    main()
