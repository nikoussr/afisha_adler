import asyncio

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaVideo

import configs
import keyboards
from states import States
from main import bot

router = Router()
timer_active = False
remaining_time = 86400  # 3 минуты в секундах


@router.message(Command('start'))
async def command_start(message: Message, state: FSMContext):
    await message.answer(
        f"Привет 👋"
        f"\n\nЯ чат-бот помощник канала <b>АФИША•АДЛЕР💬</b>.\nА так же я помогаю сформировать и публиковать твою афишу в канале."
        f"\n\nКакой вопрос тебя интересует?👇",
        reply_markup=keyboards.create_reply_keyboard(), parse_mode='HTML')


@router.message(Command('about'))
async def command_start(message: Message, state: FSMContext):
    await message.answer(f"Разработчик - @dinozavrik_22")


@router.message(lambda message: message.text == "✅ Афиша в Адлере")
async def handle_text(message: Message, state: FSMContext):
    # Отправляем текстовое сообщение
    await message.answer(
        f"Афиша мероприятий в Адлере формируется чат-ботом 🤖 cледуя простой инструкции, вы можете самостоятельно опубликовать мероприятие."
        f"\n\nРазмещение в афише <u>бесплатное</u>. Периодичность размещения 1️⃣ мероприятие в 3️⃣ дня. "
        f"\n\nРазмещение - моментальное. Мы рекомендуем размещать мероприятия минимум за 3-5 дней до его проведения."
        f"\n\nНа любом этапе заполнения информации о вашем мероприятии вы можете воспользоваться предпросмотром - для этого нажмите кнопку <b>\"Посмотреть\"</b>."
        f"\n\nЕсли в процессе диалога будут проблемы отправьте команду <b>/start</b> чтоб перезапустить бота.",
        parse_mode="HTML")
    data = await state.get_data()
    try:
        data['name'] or data['date'] or data['description'] or data['adress'] or data['price'] or data['not'] or data[
        'photo'] or data['contacts'] or data['message_id']
    except:
        await state.update_data(date=None)
        await state.update_data(description=None)
        await state.update_data(adress=None)
        await state.update_data(price=None)
        await state.update_data(name=None)
        await state.update_data(note=None)
        await state.update_data(photo=None)
        await state.update_data(contacts=None)
        await state.update_data(message_id=None)
    data = await state.get_data()
    await message.answer("Выберите поле для заполнения или редактирования:",
                         reply_markup=keyboards.create_new_keyboard(data=data))



@router.message(lambda message: message.text == "👉 Правила канала")
async def handle_text(message: Message, state: FSMContext):
    await message.answer(
        f"❗️ Правила Канала:"
        f"\n\n1. В канале публикуется <b>БЕСПЛАТНО</b> любая афиша мероприятий в городе <b>АДЛЕР</b>. Онлайн афиша и мероприятия других регионов (Красная Поляна, Сочи и др.) публикуют афишу через администратора канала платно. Условия описаны ниже."
        f"\n\n2. Афиша в Адлере формируется чат-ботом. Нажмите на кнопку <u>✅ Афиша в Адлере</u> и следуйте инструкциям чат бота. После заполнения ваше сообщение мгновенно разместится в канале <b>АФИША•АДЛЕР</b>💬"
        f"\n\n3. Афиша одного и того же мероприятия публикуется 1️⃣ раз в 3️⃣ дня."
        f"\n\n4. Платная реклама публикуется администратором канала. Нажмите на кнопку <u>❌Афиша НЕ в Адлере</u> и в диалоге с администратором <b>@adlerafisha_admin</b> пришлите свою афишу. После согласования и оплаты ваше мероприятие публикуется в канал."
        f"\n\n5. Условия платной рекламы:"
        f"\n✅ Стоимость одной публикации 300р."
        f"\n✅ Стоимость одной публикации + закреп 500р."
        f"\n✅ Реклама одного мероприятия публикуется один раз в три дня."
        f"\n✅ Вы можете сформировать афишу мероприятия без шаблона канала."
        f"\n✅ Вы можете прикреплять к вашей афише ссылки на мероприятие.",
        parse_mode="HTML", reply_markup=keyboards.back_btn2)


