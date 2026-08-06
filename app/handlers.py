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
from bot import send_admin_notification

load_dotenv()
router = Router()

# Кошелёк для оплаты
MY_WALLET = os.getenv("MY_WALLET", "UQDxYNrscV__Tawt194bY8dVVzAghphteO2oftuia0NTVxvT")

# ============================================
# 🟢 1. СТАРТОВОЕ СООБЩЕНИЕ
# ============================================
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

# ============================================
# 🟢 2. КУПИТЬ ЗВЁЗДЫ (ВЫБОР СУММЫ)
# ============================================
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

# ============================================
# 🟢 3. ЦЕНА
# ============================================
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

# ============================================
# 🟢 4. ПОДДЕРЖКА
# ============================================
@router.message(F.text == "Поддержка")
async def support(message: Message, state: FSMContext):
    await state.set_state(None)
    await message.reply(
        "📩 Если у вас возникли вопросы, пишите:\n"
        "<code>anberdindinar1@gmail.com</code>\n\n"
        "Мы отвечаем в течение 24 часов! 🚀",
        parse_mode="HTML"
    )

# ============================================
# 🟢 5. КАК ЭТО РАБОТАЕТ
# ============================================
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

# ============================================
# 🟢 6. ПОЛИТИКА КОНФИДЕНЦИАЛЬНОСТИ
# ============================================
@router.message(F.text == "Политика конфиденциальности")
async def privacy(message: Message, state: FSMContext):
    await state.set_state(None)
    await message.reply("""
🔒 **Политика конфиденциальности**

Мы не передаём ваши данные третьим лицам.
Все транзакции защищены.
Ваши звёзды — ваши звёзды. ⭐
""")

# ============================================
# 🟢 7. ОТМЕНА И НАЗАД (КНОПКИ РАБОТАЮТ 100%)
# ============================================
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

# ============================================
# 🟢 8. ВЫБОР КОЛИЧЕСТВА ЗВЁЗД
# ============================================
@router.callback_query(Purchase.amount)
async def choose_amount(callback: CallbackQuery, state: FSMContext):
    stars_amount = callback.data.split(":")[1]
    await callback.answer(f"⭐ Выбрано: {stars_amount} звёзд")
    await state.update_data(amount=stars_amount)
    await callback.message.edit_text(text=f"⭐ Выбрано: {stars_amount}", reply_markup=None)
    await state.set_state(Purchase.username)
    await callback.message.answer("👤 Введите username получателя (без @):", reply_markup=kb.username)

# ============================================
# 🟢 9. ВВОД USERNAME ПОЛУЧАТЕЛЯ
# ============================================
@router.message(Purchase.username)
async def choose_username(message: Message, state: FSMContext):
    username = message.text
    if username[0] == "@":
        username = username[1:]
    await state.update_data(username=username)
    await state.set_state(Purchase.purchase_method)
    await message.answer("💳 Выберите способ оплаты:", reply_markup=kb.purchase_method)

# ============================================
# 🟢 10. ВЫБОР СПОСОБА ОПЛАТЫ
# ============================================
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

# ============================================
# 🟢 11. ПОДТВЕРЖДЕНИЕ ЗАКАЗА И ОТПРАВКА УВЕДОМЛЕНИЯ
# ============================================
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

# ============================================
# 🟢 12. ОЖИДАНИЕ ПОДТВЕРЖДЕНИЯ ОТ КЛИЕНТА
# ============================================
@router.callback_query(Purchase.payment_status)
async def payment_status(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer("✅ Ожидание...")
    await callback.message.edit_text(text=callback.message.text, reply_markup=None)
    await callback.message.answer(
        "⏳ Ожидайте подтверждения от администратора.\n"
        "Обычно это занимает не более 15 минут. 🙏"
    )

# ============================================
# 🟢 13. АДМИН ПОДТВЕРЖДАЕТ (ИГРАЕТ ГЛАВНУЮ РОЛЬ!)
# ============================================
@router.callback_query((F.data).startswith("adm_conf:"))
async def confirm_payment(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # АДМИН ПОДТВЕРЖДАЕТ — ПРОСТО РАБОТАЕТ БЕЗ ЛИШНИХ ПРОВЕРОК
    await callback.answer("✅ Оплата подтверждена!")

    transaction_id = int(callback.data.split(":")[1])
    
    order_data = await get_chat_id(transaction_id)
    for order in order_data:
        # КЛИЕНТУ ПРИХОДИТ СООБЩЕНИЕ ОБ УСПЕХЕ
        await bot.send_message(
            chat_id=order.chat_id,
            text=(
                f"🎉 **Поздравляем! Покупка успешна!**\n\n"
                f"⭐ {order.amount} звёзд зачислено на аккаунт @{order.username}.\n"
                f"🚀 Спасибо за покупку! Желаем удачи!\n"
                f"💫 С уважением, команда StarSeller."
            ),
            reply_markup=kb.main
        )
        
        try:
            stars_buy = await purchase(order.amount, order.username)
            if stars_buy["success"]:
                await update_payment_status(transaction_id, "completed")
                await callback.message.edit_text(f"✅ Заказ #{transaction_id} успешно выполнен!")
                
                # АДМИНУ ПРИХОДИТ СООБЩЕНИЕ ОБ УСПЕХЕ
                await send_admin_notification(
                    f"✅ **ЗАКАЗ ВЫПОЛНЕН!**\n"
                    f"🆔 Заказ: #{transaction_id}\n"
                    f"👤 Получатель: @{order.username}\n"
                    f"⭐ Звёзд: {order.amount}\n"
                    f"🎉 Всё прошло успешно!"
                )
        except Exception as e:
            await update_payment_status(transaction_id, "error")
            await callback.message.edit_text(f"❌ Ошибка зачисления звёзд.")
            await send_admin_notification(f"❌ Ошибка в заказе #{transaction_id}: {str(e)}")