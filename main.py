import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.utils.exceptions import MessageNotModified

import config
from states import Form

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def welcome(message: types.Message, new_message=False):
    text = 'Когда будете готовы поделиться информацией — нажмите на кнопку 👇'

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    inside_button = types.InlineKeyboardButton(
        text='Анонимное сообщение',
        callback_data='/inside')

    keyboard.add(inside_button)

    if new_message:
        await bot.send_message(message.chat.id,
                               text,
                               reply_markup=keyboard)
    else:
        try:
            await bot.edit_message_text(text,
                                        chat_id=message.chat.id,
                                        message_id=message.message_id,
                                        reply_markup=keyboard)
        except MessageNotModified:
            pass

    await Form.preparing.set()


@dp.callback_query_handler(lambda call: call.data == '/inside', state='*')
async def invite_to_send_message(call, state: FSMContext):
    await bot.answer_callback_query(call.id)

    text = f'Пришлите сообщение и оно анонимно перешлется ' + \
        f'администратору чата {config.CHAT_NAME}'

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    cancel_button = types.InlineKeyboardButton(
        text='Отмена',
        callback_data='/cancel')

    keyboard.add(cancel_button)

    try:
        await bot.edit_message_text(text,
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    reply_markup=keyboard)
    except MessageNotModified:
        pass

    await Form.inside.set()


@dp.callback_query_handler(lambda call: call.data == '/cancel', state='*')
async def cancel_handler(call, state: FSMContext):
    await bot.answer_callback_query(call.id)
    await state.finish()
    await welcome(call.message)


@dp.message_handler(content_types=types.ContentTypes.ANY, state=Form.inside)
async def catch_feedback(message: types.Message, state: FSMContext):
    await message.send_copy(config.INSIDE_CHANNEL)
    text = 'Спасибо за сообщение!'
    await bot.send_message(message.chat.id, text)
    await Form.preparing.set()
    await welcome(message, new_message=True)


@dp.message_handler(content_types=types.ContentTypes.ANY, state='*')
async def empty_state(message: types.Message):
    await welcome(message, new_message=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
