import pytest
import sys
from unittest.mock import patch, MagicMock
from main import main


class TestMain:
    """Тесты для функции main."""
    
    @patch('main.read_csv_files')
    @patch('main.generate_report')
    @patch('main.tabulate')
    @patch('builtins.print')
    def test_main_success_performance_report(self, mock_print, mock_tabulate, mock_generate_report, mock_read_csv_files):
        """Тест успешного выполнения с отчетом performance."""
        # Настройка моков
        mock_read_csv_files.return_value = [
            {'position': 'Developer', 'performance': 4.5}
        ]
        mock_generate_report.return_value = [
            {'position': 'Developer', 'performance': 4.5}
        ]
        mock_tabulate.return_value = 'formatted_table'
        
        # Симуляция аргументов командной строки
        test_args = ['main.py', '--files', 'test.csv', '--report', 'performance']
        
        with patch('sys.argv', test_args):
            result = main()
        
        assert result == 0
        mock_read_csv_files.assert_called_once_with(['test.csv'])
        mock_generate_report.assert_called_once()
        mock_tabulate.assert_called_once()
        mock_print.assert_called()
    
    @patch('main.read_csv_files')
    @patch('main.generate_report')
    @patch('main.tabulate')
    @patch('builtins.print')
    def test_main_success_other_report(self, mock_print, mock_tabulate, mock_generate_report, mock_read_csv_files):
        """Тест успешного выполнения с другим типом отчета."""
        mock_read_csv_files.return_value = [{'key': 'value'}]
        mock_generate_report.return_value = [{'key': 'value'}]
        mock_tabulate.return_value = 'formatted_table'
        
        test_args = ['main.py', '--files', 'test.csv', '--report', 'other']
        
        with patch('sys.argv', test_args):
            result = main()
        
        assert result == 0
        mock_tabulate.assert_called_once()
    
    @patch('main.read_csv_files')
    @patch('builtins.print')
    def test_main_empty_data(self, mock_print, mock_read_csv_files):
        """Тест обработки пустых данных."""
        mock_read_csv_files.return_value = []
        
        test_args = ['main.py', '--files', 'test.csv', '--report', 'performance']
        
        with patch('sys.argv', test_args):
            result = main()
        
        assert result == 0
        mock_print.assert_called_with("Нет данных для анализа")
    
    @patch('main.read_csv_files')
    @patch('builtins.print')
    def test_main_file_error(self, mock_print, mock_read_csv_files):
        """Тест обработки ошибки чтения файла."""
        mock_read_csv_files.side_effect = FileNotFoundError("Файл не найден")
        
        test_args = ['main.py', '--files', 'test.csv', '--report', 'performance']
        
        with patch('sys.argv', test_args):
            result = main()
        
        assert result == 1
        mock_print.assert_called()
        assert 'Ошибка' in str(mock_print.call_args)
    
    @patch('main.read_csv_files')
    @patch('main.generate_report')
    @patch('builtins.print')
    def test_main_report_error(self, mock_print, mock_generate_report, mock_read_csv_files):
        """Тест обработки ошибки генерации отчета."""
        mock_read_csv_files.return_value = [{'position': 'Developer', 'performance': 4.5}]
        mock_generate_report.side_effect = ValueError("Отчет не найден")
        
        test_args = ['main.py', '--files', 'test.csv', '--report', 'invalid']
        
        with patch('sys.argv', test_args):
            result = main()
        
        assert result == 1
        mock_print.assert_called()
        assert 'Ошибка' in str(mock_print.call_args)
    
    @patch('main.read_csv_files')
    @patch('main.generate_report')
    @patch('main.tabulate')
    @patch('builtins.print')
    def test_main_multiple_files(self, mock_print, mock_tabulate, mock_generate_report, mock_read_csv_files):
        """Тест обработки нескольких файлов."""
        mock_read_csv_files.return_value = [
            {'position': 'Developer', 'performance': 4.5}
        ]
        mock_generate_report.return_value = [
            {'position': 'Developer', 'performance': 4.5}
        ]
        mock_tabulate.return_value = 'formatted_table'
        
        test_args = ['main.py', '--files', 'file1.csv', 'file2.csv', '--report', 'performance']
        
        with patch('sys.argv', test_args):
            result = main()
        
        assert result == 0
        mock_read_csv_files.assert_called_once_with(['file1.csv', 'file2.csv'])

