from typing import Any

from aiogram import Bot
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from src.bot.logic.tasks.dify import get_answer
from src.bot.structures.FSM.base_fsm import Conversation


async def thread_message_handler(
        message: Message, widget: Any, manager: DialogManager, **kwargs
):
    conversation_id: str = manager.dialog_data['conversation_id']
    await manager.reset_stack()
    state: FSMContext = manager.middleware_data['state']
    bot: Bot = manager.middleware_data['bot']
    await state.set_state(Conversation.pending)
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    await get_answer(message.text, message.from_user.id, state, conversation_id)
