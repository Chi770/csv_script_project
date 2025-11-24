# Анализ эффективности разработчиков

Скрипт для анализа данных о разработчиках и генерации отчетов.

## Установка

1. Клонируйте репозиторий

2. Установите виртуальное окружение:
python -m venv venv 

3. Активируйте виртуальное окружение:
source venv/Scripts/activate

4. Установите зависимости:
pip install -r requirements.txt

5. Запустите скрипт: 
python main.py --file employees_data/employees1.csv employees_data/employees2.csv --report performance

6. Запустите тесты:
pytest --cov=. tests/ -v
