import pandas as pd
from datetime import datetime
import json
import os
from json_utils import *
from typing import Optional
from datetime import timedelta
def filter_by_period(data: list, period: str) -> pd.DataFrame:
    """Фильтрует данные по выбранному периоду"""
    if not data:
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    
    now = datetime.now()
    periods = {
        'day': now - timedelta(days=1),
        'week': now - timedelta(weeks=1),
        'month': now - timedelta(days=30),
        'year': now - timedelta(days=365),
        'all': datetime.min
    }
    
    start_date = periods.get(period, periods['day'])
    return df[df['date'] >= start_date]
async def generate_report(report_type: str, period: str) -> tuple:
    
    """Генерирует отчет и возвращает текст и файл"""
    file_path = SPENDING if report_type == 'spend' else ORDERS
    report_name = "Расходы" if report_type == 'spend' else "Заказы"
    
    df = filter_by_period(load_data(file_path), period)
    
    if df.empty:
        return f"Отчет по {report_name.lower()}:\nДанные за выбранный период не найдены", None
    
    # Генерация статистики
    total = df['amount'].sum() if 'amount' in df.columns else 0
    count = len(df)
    
    period_names = {
        'day': "последний день",
        'week': "последнюю неделю",
        'month': "последний месяц",
        'year': "последний год",
        'all': "все время"
    }
    
    # Создание Excel файла
    filename = f"{report_name}_{period}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    df.to_excel(filename, index=False)
    
    # Текст сообщения
    message = (
        f"📊 <b>{report_name} за {period_names.get(period, 'период')}</b>\n\n"
        f"🔄 Количество записей: <b>{count}</b>\n"
        f"💰 Общая сумма: <b>{total:.2f}</b>\n\n"
        f"📎 Полный отчет прикреплен в файле"
    )
    
    return message, filename