@router.message(lambda message: message.text == "❌ Афиша не в Адлере")
async def handle_text(message: Message, state: FSMContext):
    # Отправляем текстовое сообщение
    await message.answer(
        f"Онлайн афиши и мероприятий других регионов (Красная Поляна, Сочи и др.) публикуют афишу через администратора канала платно."
        f"\n\nУсловия платной рекламы:"
        f"\n\n✅ Стоимость одной публикации 300р."
        f"\n✅ Стоимость одной публикации + закреп 500р."
        f"\n✅ Афиша одного мероприятия публикуется один раз в три дня."
        f"\n✅ Закреп афиши на следующий день после публикации 1 день 500р."
        f"\n✅ Вы можете сформировать афишу без шаблона канала."
        f"\n✅ Вы можете прикреплять к вашей афише ссылки на мероприятие."
        f"\n\n➡️ Отправьте рекламу на публикацию 👉<b>@adlerafisha_admin</b>👈"
        f"\n\nПосле оплаты администратор опубликует ваше мероприятие в канал.", reply_markup=keyboards.back_btn2,
        parse_mode='HTML')


@router.callback_query(lambda c: c.data.startswith("field_"))
async def process_field(callback: CallbackQuery, state: FSMContext):
    if callback.data == "field_name":
        data = await state.get_data()
        name = data['name']
        if name != None:
            await callback.message.edit_text(f"▶️ Вы сейчас редактируете поле <b>НАЗВАНИЕ*</b>"
                                             f"\n\nВведите название вашего мероприятия, оно должно быть кратким.Нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания."
                                             f"\n\nТекущее значение поля: {name}", reply_markup=keyboards.back_btn,
                                             parse_mode='HTML')
        else:
            await callback.message.edit_text(f"▶️ Вы сейчас редактируете поле <b>НАЗВАНИЕ*</b>"
                                             f"\n\nВведите название вашего мероприятия, оно должно быть кратким.Нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания."
                                             f"\n\nНажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания.",
                                             reply_markup=keyboards.back_btn, parse_mode='HTML')
        await state.set_state(state=States.name)
    elif callback.data == "field_date":
        data = await state.get_data()
        date = data['date']
        if date != None:
            await callback.message.edit_text(f"▶️ Вы сейчас редактируете поле <b>ДАТА/ВРЕМЯ*</b>"
                                             f"\n\nВведите дату вашего мероприятия. Нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания."
                                             f"\n\n✅ Пример: 8 июня, суббота /10:00-22:00"
                                             f"\n\nТекущее значение поля: {date}", reply_markup=keyboards.back_btn, parse_mode='HTML')
        else:
            await callback.message.edit_text(f"▶️ Вы сейчас редактируете поле <b>ДАТА/ВРЕМЯ*</b>"
                                             f"\n\nВведите дату вашего мероприятия. Нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания."
                                             f"\n\n✅ Пример: 8 июня, суббота /10:00-22:00",
                                             reply_markup=keyboards.back_btn, parse_mode='HTML')
        await state.set_state(state=States.date)
    elif callback.data == "field_description":
        data = await state.get_data()
        description = data['description']
        if description != None:
            await callback.message.edit_text(f"▶️ Вы сейчас редактируете поле <b>ОПИСАНИЕ*</b>"
                                             f"\n\nОпишите мероприятие и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам."
                                             f"\n\n⚠️ Внимание! Ограничение на объем текста - 1200 символов (включая пробелы)."
                                             f"\n\nТекущее значение поля: {description}",
                                             reply_markup=keyboards.back_btn, parse_mode='HTML')
        else:
            await callback.message.edit_text(f"▶️ Вы сейчас редактируете поле <b>ОПИСАНИЕ*</b>"
                                             f"\n\nОпишите мероприятие и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам."
                                             f"\n\n⚠️ Внимание! Ограничение на объем текста - 1200 символов (включая пробелы).",
                                             reply_markup=keyboards.back_btn, parse_mode='HTML')
        await state.set_state(state=States.description)
    elif callback.data == "field_address":
        data = await state.get_data()
        adress = data['adress']
        if adress != None:
            await callback.message.edit_text(f"▶️ Вы сейчас редактируете поле <b>АДРЕС*</b>"
                                             f"\n\nНапишите адрес проведения мероприятия и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания."
                                             f"\n\n✅ Пример: Адлер, Бестужева 1/1, Bestuzhev bar"
                                             f"\n\nТекущее значение поля: {adress}", reply_markup=keyboards.back_btn, parse_mode='HTML')
        else:
            await callback.message.edit_text(f"▶️ Вы сейчас редактируете поле <b>АДРЕС*</b>"
                                             f"\n\nНапишите адрес проведения мероприятия и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания."
                                             f"\n\n✅ Пример: Адлер, Бестужева 1/1, Bestuzhev bar",
                                             reply_markup=keyboards.back_btn, parse_mode='HTML')
        await state.set_state(state=States.address)
    elif callback.data == "field_price":
        data = await state.get_data()
        price = data['price']
        if price != None:
            await callback.message.edit_text(f"▶️ Вы сейчас редактируете поле <b>ЦЕНА</b>"
                                             f"\n\nНапишите стоимость участия и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания."
                                             f"\n\nТекущее значение поля: {price}", reply_markup=keyboards.back_btn,
                                             parse_mode='HTML')
        else:
            await callback.message.edit_text(f"▶️ Вы сейчас редактируете поле <b>ЦЕНА</b>"
                                             f"\n\nНапишите стоимость участия и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания.",
                                             reply_markup=keyboards.back_btn, parse_mode='HTML')
        await state.set_state(state=States.price)
    elif callback.data == "field_contacts":
        data = await state.get_data()
        contacts = data['contacts']
        if contacts != None:
            await callback.message.edit_text(f"▶️ Вы сейчас редактируете поле <b>КОНТАКТЫ*</b>"
                                             f"\n\nУкажите свои контакты и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания."
                                             f"\n\nУкажите свой ник в телеграмме, чтобы участники смогли записаться или задать вам интересующие вопросы по мероприятию. <u>Номер телефона пишите по желанию, не является обязательным</u>."
                                             f"\n\n✅ Пример: @Myusername +79628877016, Мария"
                                             f"\n\nТекущее значение поля: {contacts}", reply_markup=keyboards.back_btn,
                                             parse_mode='HTML')
        else:
            await callback.message.edit_text(f"▶️ Вы сейчас редактируете поле <b>КОНТАКТЫ*</b>"
                                             f"\n\nУкажите свои контакты и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания."
                                             f"\n\nУкажите свой ник в телеграмме, чтобы участники смогли записаться или задать вам интересующие вопросы по мероприятию. <u>Номер телефона пишите по желанию, не является обязательным</u>."
                                             f"\n\n✅ Пример: @Myusername +79628877016, Мария",
                                             reply_markup=keyboards.back_btn, parse_mode='HTML')
        await state.set_state(state=States.contacts)
    elif callback.data == "field_note":
        data = await state.get_data()
        note = data['note']
        if note != None:
            await callback.message.edit_text(f"▶️  Вы сейчас редактируете поле <b>ПРИМЕЧАНИЕ</b>"
                                             f"\n\nПоле не является обязательным. Используйте его для дополнительной информации о скидке на мероприятие, правилах регистрации или как призыв к действию!"
                                             f"\n\n⚠️Внимание! Есть ограничение на количество символов - 100 знаков вместе с пробелами."
                                             f"\n\n✅ Пример:"
                                             f"\nСАМОЕ ЗНАЧИМОЕ СОБЫТИЕ ГОДА. РЕГИСТРИРУЙТЕСЬ ПРЯМО СЕЙЧАС!!✨"
                                             f"\nДЕЙСТВУЕТ ПОВЫШЕНИЕ ЦЕНЫ С 10 ИЮЛЯ!🤫 "
                                             f"\n\nТекущее значение поля: {note}", reply_markup=keyboards.back_btn,
                                             parse_mode='HTML')
        else:
            await callback.message.edit_text(f"▶️  Вы сейчас редактируете поле <b>ПРИМЕЧАНИЕ</b>"
                                             f"\n\nПоле не является обязательным. Используйте его для дополнительной информации о скидке на мероприятие, правилах регистрации или как призыв к действию!"
                                             f"\n\n⚠️Внимание! Есть ограничение на количество символов - 100 знаков вместе с пробелами."
                                             f"\n\n✅ Пример:"
                                             f"\nСАМОЕ ЗНАЧИМОЕ СОБЫТИЕ ГОДА. РЕГИСТРИРУЙТЕСЬ ПРЯМО СЕЙЧАС!!✨"
                                             f"\nДЕЙСТВУЕТ ПОВЫШЕНИЕ ЦЕНЫ С 10 ИЮЛЯ!🤫 ",
                                             reply_markup=keyboards.back_btn,
                                             parse_mode='HTML')
        await state.set_state(state=States.note)
    elif callback.data == "field_photo":
        data = await state.get_data()
        photo = data['photo']
        """if photo != None:
            try:
                await bot.send_photo(chat_id=callback.from_user.id, photo=photo)
                await callback.message.edit_text(f"▶️ Вы сейчас редактируете поле <b>ФОТО</b>"
                                                 f"\n\nНажмите на скрепку чтобы отправить фото или видео афиши мероприятия. Ограничение по количеству 1️⃣ фото или 1️⃣ видео. Ограничение по  размеру файла 3 мб.",
                                                 reply_markup=keyboards.back_btn, parse_mode='HTML')

            except Exception:
                await bot.send_video(chat_id=callback.from_user.id, video=photo)
        else:"""
        await callback.message.edit_text(f"▶️ Вы сейчас редактируете поле <b>ФОТО</b>"
                                         f"\n\nНажмите на скрепку чтобы отправить фото или видео афиши мероприятия. Ограничение по количеству 1️⃣ фото или 1️⃣ видео. Ограничение по  размеру файла 3 мб.",
                                         reply_markup=keyboards.back_btn, parse_mode='HTML')
        await state.set_state(state=States.photo)


