from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import (Message, CallbackQuery, ReplyKeyboardRemove,
                           InlineKeyboardMarkup, InlineKeyboardButton)
import app.keyboards as kb
from app.states import Purchase
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import os
from app.get_exchangerate import get_exchangerate
import app.database.db_requests as rq
from app.fragment_api.stars_purchse import purchase

load_dotenv()
router = Router()

# Твой кошелек USDT (TON)
MY_WALLET = "UQDxYNrscV__Tawt194bY8dVVzAghphteO2oftuia0NTVxvT"

@router.message(CommandStart())
async def send_welcome(message: Message, state: FSMContext):
    await state.set_state(None)
    await state.set_state("chat_id")
    await message.reply("Приветствуем в StarSeller 👋 \n\nХотите купить немного звёзд?)", reply_markup=kb.main)


@router.message(F.text == "Купить звёзд ⭐")
async def buy_stars(message: Message, state: FSMContext):
    await state.update_data(chat_id=message.chat.id)
    await message.answer(
        ".",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Purchase.amount)
    await message.reply("Выберите сумму которую вы хотите приобрести:", reply_markup=kb.buy_stars)


@router.message(F.text == "Цена💲")
async def price(message: Message, state: FSMContext):
    await state.set_state(None)
    await message.reply("Цена за одну звезду 🌟 составляет <b>1.5 рубля</b> (или примерно 0.016 USDT)."
                        "\n\nПри оформлении заказа сумма пересчитывается в USDT по актуальному курсу. 📈",
                        parse_mode="HTML")


@router.message(F.text == "Поддержка")
async def support(message: Message, state: FSMContext):
    await state.set_state(None)
    await message.reply(
        "📩 Для получения поддержки или ответов на ваши вопросы напишите нам на email:\n"
        "<code>anberdindinar1@gmail.com</code>\n\n"
        "Скопируйте адрес и отправьте нам письмо. Мы ответим в течение 24 часов! 🚀",
        parse_mode="HTML"
    )


@router.message(F.text == "Как это работает?🛠️")
async def how_it_works(message: Message, state: FSMContext):
    await state.set_state(None)
    await message.reply(""" 
                        Как это работает?

            \n\nВсё очень просто и быстро! Вот как происходит процесс покупки звёзд:
            
            \n\n1.  <b>Выбор звёзд.</b> Ты выбираешь, сколько звёзд хочешь купить. ✨
            \n2.  <b>Получатель.</b> Указываешь username в Telegram того, кому нужно отправить звёзды.
            \n3.  <b>Оплата.</b> Переводишь нужную сумму в USDT на наш кошелек. 💰
            \n4.  <b>Подтверждение.</b> После оплаты ты нажимаешь "Оплатил ✅", админ проверяет транзакцию. 
            \n5.  <b>Зачисление.</b> После проверки звёзды мгновенно зачисляются на указанный тобой аккаунт! ✅
                
                        """,
                        parse_mode="HTML")


@router.message(F.text == "Политика конфиденциальности")
async def privacy(message: Message, state: FSMContext):
    await state.set_state(None)
    await message.reply(""" 
<b>Политика конфиденциальности бота Starseller</b>

\n
<b>1. Общие положения</b>

\n
Эта Политика конфиденциальности регулирует обработку персональных данных пользователей бота Starseller в
 Telegram (далее — «Бот»). Мы уважаем право на конфиденциальность и обязуемся защищать ваши данные.

\n
<b>2. Какие данные мы собираем?</b>

\n
Мы собираем только те данные, которые необходимы для выполнения ваших заказов и обеспечения работы Бота:

    <b>Telegram ID:</b> Уникальный идентификатор, который позволяет нам связываться с вами.
    <b>Имя пользователя в Telegram:</b> Используется для удобства общения и идентификации.
    <b>Данные о транзакциях:</b> Информация о платежах для подтверждения оплаты и зачисления звёзд.
     Мы не храним полные платёжные реквизиты.


\n
<b>3. Как мы используем ваши данные?</b>

\n
Ваши данные используются исключительно для следующих целей:

    <b>Обработка и выполнение заказов:</b> Передача звёзд на указанный вами аккаунт в Telegram.
    <b>Связь с вами:</b> Уведомления о статусе заказа, ответы на ваши вопросы.
    <b>Улучшение качества обслуживания:</b> Анализ общей статистики для оптимизации работы Бота.


\n
<b>4. Как мы защищаем ваши данные?</b>

\n
Мы принимаем все разумные и необходимые меры для защиты ваших данных от несанкционированного доступа,
изменения, раскрытия или уничтожения. Все данные хранятся на защищенных серверах.

\n
<b>5. Кому мы можем передавать ваши данные?</b>

\n
Мы не передаём ваши персональные данные третьим лицам, за исключением случаев, когда это необходимо
для выполнения заказа (например, для взаимодействия с платёжными системами) или по требованию законодательства.

\n
<b>6. Сроки хранения данных</b>

\n
Мы храним ваши данные ровно столько, сколько это необходимо для выполнения наших обязательств
и соблюдения требований законодательства. После этого данные удаляются.

\n
<b>7. Ваши права</b>

\n
Вы имеете право в любой момент:

Запросить доступ к своим данным.
Потребовать исправления неточных данных.
Попросить удалить свои данные (при условии, что это не противоречит нашим юридическим обязательствам).


\n
<b>8. Согласие с политикой</b>

\n
Используя наш Бот, вы автоматически соглашаетесь с условиями этой Политики конфиденциальности.
Если вы не согласны с какими-либо её положениями, пожалуйста, не используйте наш сервис.
                         """,
                        parse_mode="HTML")


