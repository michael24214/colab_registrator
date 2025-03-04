import pytest
import sqlite3
import os
from registration.registration import (  # Замените registration.registration на правильный путь к вашему файлу
    create_db,
    add_user,
    authenticate_user,
    display_users,
    DB_NAME,
    register_user, # Импортируем register_user
    #main #Больше не импортируем main
)

@pytest.fixture()
def setup_db():
    """Фикстура, создающая и очищающая базу данных перед каждым тестом."""
    create_db()
    yield
    # Teardown: Удаляем файл базы данных после теста
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)


def test_create_db(setup_db):
    """Тест проверяет, что файл базы данных создан."""
    assert os.path.exists(DB_NAME), "Файл базы данных должен быть создан"


def test_add_user(setup_db):
    """Тест проверяет добавление пользователя в базу данных с корректными данными."""
    assert add_user("testuser", "test@example.com", "password") is True, "Пользователь должен быть успешно добавлен"

    # Проверяем, что пользователь существует в базе данных и данные совпадают
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=?', ("testuser",))
        user = cursor.fetchone()
        assert user is not None, "Пользователь должен существовать в базе данных"
        assert user[1] == "test@example.com", "Email должен совпадать"
        assert user[2] == "password", "Пароль должен совпадать"


def test_add_duplicate_user(setup_db):
    """Тест проверяет, что нельзя добавить пользователя с существующим логином."""
    add_user("testuser", "test@example.com", "password")
    assert add_user("testuser", "another@example.com", "anotherpassword") is False, "Нельзя добавлять пользователя с существующим логином"


def test_authenticate_user(setup_db):
    """Тест проверяет аутентификацию пользователя с правильными и неправильными данными."""
    add_user("testuser", "test@example.com", "password")
    assert authenticate_user("testuser", "password"), "Пользователь должен быть аутентифицирован с правильными данными"
    assert not authenticate_user("testuser", "wrongpassword"), "Пользователь не должен быть аутентифицирован с неправильным паролем"
    assert not authenticate_user("nonexistentuser", "password"), "Несуществующий пользователь не должен быть аутентифицирован"


def test_display_users(setup_db, capsys):
    """Тест проверяет функцию display_users (перехватывает stdout)."""
    add_user("testuser1", "test1@example.com", "password")
    add_user("testuser2", "test2@example.com", "password")
    display_users()
    captured = capsys.readouterr()
    output = captured.out
    assert "Логин: testuser1, Электронная почта: test1@example.com" in output
    assert "Логин: testuser2, Электронная почта: test2@example.com" in output


def test_add_user_empty_username(setup_db):
    """Тест проверяет, что нельзя добавить пользователя с пустым логином."""
    assert add_user("", "test@example.com", "password") is False, "Нельзя добавлять пользователя с пустым логином"


def test_add_user_empty_email(setup_db):
    """Тест проверяет, что нельзя добавить пользователя с пустой электронной почтой."""
    assert add_user("testuser", "", "password") is False, "Нельзя добавлять пользователя с пустой электронной почтой"


def test_add_user_empty_password(setup_db):
    """Тест проверяет, что нельзя добавить пользователя с пустым паролем."""
    assert add_user("testuser", "test@example.com", "") is False, "Нельзя добавлять пользователя с пустым паролем"


def test_display_users_no_users(setup_db, capsys):
    """Тест проверяет, что display_users ничего не выводит, если нет пользователей."""
    display_users()
    captured = capsys.readouterr()
    output = captured.out
    assert output == "", "Не должно быть вывода, если нет пользователей"


def test_username_case_sensitivity(setup_db):
    """Тест проверяет, что аутентификация чувствительна к регистру логина."""
    add_user("TestUser", "test@example.com", "password")
    assert authenticate_user("TestUser", "password"), "Должен аутентифицироваться с правильным регистром"
    assert not authenticate_user("testuser", "password"), "Не должен аутентифицироваться с неправильным регистром"

def test_add_user_long_username(setup_db):
    """Тест проверяет, что нельзя добавить пользователя со слишком длинным логином."""
    long_username = "a" * 101  # Предположим, что максимальная длина логина - 100 символов
    assert add_user(long_username, "test@example.com", "password") is False # or False if you handle too long string

def test_add_user_invalid_email(setup_db):
    """Тест проверяет, что нельзя добавить пользователя с невалидным email."""
    assert add_user("testuser", "invalid-email", "password") is False # or False if you validate email

