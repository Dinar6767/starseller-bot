from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Купить звёзд ⭐")],
                                     [KeyboardButton(text="Цена💲")],
                                     [KeyboardButton(text="Как это работает?🛠️")],
                                     [KeyboardButton(text="Политика конфиденциальности"),
                                      KeyboardButton(text="Поддержка")]
                                     ], resize_keyboard=True)

buy_stars = InlineKeyboardMarkup(inline_keyboard=[

    [
        InlineKeyboardButton(text="50 ⭐", callback_data="buy_stars:50"),
        InlineKeyboardButton(text="75 ⭐", callback_data="buy_stars:75")
    ],
    [
        InlineKeyboardButton(text="100 ⭐", callback_data="buy_stars:100"),
        InlineKeyboardButton(text="150 ⭐", callback_data="buy_stars:150")
    ],
    [
        InlineKeyboardButton(text="250 ⭐", callback_data="buy_stars:250"),
        InlineKeyboardButton(text="350 ⭐", callback_data="buy_stars:350")
    ],
    [
        InlineKeyboardButton(text="500 ⭐", callback_data="buy_stars:500"),
        InlineKeyboardButton(text="750 ⭐", callback_data="buy_stars:750")
    ],
    [
        InlineKeyboardButton(text="1,000 ⭐", callback_data="buy_stars:1000"),
        InlineKeyboardButton(text="1,500 ⭐", callback_data="buy_stars:1500")
    ],
    [InlineKeyboardButton(text="Отмена ❌", callback_data="cancel")]

])

# Здесь только USDT
purchase_method = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Оплата криптой (USDT)", callback_data="USDT")],
    [InlineKeyboardButton(text="Отмена ❌", callback_data="cancel")]
])

username = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отмена ❌", callback_data="cancel")]
])

accept_or_deny = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Всё верно! ✅", callback_data="True")],
    [InlineKeyboardButton(text="Отмена ❌", callback_data="cancel")]
])

admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Подтвердить оплату пользователя ✅", callback_data="confirm_payment")],
    [InlineKeyboardButton(text="Отмена ❌", callback_data="cancel")]
])