from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder
from aiogram.types import KeyboardButton,InlineKeyboardButton,ReplyKeyboardMarkup,InlineKeyboardMarkup
from main import PRODUCT_NAMES,PRODUCT_PRICES
async def start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🛍️Продажа",callback_data="sell"),
        InlineKeyboardButton(text="📝Расход/Трата",callback_data="spend"),
    )    
    builder.adjust(2)
    return builder.as_markup()
from collections import Counter
async def admin_start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🛍️Продажа",callback_data="sell"),
        InlineKeyboardButton(text="📝Расход/Трата",callback_data="spend"),
        InlineKeyboardButton(text="📊Отчет",callback_data="report"),
        
    )    
    builder.adjust(2)
    return builder.as_markup()
async def key_reports():
    builder= ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="💰 Расходы"),
        KeyboardButton(text="💰 Продажа"),
        
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
async def custom_keyboard_sell(custom: str = None, customs: list = None):
    if customs is None:
        customs = []
    if custom and custom not in customs:
        customs.append(custom)

    counts = Counter(customs)
    total_sum = 0

    # Mahsulotlar ro‘yxati matni
    text = "<b>📦 Tanlangan mahsulotlar:</b>\n\n"
    for code, count in counts.items():
        name = PRODUCT_NAMES.get(code, code)
        price = PRODUCT_PRICES.get(code, 0)
        total = price * count
        total_sum += total
        text += f"• {name}: {count} x {price} = {total} so‘m\n"
    if not counts:
        text += "❌ Mahsulot tanlanmagan\n"
    else:
        text += f"\n<b>💸 Umumiy summa:</b> {total_sum} so‘m"

    # Klaviatura
    keyboard = InlineKeyboardBuilder()
    buttons = [
        ("Мор 5000", "add_MOR5000"),
        ("➖", "subtract_MOR5000"),
        ("Мор 10000", "add_MOR10000"),
        ("➖", "subtract_MOR10000"),
        ("Мор 15000", "add_MOR15000"),
        ("➖", "subtract_MOR15000"),
        ("Самса 8000", "add_SAM8000"),
        ("➖", "subtract_SAM8000"),
        ("Самса 2X -15000", "add_SAM2X15000"),
        ("➖", "subtract_SAM2X15000"),
        ("Самса 6000", "add_SAMSA6000"),
        ("➖", "subtract_SAMSA6000"),
        ("Кур. САМСА 8000", "add_KSAMSA8000"),
        ("➖", "subtract_KSAMSA8000"),
        ("Кур. САМСА 15000", "add_KSAMSA15000"),
        ("➖", "subtract_KSAMSA15000"),
        ("Хот-дог 10000", "add_hotdog10000"),
        ("➖", "subtract_hotdog10000"),
        ("Хот-дог 15000", "add_hotdog15000"),
        ("➖", "subtract_hotdog15000"),
        ("Хот-дог 20000", "add_hotdog20000"),
        ("➖", "subtract_hotdog20000"),
        ("Хот-дог 25000", "add_hotdog25000"),
        ("➖", "subtract_hotdog25000"),
        ("Соус 5000", "add_sous5000"),
        ("➖", "subtract_sous5000"),
        ("Соус 2000", "add_sous2000"),
        ("➖", "subtract_sous2000")
    ]
    for text_btn, callback_data in buttons:
        keyboard.add(InlineKeyboardButton(text=text_btn, callback_data=callback_data))

    keyboard.add(
        
        InlineKeyboardButton(text="🏠Главная страница", callback_data="BackToStartPanel"),
        InlineKeyboardButton(text="📩Отправить", callback_data="send_custom")
    )
    keyboard.adjust(2)

    return text, keyboard.as_markup()
def payment_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💵 Наличка/перевод", callback_data="pay_cash")],
        [InlineKeyboardButton(text="💳 Карта", callback_data="pay_card")],
        [InlineKeyboardButton(text="📝 В долг", callback_data="pay_debt")],
        [InlineKeyboardButton(text="🪄 Смешанный", callback_data="pay_mixed")],
    ])
async def skip_key():
    builder=ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Пропустить"))
    return builder.as_markup(resize_keyboard=True)
async def generate_time_period_keyboard(report_type: str) -> InlineKeyboardMarkup:
    """Генерирует клавиатуру для выбора периода отчета"""
    builder = InlineKeyboardBuilder()
    
    buttons = [
        ("📅 Отчет за день", f"report:{report_type}:day"),
        ("📅 Отчет за неделю", f"report:{report_type}:week"),
        ("📅 Отчет за месяц", f"report:{report_type}:month"),
        ("📅 Отчет за год", f"report:{report_type}:year"),
        ("📅 За все время", f"report:{report_type}:all"),
        ("🔙 На главную", "BackToStartPanel")
    ]
    
    for text, callback_data in buttons:
        builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    
    builder.adjust(2)
    return builder.as_markup()