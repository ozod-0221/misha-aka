from aiogram import Bot, Dispatcher,F
from datetime import datetime,timedelta
from aiogram.types import Message,CallbackQuery
from aiogram.filters import Command,CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
import asyncio
import logging
from keyboards import *
from excel import *
from json_utils import *
from aiogram.types import FSInputFile
import os
from dotenv import load_dotenv
load_dotenv()
class CustomSell(StatesGroup):
    waiting_for_custom = State()
    waiting_for_payment= State()
    waiting_for_debt_comment = State()
    waiting_for_comments = State()
class Spend(StatesGroup):
    waiting_for_spend_type = State()
    waiting_for_worker = State()
    waiting_for_spend_amount = State()
    waiting_for_spend_comment = State()
admin_filter = F.from_user.id.in_([5361589149,5792568362])
class Spend_report(StatesGroup):
    waiting_for_spend_report = State()
class Order_report(StatesGroup):
    waiting_for_order_report = State()
    
TOKEN= os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()
PRODUCT_NAMES = {
    "MOR5000": "Мор 5000",
    "MOR10000": "Мор 10000",
    "MOR15000": "Мор 15000",
    "MSAM8000": "гов.Самса 8000",
    "MSAM7500": "гов.Самса 7500",
    "SAMSA6000": "Самса 6000",
    "KSAMSA8000": "Кур. САМСА 8000",
    "KSAMSA7500": "Кур. САМСА 7500",
    "hotdog10000": "Хот-дог 10000",
    "hotdog15000": "Хот-дог 15000",
    "hotdog20000": "Хот-дог 20000",
    "hotdog25000": "Хот-дог 25000",
    "sous5000": "Соус 5000",
    "sous2000": "Соус 2000",
    "tea3000": "Чай 3000",
    "tea5000": "Чай 5000",
    "cup1000": "Чашка 1000",
}

PRODUCT_PRICES = {
    "MOR5000": 5000,
    "MOR10000": 10000,
    "MOR15000": 15000,
    "MSAM8000": 8000,
    "MSAM7500": 7500,
    "SAMSA6000": 6000,
    "KSAMSA8000": 8000,
    "KSAMSA7500": 7500,
    "hotdog10000": 10000,
    "hotdog15000": 15000,
    "hotdog20000": 20000,
    "hotdog25000": 25000,
    "sous5000": 5000,
    "sous2000": 2000,
    "tea3000": 3000,
    "tea5000": 5000,
    "cup1000": 1000,
}


@dp.message(CommandStart())
async def start(message: Message,bot: Bot,state: FSMContext):
    if message.from_user.id == 5361589149 or message.from_user.id == 5792568362:
        await message.answer("главное меню:",reply_markup=await admin_start_keyboard())
    else:
        await bot.send_message(message.from_user.id,"главное меню:",reply_markup=ReplyKeyboardRemove())
        await message.reply(f"Привет,{message.from_user.full_name}!\nВыбери,что хочешь сделать:",reply_markup=await start_keyboard())
    await state.clear()
    
    

