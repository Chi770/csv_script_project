import pytest
from reports import ReportGenerator, get_available_reports, generate_report


class TestReportGenerator:
    """Тесты для класса ReportGenerator."""
    
    def test_performance_report_single_position(self):
        """Тест отчета по эффективности для одной должности."""
        data = [
            {'position': 'Developer', 'performance': 4.5},
            {'position': 'Developer', 'performance': 4.7},
            {'position': 'Developer', 'performance': 4.3}
        ]
        
        result = ReportGenerator.performance_report(data)
        
        assert len(result) == 1
        assert result[0]['position'] == 'Developer'
        assert result[0]['performance'] == 4.5  # (4.5 + 4.7 + 4.3) / 3 = 4.5
    
    def test_performance_report_multiple_positions(self):
        """Тест отчета по эффективности для нескольких должностей."""
        data = [
            {'position': 'Developer', 'performance': 4.5},
            {'position': 'QA', 'performance': 4.3},
            {'position': 'Developer', 'performance': 4.7},
            {'position': 'QA', 'performance': 4.1}
        ]
        
        result = ReportGenerator.performance_report(data)
        
        assert len(result) == 2
        # Должен быть отсортирован по убыванию эффективности
        assert result[0]['position'] == 'Developer'
        assert result[0]['performance'] == 4.6  # (4.5 + 4.7) / 2
        assert result[1]['position'] == 'QA'
        assert result[1]['performance'] == 4.2  # (4.3 + 4.1) / 2
    
    def test_performance_report_sorting(self):
        """Тест сортировки отчета по убыванию эффективности."""
        data = [
            {'position': 'Low', 'performance': 3.0},
            {'position': 'High', 'performance': 5.0},
            {'position': 'Medium', 'performance': 4.0}
        ]
        
        result = ReportGenerator.performance_report(data)
        
        assert len(result) == 3
        assert result[0]['position'] == 'High'
        assert result[0]['performance'] == 5.0
        assert result[1]['position'] == 'Medium'
        assert result[1]['performance'] == 4.0
        assert result[2]['position'] == 'Low'
        assert result[2]['performance'] == 3.0
    
    def test_performance_report_rounding(self):
        """Тест округления значений эффективности."""
        data = [
            {'position': 'Developer', 'performance': 4.333},
            {'position': 'Developer', 'performance': 4.666}
        ]
        
        result = ReportGenerator.performance_report(data)
        
        assert result[0]['performance'] == 4.5  # (4.333 + 4.666) / 2 = 4.4995 -> 4.5
        assert isinstance(result[0]['performance'], float)
    
    def test_performance_report_empty_data(self):
        """Тест отчета с пустыми данными."""
        result = ReportGenerator.performance_report([])
        assert result == []
    
    def test_performance_report_full_employee_data(self):
        """Тест отчета с полными данными сотрудников."""
        data = [
            {
                'name': 'John',
                'position': 'Developer',
                'completed_tasks': 10,
                'performance': 4.5,
                'skills': 'Python',
                'team': 'Team A',
                'experience_years': 2
            },
            {
                'name': 'Jane',
                'position': 'Developer',
                'completed_tasks': 15,
                'performance': 4.7,
                'skills': 'Java',
                'team': 'Team B',
                'experience_years': 3
            },
            {
                'name': 'Bob',
                'position': 'QA',
                'completed_tasks': 12,
                'performance': 4.3,
                'skills': 'Testing',
                'team': 'Team C',
                'experience_years': 2
            }
        ]
        
        result = ReportGenerator.performance_report(data)
        
        assert len(result) == 2
        assert result[0]['position'] == 'Developer'
        assert result[0]['performance'] == 4.6
        assert result[1]['position'] == 'QA'
        assert result[1]['performance'] == 4.3


class TestGetAvailableReports:
    """Тесты для функции get_available_reports."""
    
    def test_get_available_reports_returns_list(self):
        """Тест что функция возвращает список."""
        result = get_available_reports()
        assert isinstance(result, list)
    
    def test_get_available_reports_contains_performance(self):
        """Тест что список содержит отчет 'performance'."""
        result = get_available_reports()
        assert 'performance' in result
    
    def test_get_available_reports_not_empty(self):
        """Тест что список не пустой."""
        result = get_available_reports()
        assert len(result) > 0


class TestGenerateReport:
    """Тесты для функции generate_report."""
    
    def test_generate_performance_report(self):
        """Тест генерации отчета по эффективности."""
        data = [
            {'position': 'Developer', 'performance': 4.5},
            {'position': 'Developer', 'performance': 4.7}
        ]
        
        result = generate_report('performance', data)
        
        assert len(result) == 1
        assert result[0]['position'] == 'Developer'
        assert result[0]['performance'] == 4.6
    
    def test_generate_report_invalid_name(self):
        """Тест генерации отчета с неверным именем."""
        data = [{'position': 'Developer', 'performance': 4.5}]
        
        with pytest.raises(ValueError) as exc_info:
            generate_report('invalid_report', data)
        
        assert 'Отчет \'invalid_report\' не найден' in str(exc_info.value)
        assert 'Доступные отчеты' in str(exc_info.value)
    
    def test_generate_report_empty_data(self):
        """Тест генерации отчета с пустыми данными."""
        result = generate_report('performance', [])
        assert result == []
    
    def test_generate_report_with_real_data_structure(self):
        """Тест генерации отчета с реальной структурой данных."""
        data = [
            {
                'name': 'Alice',
                'position': 'Backend Developer',
                'completed_tasks': 43,
                'performance': 4.8,
                'skills': 'Java, Spring Boot',
                'team': 'API Team',
                'experience_years': 4
            },
            {
                'name': 'Bob',
                'position': 'Backend Developer',
                'completed_tasks': 45,
                'performance': 4.8,
                'skills': 'Python, Django',
                'team': 'API Team',
                'experience_years': 5
            },
            {
                'name': 'Charlie',
                'position': 'Frontend Developer',
                'completed_tasks': 38,
                'performance': 4.7,
                'skills': 'React, TypeScript',
                'team': 'Web Team',
                'experience_years': 4
            }
        ]
        
        result = generate_report('performance', data)
        
        assert len(result) == 2
        # Backend Developer должен быть первым (4.8 > 4.7)
        assert result[0]['position'] == 'Backend Developer'
        assert result[0]['performance'] == 4.8
        assert result[1]['position'] == 'Frontend Developer'
        assert result[1]['performance'] == 4.7

