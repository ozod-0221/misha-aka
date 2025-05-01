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
def save_spend_to_json(spend_amount,comment,user_id):
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
