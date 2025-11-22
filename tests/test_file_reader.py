import pytest
import csv
import tempfile
import os
from file_reader import read_csv_files


class TestReadCsvFiles:
    """Тесты для функции read_csv_files."""
    
    def test_read_single_csv_file(self):
        """Тест чтения одного CSV файла."""
        # Создаем временный CSV файл
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'position', 'completed_tasks', 'performance', 'skills', 'team', 'experience_years'])
            writer.writerow(['John Doe', 'Developer', '10', '4.5', 'Python', 'Team A', '2'])
            temp_path = f.name
        
        try:
            result = read_csv_files([temp_path])
            
            assert len(result) == 1
            assert result[0]['name'] == 'John Doe'
            assert result[0]['position'] == 'Developer'
            assert result[0]['completed_tasks'] == 10
            assert result[0]['performance'] == 4.5
            assert result[0]['experience_years'] == 2
        finally:
            os.unlink(temp_path)
    
    def test_read_multiple_csv_files(self):
        """Тест чтения нескольких CSV файлов."""
        temp_files = []
        
        try:
            # Создаем первый файл
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['name', 'position', 'completed_tasks', 'performance', 'skills', 'team', 'experience_years'])
                writer.writerow(['Alice', 'Developer', '15', '4.7', 'Python', 'Team A', '3'])
                temp_files.append(f.name)
            
            # Создаем второй файл
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['name', 'position', 'completed_tasks', 'performance', 'skills', 'team', 'experience_years'])
                writer.writerow(['Bob', 'QA', '12', '4.3', 'Testing', 'Team B', '2'])
                temp_files.append(f.name)
            
            result = read_csv_files(temp_files)
            
            assert len(result) == 2
            assert result[0]['name'] == 'Alice'
            assert result[1]['name'] == 'Bob'
        finally:
            for path in temp_files:
                os.unlink(path)
    
    def test_data_type_conversion(self):
        """Тест конвертации типов данных."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'position', 'completed_tasks', 'performance', 'skills', 'team', 'experience_years'])
            writer.writerow(['Test', 'Dev', '25', '4.8', 'Skills', 'Team', '5'])
            temp_path = f.name
        
        try:
            result = read_csv_files([temp_path])
            
            assert isinstance(result[0]['completed_tasks'], int)
            assert isinstance(result[0]['performance'], float)
            assert isinstance(result[0]['experience_years'], int)
            assert result[0]['completed_tasks'] == 25
            assert result[0]['performance'] == 4.8
            assert result[0]['experience_years'] == 5
        finally:
            os.unlink(temp_path)
    
    def test_file_not_found_error(self):
        """Тест обработки ошибки отсутствующего файла."""
        with pytest.raises(FileNotFoundError) as exc_info:
            read_csv_files(['nonexistent_file.csv'])
        
        assert 'Файл не найден' in str(exc_info.value)
        assert 'nonexistent_file.csv' in str(exc_info.value)
    
    def test_invalid_csv_format(self):
        """Тест обработки некорректного формата CSV."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
            # Создаем файл с некорректными данными (отсутствует поле)
            f.write('name,position\n')
            f.write('John,Developer\n')
            f.write('Jane')  # Неполная строка
            temp_path = f.name
        
        try:
            # Ожидаем ошибку при чтении некорректного CSV
            with pytest.raises(Exception) as exc_info:
                read_csv_files([temp_path])
            
            assert 'Ошибка при чтении файла' in str(exc_info.value)
        finally:
            os.unlink(temp_path)
    
    def test_missing_required_fields(self):
        """Тест обработки отсутствующих обязательных полей."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'position'])  # Отсутствуют обязательные поля
            writer.writerow(['John', 'Developer'])
            temp_path = f.name
        
        try:
            with pytest.raises(Exception) as exc_info:
                read_csv_files([temp_path])
            
            assert 'Ошибка при чтении файла' in str(exc_info.value)
        finally:
            os.unlink(temp_path)
    
    def test_empty_csv_file(self):
        """Тест чтения пустого CSV файла (только заголовки)."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'position', 'completed_tasks', 'performance', 'skills', 'team', 'experience_years'])
            temp_path = f.name
        
        try:
            result = read_csv_files([temp_path])
            assert len(result) == 0
            assert result == []
        finally:
            os.unlink(temp_path)
    
    def test_empty_file_list(self):
        """Тест обработки пустого списка файлов."""
        result = read_csv_files([])
        assert result == []
    
    def test_float_performance_values(self):
        """Тест обработки различных значений performance."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'position', 'completed_tasks', 'performance', 'skills', 'team', 'experience_years'])
            writer.writerow(['Test1', 'Dev', '10', '3.14', 'Skills', 'Team', '1'])
            writer.writerow(['Test2', 'Dev', '20', '5.0', 'Skills', 'Team', '2'])
            temp_path = f.name
        
        try:
            result = read_csv_files([temp_path])
            
            assert result[0]['performance'] == 3.14
            assert result[1]['performance'] == 5.0
        finally:
            os.unlink(temp_path)