@dp.callback_query(F.data == "BackToStartPanel")
async def back_to_start_panel(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if callback.from_user.id == 5361589149 or callback.from_user.id == 5792568362:
        await callback.answer()
        await bot.send_message(callback.from_user.id,"привет:",reply_markup=ReplyKeyboardRemove())
        await bot.send_message(callback.from_user.id,"главное меню:",reply_markup=await admin_start_keyboard())
        await state.clear()
    else:
        await callback.answer()
        await bot.send_message(callback.from_user.id,"главное меню:",reply_markup=ReplyKeyboardRemove())
        await bot.send_message(callback.from_user.id,"Привет,{callback.from_user.full_name}!\nВыбери,что хочешь сделать:",reply_markup=await start_keyboard())
        await state.clear()
    
    
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

@dp.callback_query(F.data == "sell")
async def sell(callback: CallbackQuery, state: FSMContext,bot: Bot):
    await callback.answer()
    customs=[]
    await state.set_state(CustomSell.waiting_for_custom)
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await state.update_data(customs=[]) 
    
    text, keyboard = await custom_keyboard_sell(customs=customs)
    await callback.message.answer("Выбери товар", reply_markup=keyboard,parse_mode="HTML")
@dp.callback_query(F.data.startswith("add_") | F.data.startswith("subtract_"))
async def handle_custom_buttons(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    customs = data.get("customs", [])

    action, code = query.data.split("_", 1)

    if action == "add":
        customs.append(code)
    elif action == "subtract" and code in customs:
        customs.remove(code)

    # Yangilangan holatni saqlaymiz
    await state.update_data(customs=customs)

    # Matn va klaviaturani qayta quramiz
    text, keyboard = await custom_keyboard_sell(customs=customs)

    # Xabarni yangilaymiz
    await query.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await query.answer()

@dp.callback_query(F.data == "send_custom")
async def handle_send_custom(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    customs = data.get("customs", [])

    if not customs:
        await query.answer("Никакой товар не выбран!", show_alert=True)
        return

    counts = Counter(customs)
    total_sum = 0

    text = "<b>Заказ:</b>\n\n"
    for code, count in counts.items():
        name = PRODUCT_NAMES.get(code, code)
        price = PRODUCT_PRICES.get(code, 0)
        total = price * count
        total_sum += total
        text += f"• {name}: {count} x {price} = {total} сум\n"

    text += f"\n<b>💸 Общая сумма:</b> {total_sum} сум"
    text += "\n\n👇 Выберите способ оплаты:"

    await state.set_state(CustomSell.waiting_for_payment)
    await state.update_data(total_sum=total_sum)
    await query.message.edit_text(text, reply_markup=payment_keyboard(), parse_mode="HTML")
    await query.answer()
@dp.callback_query(CustomSell.waiting_for_payment,F.data == "pay_debt")
async def handle_pay_debt(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text("📝 Пожалуйста, укажите, на чьё имя и до какого числа нужно оплатить.\n\nНапример:\n<b>На имя Али ака, до 10 мая</b>", parse_mode="HTML")
    await state.set_state(CustomSell.waiting_for_debt_comment)
    await query.answer()
@dp.message(CustomSell.waiting_for_debt_comment)
async def handle_debt_comment(msg: Message, state: FSMContext):
    comment = msg.text
    payment_type="debt"
    await state.update_data(payment_type=payment_type)
    await state.update_data(debt_comment=comment)

    # optional: customs yoki boshqa ma'lumotlar bilan birga
    await msg.answer(f"✅ Данные о долгах сохранено:\n\n🗒 {comment}\nСпасибо!")
    
    # Bu yerda bazaga yozish yoki adminga yuborish logikasini qo‘shish mumkin
    await state.set_state(CustomSell.waiting_for_comments)
    await msg.answer("Пишите комментария для заказа либо пропустите",reply_markup= await skip_key())
    
@dp.callback_query(CustomSell.waiting_for_payment,F.data == "pay_cash")
async def handle_pay_cash(query: CallbackQuery, state: FSMContext, bot: Bot):
    payment_type="cash"
    await state.update_data(payment_type=payment_type)
    await query.answer()
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.message.answer("Тип оплаты: Наличные")
    await state.set_state(CustomSell.waiting_for_comments)
    await query.message.answer("Пишите комментария для заказа либо пропустите",reply_markup= await skip_key())
    
@dp.callback_query(F.data == "pay_card")
async def handle_pay_card(query: CallbackQuery, state: FSMContext, bot: Bot):
    await query.answer()
    payment_type="card"
    await state.update_data(payment_type=payment_type)
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.message.answer("Тип оплаты: Карта")
    await state.set_state(CustomSell.waiting_for_comments)
    await query.message.answer("Пишите комментария для заказа либо пропустите:",reply_markup= await skip_key())
    
@dp.message(CustomSell.waiting_for_comments)
async def handle_comments_all(msg: Message, state: FSMContext):
    comments = msg.text
    await state.update_data(comments=comments)
    order_data = await state.get_data() 
    total_sum = order_data.get("total_sum", 0)
    debt_comment = order_data.get("debt_comment", "")
    payment_type = order_data.get("payment_type", "")
    customs = order_data.get("customs", [])
    comments = order_data.get("comments", "")
    user_id = msg.from_user.id
    save_order_to_json(customs, total_sum, payment_type, comments,user_id, debt_comment)
    await msg.answer("✅Заказ сохранен",reply_markup=ReplyKeyboardRemove())
    await msg.answer("главная:",reply_markup=await start_keyboard())
@dp.callback_query(F.data == "spending")
async def handle_spending(query: CallbackQuery, state: FSMContext, bot: Bot):
    await query.answer()
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.message.answer("Выберите тип расхода:",reply_markup=await spend_type_keyboard())
    await state.set_state(Spend.waiting_for_spend_type)
@dp.callback_query(Spend.waiting_for_spend_type,F.data =="spend")  
async def handle_spend(query: CallbackQuery, state: FSMContext, bot: Bot):
    await query.answer()
    await state.update_data(spend_type="any_spend")
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.message.answer("Отправьте сумму, которую хотите потратить:")
    await state.set_state(Spend.waiting_for_spend_amount)
@dp.message(Spend.waiting_for_spend_amount)
async def handle_amount(msg: Message, state: FSMContext):
    try:
        if not msg.text.isdigit():
            await msg.answer("долбоеб, введи корректную сумму.")
            return
        if not 0 < float(msg.text) <= 1000000:
            await msg.answer("Долбоеб, введи сумму от 0 до 1000000.")
            return
        amount = float(msg.text)
        await state.update_data(amount=amount)
        await msg.answer("Отправьте комментарий для траты:")
        await state.set_state(Spend.waiting_for_spend_comment)
    except ValueError:
        await msg.answer("Долбоеб, введи корректную сумму.")

@dp.message(Spend.waiting_for_spend_comment)
async def handle_comment_for_spend(msg: Message, state: FSMContext):
    comment = msg.text
    
    await state.update_data(comment=comment)
    data = await state.get_data()
    amount = data.get("amount")
    comment = data.get("comment")
    spend_type=data.get("spend_type")
    try:
        worker= data.get("worker")
    except:
        worker=" "
    user_id = msg.from_user.id
    save_spend_to_json(user_id=user_id, spend_amount=amount, comment=comment, spend_type=spend_type,worker=worker)
    await msg.reply("Сам Такой")
    await msg.answer("✅Трата сохранена",reply_markup=ReplyKeyboardRemove())
    await msg.answer("главная:",reply_markup=await start_keyboard())
@dp.callback_query(F.data == "report")
async def handle_report(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await callback.message.answer("Выберите действие:", reply_markup=await key_reports()) 
@dp.message(admin_filter,F.text == "💰 Расходы")
async def handle_expenses(msg: Message, state: FSMContext):
    await msg.answer("Got it!", reply_markup=ReplyKeyboardRemove())
    await msg.answer("Выберите действие:", reply_markup=await generate_time_period_keyboard("spend"))
    await state.set_state(Spend_report.waiting_for_spend_report)
@dp.message(admin_filter,F.text == "💰 Продажа")
async def handle_sales(msg: Message, state: FSMContext):
    await msg.answer("Got it!", reply_markup=ReplyKeyboardRemove())
    await msg.answer("Выберите действие:", reply_markup=await generate_time_period_keyboard("sell"))
    
    await state.set_state(Order_report.waiting_for_order_report)
@dp.callback_query(Spend.waiting_for_spend_type,F.data== "staff")
async def handle_staff(query: CallbackQuery, state: FSMContext, bot: Bot):
    await query.answer()
    await state.update_data(spend_type="staff")
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.message.answer("Стафф бесплатно выбери че хочешь!")
    
    chat_id = query.from_user.id
    await query.message.answer

    
@dp.callback_query(Spend.waiting_for_spend_type,F.data=="salary")
async def handle_slary(query: CallbackQuery, state: FSMContext, bot: Bot):
    await query.answer()
    await state.update_data(spend_type="salary")
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.message.answer("Выберите действие:",reply_markup=await key_choose_worker())
    await state.set_state(Spend.waiting_for_worker)
@dp.callback_query(Spend.waiting_for_worker)
async def handle_worker(query: CallbackQuery, state: FSMContext, bot: Bot):
    await query.answer()
    await state.update_data(worker=query.data)
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.message.answer("Введите сумму зарплаты:")
    await state.set_state(Spend.waiting_for_spend_amount)
@dp.callback_query(F.data.startswith("report:"))
async def handle_report_callback(callback: CallbackQuery,bot: Bot):
    _, report_type, period = callback.data.split(':')
    
    message, filename = await generate_report(report_type, period)
    
    
    print(f"Fayl nomi: {filename}")
        
    if not filename:
            await callback.message.answer("Faylni yaratishda xatolik yuz berdi.")
            return

        # Faylni to'g'ri formatda yuborish
    document = FSInputFile(filename)
        
    await callback.message.answer_document(
            document=document,
            caption=message,
            parse_mode='HTML',
            reply_markup= ReplyKeyboardRemove()
        )
    os.remove(filename)
@dp.callback_query(F.data == "pay_mixed")
async def handle_pay_mixed(query: CallbackQuery, state: FSMContext, bot: Bot):
    await query.answer()
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.message.answer("Скоро будет доступно")
@dp.callback_query(F.data == "bills")
async def handle_bills(query: CallbackQuery, state: FSMContext, bot: Bot):
    await query.answer()
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.message.answer("Выберите дату:",reply_markup= await generate_date_bills_keyboard())
@dp.callback_query(F.data.startswith("bill:"))  
async def handle_bills(query: CallbackQuery, state: FSMContext, bot: Bot):
    await query.answer()
    await bot.delete_message(query.from_user.id, query.message.message_id)
    data=  load_data(ORDERS)
    
    date= query.data.split(":")[1]
    for i in data:
        if i["date"].split(" ")[0] == date:
            message = show_order_info(i["id"])
            
            await query.message.answer(message,parse_mode="HTML",reply_markup= await generate_editor_order_keyboard(i["id"]))
@dp.callback_query(F.data.startswith("delete_order:")) 
async def handle_delete_order(query: CallbackQuery, state: FSMContext, bot: Bot):
    order_id = int(query.data.split(":")[1])
    print(order_id)
    print(query.data)
    data=  load_data(ORDERS)
    for i in data:
        if int(i["id"]) == order_id:
            message = delete_order(i["id"])
            print(message)
            await query.message.answer(message,parse_mode="HTML")
    await query.answer()
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.message.answer("Выберите действие:", reply_markup=await start_keyboard())
    
@dp.callback_query(F.data=="spends")
async def handle_spends(query: CallbackQuery, state: FSMContext, bot: Bot):
    await query.answer()
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.message.answer("Выберите действие:", reply_markup=await generate_date_spends_keyboard())
@dp.callback_query(F.data.startswith("spends:"))
async def handle_spends(query: CallbackQuery, state: FSMContext, bot: Bot):
    await query.answer()
    await bot.delete_message(query.from_user.id, query.message.message_id)
    data=  load_data(SPENDING)
    date= query.data.split(":")[1]
    for i in data:
        if i["date"].split(" ")[0] == date:
            message = show_spend_info(i["id"])

            await query.message.answer(message,parse_mode="HTML",reply_markup= await generate_editor_spend_keyboard(i["id"]))
            
    
@dp.callback_query(F.data.startswith("delete_spend:"))
async def handle_delete_spend(query: CallbackQuery, state: FSMContext, bot: Bot):
    spend_id = int(query.data.split(":")[1])
    print(spend_id)
    print(query.data)
    data=load_data(SPENDING)
    for i in data:
        if int(i["id"]) == spend_id:
            message = delete_spend(i["id"])
            print(message)
            await query.message.answer(message,parse_mode="HTML")
    await query.answer()
    
    await query.message.answer("Выберите действие:", reply_markup=await start_keyboard())
    
    

        

async def main():
        logging.basicConfig(level=logging.INFO)
        await dp.start_polling(bot)
    # Start the bot
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
    
    
    