@router.message(States.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    keyboard = keyboards.create_new_keyboard(data)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer("Выберите поле для заполнения или редактирования:", reply_markup=keyboard)
    await state.set_state(state=States.process)


@router.message(States.date)
async def process_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    data = await state.get_data()
    keyboard = keyboards.create_new_keyboard(data)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer("Выберите поле для заполнения или редактирования:", reply_markup=keyboard)
    await state.set_state(state=States.process)


@router.message(States.description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    keyboard = keyboards.create_new_keyboard(data)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer("Выберите поле для заполнения или редактирования:", reply_markup=keyboard)
    await state.set_state(state=States.process)


@router.message(States.address)
async def process_address(message: Message, state: FSMContext):
    await state.update_data(adress=message.text)
    data = await state.get_data()
    keyboard = keyboards.create_new_keyboard(data)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer("Выберите поле для заполнения или редактирования:", reply_markup=keyboard)
    await state.set_state(state=States.process)


@router.message(States.price)
async def process_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    keyboard = keyboards.create_new_keyboard(data)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer("Выберите поле для заполнения или редактирования:", reply_markup=keyboard)
    await state.set_state(state=States.process)


@router.message(States.contacts)
async def process_contacts(message: Message, state: FSMContext):
    await state.update_data(contacts=message.text)
    data = await state.get_data()
    keyboard = keyboards.create_new_keyboard(data)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer("Выберите поле для заполнения или редактирования:", reply_markup=keyboard)
    await state.set_state(state=States.process)


@router.message(States.note)
async def process_note(message: Message, state: FSMContext):
    await state.update_data(note=message.text)
    data = await state.get_data()
    keyboard = keyboards.create_new_keyboard(data)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer("Выберите поле для заполнения или редактирования:", reply_markup=keyboard)
    await state.set_state(state=States.process)


@router.message(States.photo)
async def process_photo(message: Message, state: FSMContext):
    if message.photo:
        # Получаем ID самого высокого разрешения фото
        photo_id = message.photo[-1].file_id
        await state.update_data(photo=photo_id)
    elif message.video:
        video_id = message.video.file_id
        await state.update_data(photo=video_id)

    data = await state.get_data()
    keyboard = keyboards.create_new_keyboard(data)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer("Выберите поле для заполнения или редактирования:", reply_markup=keyboard)
    await state.set_state(state=States.process)


@router.callback_query(lambda q: q.data == "back")
async def back(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    keyboard = keyboards.create_new_keyboard(data)
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer("Выберите поле для заполнения или редактирования:", reply_markup=keyboard)
    await state.set_state(state=States.process)


@router.callback_query(lambda q: q.data == "view")
async def back(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    data = await state.get_data()
    text = ''
    username = callback.from_user.username
    if data['name'] is not None:
        text += f"📎{data['name']}\n"
    if data['date'] is not None:
        text += f"📆{data['date']}\n"
    try:
        found_city = None
        for city in configs.CITY:
            if city in data['adress']:
                found_city = city
                break
        if found_city is not None:
            text += f"#{found_city.replace(' ', '_')}\n"
    except:
        pass
    if data['description'] is not None:
        text += f"▶️{data['description']}\n"
    if data['adress'] is not None:
        text += f"📍{data['adress']}\n"
    if data['price'] is not None:
        text += f"💸{data['price']}\n"
    if data['contacts'] is not None:
        text += f"👤{data['contacts']}\n"
    if data['note'] is not None:
        text += f"↗️{data['note']}\n"
    if data['photo'] is not None:
        text += f"\nОпубликовал: @{username}"

        try:
            await bot.send_photo(chat_id=callback.from_user.id, photo=data['photo'], caption=text,
                                 reply_markup=keyboards.back_btn1)
        except Exception:
            await bot.send_video(chat_id=callback.from_user.id, video=data['photo'], caption=text,
                                 reply_markup=keyboards.back_btn1)
    else:
        text += f"\nОпубликовал: @{username}"
        await callback.message.answer(text, reply_markup=keyboards.back_btn1)


@router.callback_query(lambda q: q.data == "send")
async def back(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['message_id'] is not None:
        username = callback.from_user.username
        text = ''
        if data['name'] is not None:
            text += f"📎{data['name']}\n"
        if data['date'] is not None:
            text += f"📆{data['date']}\n"
        try:
            found_city = None
            for city in configs.CITY:
                if city in data['adress']:
                    found_city = city
                    break
            if found_city is not None:
                text += f"#{found_city.replace(' ', '_')}\n"
        except:
            pass
        if data['description'] is not None:
            text += f"▶️{data['description']}\n"
        if data['adress'] is not None:
            text += f"📍{data['adress']}\n"
        if data['price'] is not None:
            text += f"💸{data['price']}\n"
        if data['contacts'] is not None:
            text += f"👤{data['contacts']}\n"
        if data['note'] is not None:
            text += f"↗️{data['note']}\n"
        if data['photo'] is not None:
            text += f"\nОпубликовал: @{username}"
            try:
                mes_id = data['message_id']
                await bot.edit_message_media(chat_id=-1002493912329, message_id=mes_id,
                                             media=InputMediaVideo(media=data['photo']))
                mes = await bot.edit_message_caption(chat_id=-1002493912329, message_id=mes_id, caption=text)
                await state.update_data(message_id=mes.message_id)
            except Exception:
                mes_id = data['message_id']
                await bot.edit_message_media(chat_id=-1002493912329, message_id=mes_id,
                                             media=InputMediaPhoto(media=data['photo']))
                mes = await bot.edit_message_caption(chat_id=-1002493912329, message_id=mes_id, caption=text)
                await state.update_data(message_id=mes.message_id)

        else:
            text += f"\nОпубликовал: @{username}"
            mes_id = data['message_id']
            mes = await bot.edit_message_text(chat_id=-1002493912329, message_id=int(mes_id), text=text)
            await state.update_data(message_id=mes.message_id)
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await callback.message.answer(f"Сообщение отправено в группу", reply_markup=keyboards.back_btn1)
    else:
        global timer_active, remaining_time

        if timer_active:
            hours = remaining_time
            await callback.message.answer(
                f"Таймер уже запущен! Осталось времени: {remaining_time // 3600} часов {remaining_time % 3600 // 60} минут {remaining_time % 60} секунд.")
            return
        username = callback.from_user.username
        text = ''
        if data['name'] is not None:
            text += f"📎{data['name']}\n"
        if data['date'] is not None:
            text += f"📆{data['date']}\n"
        found_city = None
        for city in configs.CITY:
            if city in data['adress']:
                found_city = city
                break
        if found_city is not None:
            text += f"#{found_city}\n"
        if data['description'] is not None:
            text += f"▶️{data['description']}\n"
        if data['adress'] is not None:
            text += f"📍{data['adress']}\n"
        if data['price'] is not None:
            text += f"💸{data['price']}\n"
        if data['contacts'] is not None:
            text += f"👤{data['contacts']}\n"
        if data['note'] is not None:
            text += f"↗️{data['note']}\n"
        if data['photo'] is not None:
            text += f"\nОпубликовал: @{username}"

            try:
                mes = await bot.send_photo(chat_id=-1002493912329, photo=data['photo'], caption=text)
                await state.update_data(message_id=mes.message_id)
            except Exception:
                mes = await bot.send_video(chat_id=-1002493912329, video=data['photo'], caption=text)
                await state.update_data(message_id=mes.message_id)

        else:
            text += f"\nОпубликовал: @{username}"
            mes = await bot.send_message(-1002493912329, text=text)
            await state.update_data(message_id=mes.message_id)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            await callback.message.answer(f"Сообщение отправено в группу", reply_markup=keyboards.back_btn1)

        timer_active = True
        # await callback.message.answer("Таймер запущен на 3 суток. В это время нельзя публиковать новое мероприятие, но можно редактировать уже отправленное сообщение.")

        while remaining_time > 0:
            await asyncio.sleep(1)
            remaining_time -= 1

        timer_active = False
        remaining_time = 86400  # Сброс времени на 3 минуты
        await callback.message.answer("Прошло 3 суток, вам снова можно публиковать афишу!")


@router.callback_query(lambda q: q.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f"Вы уверены, что хотите сбросить все несохраненные данные?",
                                  reply_markup=keyboards.yes_no_btn)

    @router.callback_query(lambda q: q.data == "clear")
    async def yes(callback: CallbackQuery, state: FSMContext):
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await state.clear()
        await callback.message.answer(f"Выбрите пункт меню", reply_markup=keyboards.create_reply_keyboard())

    @router.callback_query(lambda q: q.data == "gotored")
    async def yes(callback: CallbackQuery, state: FSMContext):
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        data = await state.get_data()
        keyboard = keyboards.create_new_keyboard(data)
        await callback.message.answer("Выберите поле для заполнения или редактирования:", reply_markup=keyboard)


@router.callback_query(lambda q: q.data == "back_to_menu")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(
        f"Привет 👋"
        f"\n\nЯ чат-бот помощник канала <b>АФИША•АДЛЕР💬</b>.\nА так же я помогаю сформировать и публиковать твою афишу в канале."
        f"\n\nКакой вопрос тебя интересует?👇",
        reply_markup=keyboards.create_reply_keyboard(), parse_mode='HTML')