@router.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Отмена транзакции")
    await state.set_state(None)
    await callback.message.edit_text(
        text=f"Отмена ❌",
        reply_markup=None
    )
    await callback.message.answer("Выберите что нибудь:", reply_markup=kb.main)


@router.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Purchase.username:
        await state.set_state(Purchase.amount)
        await callback.message.edit_text("Выберите сумму которую вы хотите приобрести:", reply_markup=kb.buy_stars)
    elif current_state == Purchase.purchase_method:
        await state.set_state(Purchase.username)
        await callback.message.edit_text("Пожалуйста введите username получателя:", reply_markup=kb.username)


@router.callback_query(Purchase.amount)
async def choose_amount(callback: CallbackQuery, state: FSMContext):
    stars_amount = callback.data.split(":")[1]
    await callback.answer(f"Вы выбрали: {stars_amount} звёзд")
    await state.update_data(amount=stars_amount)
    await callback.message.edit_text(
        text=f"Вы выбрали {stars_amount} ⭐",
        reply_markup=None
    )
    await state.set_state(Purchase.username)
    await callback.message.answer("Пожалуйста введите username получателя:", reply_markup=kb.username)


@router.message(Purchase.username)
async def choose_username(message: Message, state: FSMContext):
    username = message.text
    if username[0] == "@":
        username = username[1:]
    await state.update_data(username=username)
    await state.set_state(Purchase.purchase_method)
    await message.answer("Выберите способ оплаты:", reply_markup=kb.purchase_method)


@router.callback_query(Purchase.purchase_method)
async def choose_purchase(callback: CallbackQuery, state: FSMContext):
    await state.update_data(purchase_method=callback.data)
    await callback.answer(f"Вы выбрали: {callback.data}")
    await state.set_state(Purchase.accepted)
    data = await state.get_data()
    await callback.message.edit_text(
        text=f"Вы выбрали {callback.data}",
        reply_markup=None
    )
    await callback.message.answer(f"       Ваш заказ: \n\n {data['amount']} ⭐\n\n Получатель: @{data['username']}\n\n"
                                  f"Способ Оплаты: {data['purchase_method']}", reply_markup=kb.accept_or_deny)


@router.callback_query(Purchase.accepted)
async def choose_status(callback: CallbackQuery, state: FSMContext):
    await state.update_data(accepted="True")
    data = await state.get_data()
    
    # Цена за 1 звезду = 1.5 рубля. Переводим в USDT примерно
    # Для простоты используем фиксированный курс 1 USDT = 90 руб (измени, если нужно)
    usdt_rate = 90.0
    total_rub = float(data['amount']) * 1.5
    total_usdt = round(total_rub / usdt_rate, 2)
    
    await callback.answer("Нажав эту кнопку вы подтверждаете что все введённые вами данные верны", show_alert=True)
    await callback.message.edit_text(
        text=callback.message.text,
        reply_markup=None
    )
    await state.set_state(Purchase.payment_status)
    new_order = await rq.set_order(data["chat_id"], data["username"], data["amount"], data["purchase_method"],
                                   data["accepted"], "pending")
    
    # Так как убрали CryptoCloud, просто выдаем кошелек
    if data["purchase_method"] == "USDT":
        await callback.message.answer(
            f"💳 <b>Для оплаты переведите {total_usdt} USDT на кошелек:</b>\n\n"
            f"<code>{MY_WALLET}</code>\n\n"
            f"📝 <b>В комментарии к переводу укажите Ваш ID транзакции:</b>\n"
            f"<code>{new_order.id}</code>\n\n"
            f"⚠️ После перевода нажмите кнопку «Оплатил ✅».",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Оплатил ✅", callback_data=str(new_order.id))],
                [InlineKeyboardButton(text="Отмена ❌", callback_data="cancel")]
            ])
        )


@router.callback_query(Purchase.payment_status)
async def payment_status(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer("Вы подтвердили оплату ✅")
    await callback.message.edit_text(
        text=callback.message.text,
        reply_markup=None
    )
    await callback.message.answer(
        "Вы подтвердили оплату ✅, ожидайте её подтверждения с нашей стороны это займёт около 15 минут")
    await bot.send_message(
        chat_id=os.getenv("ADMIN_ID"),
        text=f"❗️ **Нужно проверить оплату от {callback.data}**",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить оплату пользователя ✅", callback_data="adm_conf:" + callback.data)],
            [InlineKeyboardButton(text="Отмена ❌", callback_data="cancel")]

        ])
    )


@router.callback_query((F.data).startswith("adm_conf:"))
async def confirm_payment(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if callback.from_user.id != int(os.getenv("ADMIN_ID")):
        await callback.answer("У вас нет прав для этого действия.")
        return
    await callback.answer("Вы подтвердили платёж")
    transaction_id = int(callback.data.split(":")[1])
    order_data = await rq.get_chat_id(transaction_id)
    for order in order_data:
        await bot.send_message(
            chat_id=order.chat_id,
            text=f"🎉 Ваш платеж на {order.amount} ⭐ подтвержден! Звезды будут зачислены в скором времени.",
            reply_markup=kb.main
        )
        stars_buy = await purchase(order.amount, order.username)
        try:
            if stars_buy["success"]:
                await rq.update_payment_status(transaction_id, "completed")
                await callback.message.edit_text(f"✅ Платеж #{transaction_id} подтвержден", reply_markup=None)
        except Exception as e:
            await callback.message.edit_text(f"В Платеже #{transaction_id} возникла ошибка❗❗❗", reply_markup=None)
            await rq.update_payment_status(transaction_id, "error")