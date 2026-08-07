from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import (Message, CallbackQuery, ReplyKeyboardRemove,
                           InlineKeyboardMarkup, InlineKeyboardButton)
import app.keyboards as kb
from app.states import Purchase
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import os
from app.database.db_requests import set_order, get_chat_id, update_payment_status
from app.fragment_api.stars_purchse import purchase
from notify import send_admin_notification

load_dotenv()
router = Router()

MY_WALLET = os.getenv("MY_WALLET", "UQDxYNrscV__Tawt194bY8dVVzAghphteO2oftuia0NTVxvT")

# ==========================================================
# БЛОК 1: ГЛАВНОЕ МЕНЮ И СТАРТ
# ==========================================================
@router.message(CommandStart())
async def send_welcome(message: Message, state: FSMContext):
    await state.set_state(None)
    await state.set_state("chat_id")
    await message.reply(
        "🌟 Приветствуем в StarSeller!\n\n"
        "Мы продаём звёзды Telegram по самой низкой цене.\n"
        "Нажми «Купить звёзд ⭐», чтобы начать! 🚀",
        reply_markup=kb.main
    )

@router.message(F.text == "Купить звёзд ⭐")
async def buy_stars(message: Message, state: FSMContext):
    await state.update_data(chat_id=message.chat.id)
    await message.answer(".", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Purchase.amount)
    await message.reply(
        "⭐ Выберите количество звёзд:\n\n"
        "50 звезд — отличный старт!\n"
        "100 звезд — для друзей!\n"
        "500 звезд — для больших подарков!",
        reply_markup=kb.buy_stars
    )

@router.message(F.text == "Цена💲")
async def price(message: Message, state: FSMContext):
    await state.set_state(None)
    price_rub = float(os.getenv("PRICE_PER_STAR_RUB", "1.5"))
    usdt_rate = float(os.getenv("USDT_RATE_RUB", "81.5"))
    price_usdt = round(price_rub / usdt_rate, 4)
    await message.reply(
        f"💰 Цена за одну звезду 🌟:\n"
        f"→ <b>{price_rub} рубля</b>\n"
        f"→ ≈ {price_usdt} USDT\n\n"
        f"При оформлении заказа сумма пересчитывается в USDT.\n"
        f"Курс обновляется автоматически! 📈",
        parse_mode="HTML"
    )

@router.message(F.text == "Поддержка")
async def support(message: Message, state: FSMContext):
    await state.set_state(None)
    await message.reply(
        "📩 Если у вас возникли вопросы, пишите:\n"
        "<code>anberdindinar1@gmail.com</code>\n\n"
        "Мы отвечаем в течение 24 часов! 🚀",
        parse_mode="HTML"
    )

@router.message(F.text == "Как это работает?🛠️")
async def how_it_works(message: Message, state: FSMContext):
    await state.set_state(None)
    await message.reply("""
🛠️ **Как это работает?**

1️⃣ Нажми «Купить звёзд ⭐»
2️⃣ Выбери количество звёзд
3️⃣ Введи username получателя
4️⃣ Оплати USDT на наш кошелёк
5️⃣ Нажми «Оплатил ✅»

После проверки звёзды зачисляются мгновенно! ✨
""")

@router.message(F.text == "Политика конфиденциальности")
async def privacy(message: Message, state: FSMContext):
    await state.set_state(None)
    await message.reply("""
🔒 **Политика конфиденциальности**

Мы не передаём ваши данные третьим лицам.
Все транзакции защищены.
Ваши звёзды — ваши звёзды. ⭐
""")

# ==========================================================
# БЛОК 2: ОТМЕНА И НАЗАД
# ==========================================================
@router.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer("❌ Отменено")
    await state.set_state(None)
    await callback.message.edit_text(text="❌ Действие отменено.", reply_markup=None)
    await callback.message.answer("✨ Возвращаемся в главное меню:", reply_markup=kb.main)

@router.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Purchase.username:
        await state.set_state(Purchase.amount)
        await callback.message.edit_text("⭐ Выберите количество звёзд:", reply_markup=kb.buy_stars)
    elif current_state == Purchase.purchase_method:
        await state.set_state(Purchase.username)
        await callback.message.edit_text("👤 Введите username получателя (без @):", reply_markup=kb.username)

# ==========================================================
# БЛОК 3: ВЫБОР ЗВЁЗД И ОПЛАТА
# ==========================================================
@router.callback_query(Purchase.amount)
async def choose_amount(callback: CallbackQuery, state: FSMContext):
    stars_amount = callback.data.split(":")[1]
    await callback.answer(f"⭐ Выбрано: {stars_amount} звёзд")
    await state.update_data(amount=stars_amount)
    await callback.message.edit_text(text=f"⭐ Выбрано: {stars_amount}", reply_markup=None)
    await state.set_state(Purchase.username)
    await callback.message.answer("👤 Введите username получателя (без @):", reply_markup=kb.username)

@router.message(Purchase.username)
async def choose_username(message: Message, state: FSMContext):
    username = message.text
    if username[0] == "@":
        username = username[1:]
    await state.update_data(username=username)
    await state.set_state(Purchase.purchase_method)
    await message.answer("💳 Выберите способ оплаты:", reply_markup=kb.purchase_method)

