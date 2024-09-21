from aiogram.fsm.state import StatesGroup, State


class StartSG(StatesGroup):
    greeting = State()


class ThreadsSG(StatesGroup):
    select = State()
    thread_page = State()
