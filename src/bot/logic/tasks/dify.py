import logging

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from markdown import markdown
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sulguk import SULGUK_PARSE_MODE, AiogramSulgukMiddleware

from src.configuration import conf
from src.db.database import create_async_engine, Database
from src.db.models import User
from src.dify.client import Dify

logger = logging.getLogger(__name__)


async def save_conversion(conversation_id: str, user_id: int):
    engine: AsyncEngine = create_async_engine(conf.db.build_connection_str())
    async with AsyncSession(bind=engine) as session:
        db: Database = Database(session)
        user: User = (await db.user.get_by_where(User.user_id == int(user_id)))[0]
        await db.thread.new(conversation_id, user)
        await db.session.commit()


async def get_answer(
        user_input: str,
        user_id: int,
        state: FSMContext,
        conversation_id: str = None,
):
    bot = Bot(conf.bot.token, default=DefaultBotProperties(parse_mode=SULGUK_PARSE_MODE))
    bot.session.middleware(AiogramSulgukMiddleware())
    dify: Dify = Dify(conf.dify.api_key)
    try:
        status_code, response = await dify.send_chat_message(user_input, user_id, conversation_id)
        if status_code == 200:
            answer = markdown(response['answer'])
        else:
            answer = f'Non 200 status code received from Dify API. Check if API key is ok.'
        async with bot:
            await bot.send_message(user_id, answer)
            await state.set_data(
                {"conversation_id": conversation_id if conversation_id else response['conversation_id']}
            )
            if not conversation_id:
                await save_conversion(response['conversation_id'], user_id)

    except TelegramAPIError as e:
        async with bot:
            await bot.send_message(user_id, 'An error has occurred during conversation. Try again!')
        logger.critical(f'Failed to send message. Error: {str(e)}')
    finally:
        await dify.close()