@router.callback_query(Purchase.purchase_method)
async def choose_purchase(callback: CallbackQuery, state: FSMContext):
    await state.update_data(purchase_method=callback.data)
    await callback.answer(f"💳 Оплата: {callback.data}")
    await state.set_state(Purchase.accepted)
    data = await state.get_data()
    await callback.message.edit_text(text=f"💳 Оплата: {callback.data}", reply_markup=None)
    await callback.message.answer(
        f"📦 **Ваш заказ:**\n\n"
        f"⭐ Звёзд: {data['amount']}\n"
        f"👤 Получатель: @{data['username']}\n"
        f"💳 Оплата: {data['purchase_method']}\n\n"
        f"Подтвердите, что всё верно:",
        reply_markup=kb.accept_or_deny
    )

@router.callback_query(Purchase.accepted)
async def choose_status(callback: CallbackQuery, state: FSMContext):
    await state.update_data(accepted="True")
    data = await state.get_data()
    
    price_per_star_rub = float(os.getenv("PRICE_PER_STAR_RUB", "1.5"))
    usdt_rate = float(os.getenv("USDT_RATE_RUB", "81.5"))
    total_rub = float(data['amount']) * price_per_star_rub
    total_usdt = round(total_rub / usdt_rate, 2)
    
    await callback.answer("✅ Данные подтверждены!", show_alert=True)
    await callback.message.edit_text(text=callback.message.text, reply_markup=None)
    await state.set_state(Purchase.payment_status)
    
    new_order = await set_order(data["chat_id"], data["username"], data["amount"], data["purchase_method"],
                               data["accepted"], "pending")
    
    if data["purchase_method"] == "USDT":
        await callback.message.answer(
            f"💳 **Инструкция по оплате**\n\n"
            f"💰 Сумма к оплате: {total_usdt} USDT\n"
            f"💳 Кошелёк: <code>{MY_WALLET}</code>\n"
            f"📝 ID заказа: <code>{new_order.id}</code>\n\n"
            f"✅ Переведите USDT на кошелёк.\n"
            f"✅ В комментарии укажите ID заказа.\n"
            f"✅ После перевода нажмите «Оплатил ✅».",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Оплатил", callback_data=str(new_order.id))],
                [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
            ])
        )
        
        # ОТПРАВКА АДМИНУ (КНОПКИ ПОЯВЯТСЯ ЗДЕСЬ)
        admin_text = (
            f"🛒 **НОВЫЙ ЗАКАЗ!**\n"
            f"⭐ Количество: {data['amount']}\n"
            f"👤 Получатель: @{data['username']}\n"
            f"💰 Сумма: {total_usdt} USDT\n"
            f"🆔 Заказ: {new_order.id}"
        )
        admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Подтвердить оплату", callback_data=f"adm_conf:{new_order.id}"),
                InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
            ]
        ])
        await send_admin_notification(admin_text, reply_markup=admin_keyboard)

# ==========================================================
# БЛОК 4: ОЖИДАНИЕ ПОДТВЕРЖДЕНИЯ ОТ КЛИЕНТА
# ==========================================================
@router.callback_query(Purchase.payment_status)
async def payment_status(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer("✅ Ожидание...")
    await callback.message.edit_text(text=callback.message.text, reply_markup=None)
    await callback.message.answer(
        "⏳ Ожидайте подтверждения от администратора.\n"
        "Обычно это занимает не более 15 минут. 🙏"
    )

# ==========================================================
# БЛОК 5: АДМИН ПОДТВЕРЖДАЕТ (И ДЛЯ БОТА, И ДЛЯ САЙТА)
# ==========================================================
@router.callback_query((F.data).startswith("adm_conf:"))
async def confirm_payment(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # Сразу отвечаем на нажатие (чтобы кнопка не зависала)
    await callback.answer("✅ Подтверждено!", show_alert=False)
    
    # Достаём ID заказа
    try:
        transaction_id = int(callback.data.split(":")[1])
    except:
        await callback.message.edit_text("❌ Ошибка ID заказа.")
        return

    # Получаем данные заказа
    order_data = await get_chat_id(transaction_id)
    if not order_data:
        await callback.message.edit_text("❌ Заказ не найден в базе.")
        return

    for order in order_data:
        # 1. Пишем клиенту сообщение об успехе (это сообщение увидит клиент)
        await bot.send_message(
            chat_id=order.chat_id,
            text=(
                f"🎉 **Ваш заказ подтверждён!**\n\n"
                f"⭐ Количество: {order.amount} звёзд\n"
                f"👤 Получатель: @{order.username}\n\n"
                f"🚀 Спасибо за покупку! Мы передаём ваш заказ в обработку.\n"
                f"💫 Звёзды будут зачислены вручную в ближайшее время."
            ),
            reply_markup=kb.main
        )
        
        # 2. Обновляем статус заказа в базе
        await update_payment_status(transaction_id, "completed")
        
        # 3. Пишем админу (вам) инструкцию для ручной выдачи
        await send_admin_notification(
            f"🎯 **РУЧНАЯ ВЫДАЧА ЗВЁЗД**\n"
            f"🆔 Заказ: #{transaction_id}\n"
            f"👤 Клиент: @{order.username}\n"
            f"⭐ Звёзд: {order.amount}\n\n"
            f"📌 Перейдите в @Fragment, купите {order.amount} звёзд и отправьте получателю @{order.username}."
        )
        
        # 4. Сообщаем админу об успехе и скрываем кнопки
        await callback.message.edit_text(
            f"✅ Заказ #{transaction_id} обработан!\n\n"
            f"📌 Не забудьте выдать звёзды вручную через @Fragment.",
            reply_markup=None
        )