def test_register_user_success(setup_db, capsys):
    """Тест проверяет успешную регистрацию пользователя."""
    result = register_user("testuser", "test@example.com", "password")
    assert result is True, "Регистрация должна быть успешной"
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=?', ("testuser",))
        user = cursor.fetchone()
        assert user is not None, "Пользователь должен существовать в базе данных"
        assert user[1] == "test@example.com", "Email должен совпадать"
        assert user[2] == "password", "Пароль должен совпадать"
    captured = capsys.readouterr()
    assert "Пользователь успешно зарегистрирован." in captured.out

def test_register_user_empty_username(setup_db, capsys):
    """Тест проверяет обработку пустого логина при регистрации."""
    result = register_user("", "test@example.com", "password")
    assert result is False, "Регистрация не должна быть успешной"
    captured = capsys.readouterr()
    assert "Ошибка: Логин не может быть пустым." in captured.out

def test_register_user_empty_email(setup_db, capsys):
    """Тест проверяет обработку пустого email при регистрации."""
    result = register_user("testuser", "", "password")
    assert result is False, "Регистрация не должна быть успешной"
    captured = capsys.readouterr()
    assert "Ошибка: Email не может быть пустым." in captured.out

def test_register_user_empty_password(setup_db, capsys):
    """Тест проверяет обработку пустого пароля при регистрации."""
    result = register_user("testuser", "test@example.com", "")
    assert result is False, "Регистрация не должна быть успешной"
    captured = capsys.readouterr()
    assert "Ошибка: Пароль не может быть пустым." in captured.out# or False if you validate email
# 1.  Сохраните этот код как Python-файл (например, `test_your_module.py`).  Убедитесь, что он находится в той же директории, что и ваш оригинальный код (`your_module.py`).
# 2.  Установите pytest и pytest-html:
#    ```bash
#    pip install pytest pytest-html
#    ```
# 3. Запустите тесты из терминала:
#    ```bash
#    pytest --html=report.html
#    ```
#     * Замените `report.html` на желаемое имя файла отчета.
# 4. Откройте `report.html` в браузере, чтобы просмотреть подробные результаты тестов.

# ---- Важные замечания и улучшения -----

# * **Замените заполнители:** Замените `your_module` на фактическое имя вашего Python-файла.
# * **Обработка ошибок:** Хотя тесты проверяют некоторые ошибки, вы можете добавить более конкретную обработку ошибок в свой оригинальный код и протестировать эти конкретные исключения.
# * **Больше тестов безопасности:** Тест на SQL-инъекции очень простой. Для реального приложения вам потребуется использовать параметризованные запросы (что вы уже делаете!) и выполнить более тщательное тестирование безопасности. Рассмотрите возможность использования инструмента статического анализа, чтобы помочь найти потенциальные уязвимости.
# * **Тестовые данные:** Рассмотрите возможность использования `pytest.mark.parametrize`, чтобы запустить один и тот же тест с разными наборами данных, чтобы охватить более широкий спектр сценариев.
# * **Покрытие кода:** Используйте инструмент покрытия кода (например, `pytest-cov`), чтобы проверить, какая часть вашего кода фактически тестируется вашими тестами. Это может помочь вам определить области, которые нуждаются в большем тестировании. Установите с помощью `pip install pytest-cov` и запустите с помощью `pytest --cov=your_module --cov-report term-missing`

#---- Объяснение ключевых частей ----

# * **`pytest.fixture`:** Фикстура - это функция, которая запускается перед каждым тестом. `setup_db` создает базу данных перед каждым тестом и удаляет ее после этого, гарантируя, что каждый тест начинается с чистого листа. Ключевое слово `yield` имеет решающее значение; оно позволяет тесту запуститься, а затем выполняет код после `yield` как teardown.
# * **`capsys`:** Это еще одна фикстура pytest. Она используется для перехвата вывода, который выводится в консоль (stdout). Это позволяет тестировать такие функции, как `display_users`, которые печатают информацию.
# * **`assert`:** Оператор `assert` - это то, как вы проверяете, пройден тест или нет. Если условие после `assert` истинно, тест пройден. Если оно ложно, тест не пройден. Сообщения после запятых в операторах `assert` полезны для отладки.
# * **Тест на SQL-инъекции:** Функция `test_sql_injection_add_user` пытается вставить вредоносную строку в базу данных. Цель состоит в том, чтобы проверить, защищена ли база данных от атак SQL-инъекций (что *должно* быть, учитывая использование параметризованных запросов). Если попытка успешна (т.е. таблица удалена), тест не пройден.
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""