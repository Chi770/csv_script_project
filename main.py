#!/usr/bin/env python3
import argparse
from tabulate import tabulate

from file_reader import read_csv_files
from reports import generate_report, get_available_reports


def main():
    parser = argparse.ArgumentParser(
        description='Генератор отчетов по эффективности разработчиков'
    )
    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help='Пути к CSV-файлам с данными'
    )
    parser.add_argument(
        '--report',
        required=True,
        help=f'Тип отчета. Доступные: {", ".join(get_available_reports())}'
    )
    
    args = parser.parse_args()
    
    try:
        # Чтение данных
        data = read_csv_files(args.files)
        
        if not data:
            print("Нет данных для анализа")
            return 0
        
        # Генерация отчета
        report_results = generate_report(args.report, data)
        
        # Форматирование вывода
        if args.report == 'performance':
            headers = ['№', 'position', 'performance']
            table_data = []
            for i, row in enumerate(report_results, 1):
                table_data.append([i, row['position'], row['performance']])
            
            print(tabulate(table_data, headers=headers))
        else:
            # Универсальный вывод для будущих отчетов
            print(tabulate(report_results, headers='keys'))
            
    except Exception as e:
        print(f"Ошибка: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
