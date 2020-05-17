from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    preparing = State()
    inside = State()
