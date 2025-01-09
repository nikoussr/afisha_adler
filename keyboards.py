from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton

import configs


def create_reply_keyboard():
    # Создаем кнопки
    button1 = KeyboardButton(text='✅ Афиша в Адлере')
    button2 = KeyboardButton(text='❌ Афиша не в Адлере')
    button3 = KeyboardButton(text='👉 Правила канала')

    # Создаем разметку клавиатуры
    keyboard = ReplyKeyboardMarkup(keyboard=[[button1], [button2], [button3]], resize_keyboard=True,
                                   one_time_keyboard=True)

    # Добавляем кнопки в два ряда

    return keyboard


def create_inline_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Название * ", callback_data="field_name"),
         InlineKeyboardButton(text="Дата/время *", callback_data="field_date"),
         InlineKeyboardButton(text="Описание *", callback_data="field_description")],

        [InlineKeyboardButton(text="Адрес *", callback_data="field_address"),
         InlineKeyboardButton(text="Цена", callback_data="field_price"),
         InlineKeyboardButton(text="Контакты *", callback_data="field_contacts")],

        [InlineKeyboardButton(text="Примечание", callback_data="field_note"),
         InlineKeyboardButton(text="Фото/видео", callback_data="field_photo")],
        [InlineKeyboardButton(text="Посмотреть", callback_data="view"),
         InlineKeyboardButton(text="Отменить", callback_data="cancel")
         ]])
    return keyboard


def create_new_keyboard(data):
    if data['name'] != None and data[
        'date'] != None and data['adress'] != None and data['description'] and data['contacts'] != None:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=(" ✅" if data['name'] else "") + "Название *", callback_data="field_name"),
             InlineKeyboardButton(text=(" ✅" if data['date'] else "") + "Дата\время *", callback_data="field_date"),
             InlineKeyboardButton(text=(" ✅" if data['description'] else "") + "Описание *",
                                  callback_data="field_description")],

            [InlineKeyboardButton(text=(" ✅" if data['adress'] else "") + "Адрес *", callback_data="field_address"),
             InlineKeyboardButton(text=(" ✅" if data['price'] else "") + "Цена", callback_data="field_price"),
             InlineKeyboardButton(text=(" ✅" if data['contacts'] else "") + "Контакты *",
                                  callback_data="field_contacts")],

            [InlineKeyboardButton(text=(" ✅" if data['note'] else "") + "Примечание", callback_data="field_note"),
             InlineKeyboardButton(text=(" ✅" if data['photo'] else "") + "Фото/видео", callback_data="field_photo")],

            [InlineKeyboardButton(text="Посмотреть", callback_data="view"),
             InlineKeyboardButton(text="Отправить", callback_data="send"),
             InlineKeyboardButton(text="Отменить", callback_data="cancel")
             ]])
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=(" ✅" if data['name'] else "") + "Название *", callback_data="field_name"),
             InlineKeyboardButton(text=(" ✅" if data['date'] else "") + "Дата\время *", callback_data="field_date"),
             InlineKeyboardButton(text=(" ✅" if data['description'] else "") + "Описание *",
                                  callback_data="field_description")],

            [InlineKeyboardButton(text=(" ✅" if data['adress'] else "") + "Адрес *", callback_data="field_address"),
             InlineKeyboardButton(text=(" ✅" if data['price'] else "") + "Цена", callback_data="field_price"),
             InlineKeyboardButton(text=(" ✅" if data['contacts'] else "") + "Контакты *",
                                  callback_data="field_contacts")],

            [InlineKeyboardButton(text=(" ✅" if data['note'] else "") + "Примечание", callback_data="field_note"),
             InlineKeyboardButton(text=(" ✅" if data['photo'] else "") + "Фото/видео", callback_data="field_photo")],

            [InlineKeyboardButton(text="Посмотреть", callback_data="view"),
             InlineKeyboardButton(text="Отменить", callback_data="cancel")
             ]])
    return keyboard

back_btn = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="back")]])
back_btn1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="back")]])
back_btn2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="back_to_menu")]])


yes_no_btn = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Да, сбросить", callback_data="clear"), InlineKeyboardButton(text="Вернуться к редактированию", callback_data="gotored")]])