from typing import List, Dict, Any
from collections import defaultdict


class ReportGenerator:
    """Базовый класс для генерации отчетов."""
    
    @staticmethod
    def performance_report(data: List[Dict]) -> List[Dict[str, Any]]:
        """
        Генерирует отчет по средней эффективности по должностям.
        
        Args:
            data: Список словарей с данными сотрудников
            
        Returns:
            List[Dict]: Отсортированный список с средней эффективностью по должностям
        """
        position_stats = defaultdict(list)
        
        # Группируем performance по должностям
        for employee in data:
            position = employee['position']
            performance = employee['performance']
            position_stats[position].append(performance)
        
        # Вычисляем среднее для каждой должности
        report_data = []
        for position, performances in position_stats.items():
            avg_performance = sum(performances) / len(performances)
            report_data.append({
                'position': position,
                'performance': round(avg_performance, 2)
            })
        
        # Сортируем по убыванию эффективности
        report_data.sort(key=lambda x: x['performance'], reverse=True)
        
        return report_data


# Реестр доступных отчетов для легкого добавления новых
REPORT_REGISTRY = {
    'performance': ReportGenerator.performance_report
}


def get_available_reports():
    """Возвращает список доступных отчетов."""
    return list(REPORT_REGISTRY.keys())


def generate_report(report_name: str, data: List[Dict]) -> List[Dict[str, Any]]:
    """
    Генерирует указанный отчет на основе данных.
    
    Args:
        report_name: Название отчета
        data: Данные для анализа
        
    Returns:
        List[Dict]: Результаты отчета
    """
    if report_name not in REPORT_REGISTRY:
        available_reports = ', '.join(get_available_reports())
        raise ValueError(f"Отчет '{report_name}' не найден. Доступные отчеты: {available_reports}")
    
    return REPORT_REGISTRY[report_name](data)
