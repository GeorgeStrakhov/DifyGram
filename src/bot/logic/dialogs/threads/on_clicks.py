from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll

from src.bot.structures.FSM.dialog_fsm import ThreadsSG


async def select_thread(
    c: CallbackQuery, widget: Any, manager: DialogManager, *args, **kwargs
):
    thread_id: str = args[0]
    manager.dialog_data['thread_id'] = thread_id
    await manager.switch_to(state=ThreadsSG.thread_page)


async def clear_history(
    c: CallbackQuery, widget: Any, manager: DialogManager, *args, **kwargs
):
    del manager.dialog_data['messages_history']
    messages_scroll: ManagedScroll = manager.find('messages')
    await messages_scroll.set_page(0)
