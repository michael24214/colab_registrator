# run_tests.py
import pytest
import os
import webbrowser
from bs4 import BeautifulSoup  # Import BeautifulSoup

# Настройки
COVERAGE_REPORT_DIR = "htmlcov"  # Папка для HTML-отчета

def run_tests():
    """Запускает тесты pytest с покрытием кода и создает HTML-отчет."""
    pytest.main([
        "--cov=registration",  # Укажите пакет для измерения покрытия
        "--cov-report=html:" + COVERAGE_REPORT_DIR,  # Создать HTML-отчет
        "tests/test_registration.py" # Укажите файл с тестами
    ])

def get_coverage_percentage(report_dir):
    """Извлекает процент покрытия кода из HTML-отчета."""
    index_file = os.path.join(report_dir, "index.html")
    try:
        with open(index_file, "r") as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        coverage_percentage = soup.find('tfoot').find_all('td')[-1].text.strip() # Gets last td element inside tfoot tag

        return coverage_percentage
    except FileNotFoundError:
        print(f"Ошибка: Файл отчета не найден: {index_file}")
        return "N/A"
    except Exception as e:
        print(f"Ошибка при чтении отчета: {e}")
        return "N/A"

def open_html_report(report_dir):
    """Открывает HTML-отчет в браузере."""
    index_file = os.path.join(report_dir, "index.html")
    report_url = "file://" + os.path.abspath(index_file)
    try:
        webbrowser.open(report_url)
    except Exception as e:
        print(f"Ошибка при открытии HTML-отчета в браузере: {e}")

if __name__ == "__main__":
    run_tests()
    coverage = get_coverage_percentage(COVERAGE_REPORT_DIR)
    print(f"Процент покрытия кода: {coverage}")
    open_html_report(COVERAGE_REPORT_DIR)