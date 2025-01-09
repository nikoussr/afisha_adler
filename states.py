from aiogram.filters.state import State, StatesGroup


class States(StatesGroup):
    name = State()
    date = State()
    address = State()
    conductor = State()
    price = State()
    note = State()
    description = State()
    contacts = State()
    process = State()
    photo = State()
