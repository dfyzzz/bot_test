import pandas as pd
from io import BytesIO
from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Booking


async def export_bookings_to_excel(bookings: List[Booking], start_date: datetime, end_date: datetime) -> BytesIO:
    """
    Export bookings to Excel file
    """
    # Prepare data for export
    data = []
    for booking in bookings:
        data.append({
            'Имя клиента': booking.user.name,
            'Телефон': booking.user.phone,
            'Услуга': booking.service.name if booking.service else 'Не указана',
            'Дата': booking.date.strftime('%Y-%m-%d'),
            'Время': booking.time.strftime('%H:%M'),
            'Статус': 'Подтверждена' if booking.confirmed else 'Ожидание',
            'Дата создания': booking.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Записи', index=False)
    
    # Set pointer to the beginning
    output.seek(0)
    
    return output