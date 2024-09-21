from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Row, Button, Cancel, Column, Select, Back, ScrollingGroup, LastPage, NextPage, \
    CurrentPage, PrevPage, FirstPage
from aiogram_dialog.widgets.text import Format, Jinja, List
from sulguk import SULGUK_PARSE_MODE

from src.bot.logic.dialogs.threads.getter import get_threads, thread_info_getter
from src.bot.logic.dialogs.threads.input_handlers import thread_message_handler
from src.bot.logic.dialogs.threads.on_clicks import select_thread, clear_history
from src.bot.structures.FSM.dialog_fsm import StartSG, ThreadsSG

from src.bot.utils.translation.i18n_format import I18NFormat

threads_dialog = Dialog(
    Window(
        I18NFormat("select-thread-window", when='threads'),
        I18NFormat('no-threads', when=~F['threads']),
        ScrollingGroup(
            Column(
                Select(
                    text=Jinja("Thread #{{ item.id }}, {{ item.created_at.strftime('%-d.%-m.%y') }}"),
                    id='thread',
                    items='threads',
                    item_id_getter=lambda x: x.id,
                    on_click=select_thread,
                ),
            ),
            id='threads_scroll',
            when='threads',
            hide_on_single_page=True,
            height=5
        ),
        getter=get_threads,
        state=ThreadsSG.select,
    ),
    Window(
        Jinja("<b>Thread #{{ thread.id }}, {{ thread.created_at.strftime('%-d.%-m.%y') }}</b>"),
        List(
            Format('<br><br><b>User</b>: {item[0]}<br><br><b>Assistant</b>: {item[1]}<br>'),
            items='messages',
            sep=' ',
            when='messages',
            id='messages',
            page_size=1,
        ),
        Row(
            FirstPage(
                scroll='messages',
                text=Format('⏮️ {target_page1}'),
            ),
            PrevPage(
                scroll='messages',
                text=Format('◀️'),
            ),
            CurrentPage(
                scroll='messages',
                text=Format('{current_page1}'),
            ),
            NextPage(
                scroll='messages',
                text=Format('▶️'),
            ),
            LastPage(
                scroll='messages',
                text=Format('{target_page1} ⏭️'),
            ),
            when='need_pagination',
        ),
        I18NFormat('continue-thread'),
        MessageInput(thread_message_handler, content_types=[ContentType.TEXT]),
        Back(I18NFormat('back-button'), on_click=clear_history),
        parse_mode=SULGUK_PARSE_MODE,
        getter=thread_info_getter,
        state=ThreadsSG.thread_page
    )
)
