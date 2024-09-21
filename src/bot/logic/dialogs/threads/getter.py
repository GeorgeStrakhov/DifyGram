from aiogram_dialog import DialogManager
from markdown import markdown

from src.db import Database
from src.db.models import User
from src.db.models.thread import Thread
from src.dify.client import Dify


async def get_threads(dialog_manager: DialogManager, db: Database, user: User, **kwargs):
    threads: list[Thread] = list(await db.thread.get_many(Thread.user == user, order_by=Thread.created_at.desc()))
    return {"threads": threads}


async def thread_info_getter(dialog_manager: DialogManager, db: Database, user: User, dify: Dify, **kwargs):
    thread: Thread = await db.thread.get(int(dialog_manager.dialog_data['thread_id']))
    if dialog_manager.dialog_data.get('messages_history'):
        return {
            "ok": True,
            "messages": dialog_manager.dialog_data['messages_history'],
            "need_pagination": True,
            "thread": thread
        }
    try:
        status_code, response = await dify.get_conversation_history_messages(thread.conversation_id, user.user_id)
        if status_code == 200:
            messages_history: list[tuple[str, str]] = [
                (message['query'], markdown(message['answer'])) for message in response['data']
            ]
            dialog_manager.dialog_data['messages_history'] = messages_history
            dialog_manager.dialog_data['conversation_id'] = thread.conversation_id
            return {
                "ok": True,
                "messages": messages_history,
                "thread": thread,
                "need_pagination": len(messages_history) > 1
            }
        return {"ok": False, "detail": "Non 200 status code"}
    finally:
        await dify.close()
