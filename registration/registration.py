import sqlite3

DB_NAME = 'users.db'

def create_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY, email TEXT NOT NULL, password TEXT NOT NULL)''')
        conn.commit()

def add_user(username, email, password):
    if not username or not email or not password: return False
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute('INSERT INTO users VALUES (?, ?, ?)', (username, email, password))
            conn.commit()
        return True
    except sqlite3.IntegrityError: return False

def authenticate_user(username, password):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        return cursor.fetchone() is not None

def display_users():
    with sqlite3.connect(DB_NAME) as conn:
        for user in conn.execute('SELECT username, email FROM users'):
            print(f"Логин: {user[0]}, Электронная почта: {user[1]}")

def register_user(username, email, password):
    if not username: print("Ошибка: Логин не может быть пустым."); return False
    if not email: print("Ошибка: Email не может быть пустым."); return False
    if not password: print("Ошибка: Пароль не может быть пустым."); return False
    if add_user(username, email, password):
        print("Пользователь успешно зарегистрирован.")
        return True
    else: print("Ошибка регистрации."); return False

def main():
    create_db()
    display_users()

    choice = input("\n1. Авторизоваться\n2. Зарегистрироваться\nВведите ваш выбор (1/2): ")

    if choice == '1':
        username, password = input("Введите логин: "), input("Введите пароль: ")
        if authenticate_user(username, password): print("Авторизация успешна.")
        else: print("Неверный логин или пароль.")
    elif choice == '2':
        username, email, password = input("Введите логин: "), input("Введите email: "), input("Введите пароль: ")
        register_user(username, email, password)
    else: print("Неверный ввод.")

if __name__ == "__main__":
    main()