import json
from datetime import datetime
ORDERS="orders.json"
SPENDING="spending.json"
def save_order_to_json(customs, total_sum, payment_type, comments,user_id, debt_comment=None):
    try:
        # Avvalgi events'ni o'qish
        with open(ORDERS, 'r') as file:
            orders = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        orders = []

    # Yangi event'ning id sini avtomatik inkrement qilish
    new_id = len(orders) + 1 
    orders.append({
        "id": new_id,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "telegram_user_id": user_id,
        "products": customs,
        "amount": total_sum,
        "debt_comment": debt_comment,
        "payment_type": payment_type,
        "comments": comments
    })
    with open(ORDERS, 'w') as file:
        json.dump(orders, file, indent=4)
    return new_id
def save_spend_to_json(spend_amount,comment,user_id,spend_type,worker=None):
    try:
        # Avvalgi events'ni o'qish
        with open(SPENDING, 'r') as file:
            spending = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        spending = []
        
    new_id = len(spending) + 1 
    spending.append({
        "id": new_id,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "telegram_user_id": user_id,
        "type": spend_type,
        "worker": worker or "",
        "comment": comment,
        "amount": spend_amount
    })
    with open(SPENDING, 'w') as file:
        json.dump(spending, file, indent=4)
    return new_id
def load_data(file_path: str) -> list:
    """Загружает данные из JSON файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
def show_order_info(order_id: int) -> str: 
    """Показывает информацию о заказе по его ID"""
    orders = load_data(ORDERS)
    for order in orders:
        if order['id'] == order_id:
            message = (
                f"ID: {order['id']}\n"
                f"Дата: {order['date']}\n"
                f"Telegram ID: {order['telegram_user_id']}\n"
                f"Товары: {', '.join(order['products'])}\n"
                f"Сумма: {order['amount']} сум\n"
                f"Способ оплаты: {order['payment_type']}\n"
                f"Комментарий: {order.get('comments', 'Нет')}\n"
                f"Задолженность: {order.get('debt_comment', 'Нет')}\n"
            )
            return message  
            
    return "Заказ не найден."
def delete_order(order_id: int) -> str:
    """Очищает данные заказа, сохраняя структуру с пустыми значениями"""
    orders = load_data(ORDERS)
    for order in orders:
        if order['id'] == order_id:
            # Устанавливаем пустые значения для каждого поля
            order.update({
                'date': '',
                'telegram_user_id': 0,
                'products': [],
                'amount': 0,
                'payment_type': '',
                'comments': '',
                'debt_comment': ''
            })
            
            with open(ORDERS, 'w') as file:
                json.dump(orders, file, indent=4)
            message = f"Заказ с ID {order_id} очищен (все данные сброшены)."
            return message
    return "Заказ не найден."
def show_spend_info(spend_id: int) -> str:
    """Показывает информацию о расходе по его ID"""
    spending = load_data(SPENDING)
    
    for spend in spending:
        if spend['id'] == spend_id:
            try:
                type_of_spend = spend['type']
            except KeyError:
                type_of_spend = "Неизвестный тип"
            try:
                worker = spend['worker']
            except KeyError:
                worker = "Неизвестный работник"
            message = (
                f"ID: {spend['id']}\n"
                f"Дата: {spend['date']}\n"
                f"Telegram ID: {spend['telegram_user_id']}\n"
                f"Тип расхода: {type_of_spend}\n"  
                f"Работник: {worker}\n"    
                f"Комментарий: {spend['comment']}\n"
                f"Сумма: {spend['amount']} сум\n"
            )
            return message
    return "Расход не найден."
def delete_spend(spend_id: int) -> str:
    """Очищает данные расхода, сохраняя структуру с пустыми значениями"""
    spending = load_data(SPENDING)
    for spend in spending:
        if spend['id'] == spend_id:
            # Устанавливаем пустые значения для каждого поля
            spend.update({
                'date': '',
                'telegram_user_id': 0,
                'type': '',
                'worker': '',
                'comment': '',
                'amount': 0
            })

            with open(SPENDING, 'w') as file:
                json.dump(spending, file, indent=4)
            message = f"Расход с ID {spend_id} очищен (все данные сброшены)."
            return message
    return "Расход не найден."
