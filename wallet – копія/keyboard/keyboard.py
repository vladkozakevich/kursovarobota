from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_keyboard() -> InlineKeyboardMarkup:
    # головна клавіатура
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Баланс", callback_data='main_balance')],
        [InlineKeyboardButton("Виртати", callback_data='main_costs')],
        [InlineKeyboardButton("Статистика", callback_data='main_static')],
        [InlineKeyboardButton("Карта", callback_data='main_card')]]
    )
    return markup


def balance(top_up_available: bool = False) -> InlineKeyboardMarkup:
    # клавіатури для витрат
    if top_up_available:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("Поповнити", callback_data='add_money'),
             InlineKeyboardButton("Конвертувати", callback_data='add_konvert')],
            [InlineKeyboardButton("Назад", callback_data='add_back')]
        ])
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("Конвертувати", callback_data='add_konvert')],
            [InlineKeyboardButton("Назад", callback_data='add_back')]
        ])
    return markup


def back() -> InlineKeyboardMarkup:
    # клавіатура для повернення назад
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data='fsm_back')]]
    )
    return markup


def back_conv() -> InlineKeyboardMarkup:
    # клавіатура для повернення назад
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data='add_back_b')]]
    )
    return markup


def costs_menu(top_up_available: bool = False) -> InlineKeyboardMarkup:
    # клавіатура для історії
    if not top_up_available:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("Добавити", callback_data="costs_add")],
            [InlineKeyboardButton("Історія", callback_data="costs_history")],
            [InlineKeyboardButton("Назад", callback_data='back')]]
        )
        return markup
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("Історія", callback_data="costs_history")],
            [InlineKeyboardButton("Назад", callback_data='back')]]
        )
        return markup


def costs_back() -> InlineKeyboardMarkup:
    # клавіатура для повернення назад з фсм машини стану
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data='costs_back')]]
    )
    return markup


def all_logg() -> InlineKeyboardMarkup:
    # клавіатура для повернення назад
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data='costs_back')]]
    )
    return markup


def statistick() -> InlineKeyboardMarkup:
    # клавіатура для статистики
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Витрати", callback_data='statistick_minuse'),
         InlineKeyboardButton("Поповнення", callback_data='statistick_add')],
        [InlineKeyboardButton("назад", callback_data='statistick_back_main')]]
    )
    return markup


def stat_back() -> InlineKeyboardMarkup:
    # клавіатура для повернення назад з фсм машини стану
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Повернутися назад", callback_data='statistick_back')]]
    )
    return markup


def card_menu() -> InlineKeyboardMarkup:
    # клавіатура для отрмання токену
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Отримати токен',url='https://api.monobank.ua')],
        [InlineKeyboardButton("Підключити карту", callback_data='card_insert')],
        [InlineKeyboardButton("Назад", callback_data='back')]
    ])
    return markup


def back_in_main_card(data, data2) -> InlineKeyboardMarkup:
    # клавіатура для прийняття токену
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(f"{data}", callback_data=f'card_{data2}')],
        [InlineKeyboardButton("В головне меню", callback_data='back')]
    ])
    return markup