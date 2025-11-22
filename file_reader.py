import csv
from typing import List, Dict


def read_csv_files(file_paths: List[str]) -> List[Dict]:
    """
    Читает данные из нескольких CSV-файлов и возвращает объединенный список словарей.
    
    Args:
        file_paths: Список путей к CSV-файлам
        
    Returns:
        List[Dict]: Объединенные данные из всех файлов
    """
    all_data = []
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Конвертируем числовые поля
                    row['completed_tasks'] = int(row['completed_tasks'])
                    row['performance'] = float(row['performance'])
                    row['experience_years'] = int(row['experience_years'])
                    all_data.append(row)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        except Exception as e:
            raise Exception(f"Ошибка при чтении файла {file_path}: {str(e)}")
    
    return all_data
