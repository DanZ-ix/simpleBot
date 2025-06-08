import asyncio

from loader import dp, types, mongo_conn, FSMContext, bot, welcome_message, rate_limit, logging, user_states, config
from filters.filter_commands import isUser
from utils.state_progress import start_state, gpt_state, state_profile
from utils.keyboards import keyboard


@dp.message_handler(isUser(), commands=['start'], state="*")
@rate_limit(2, 'start')
async def start(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    fullname = message.from_user.full_name
    username = message.from_user.username and f"@{message.from_user.username}" or ""
    user_id = str(message.from_user.id)

    arg = message.get_args()
    if arg:
        user = await mongo_conn.db.users.find_one({'user_id': user_id})

        if user.get('new_user') == True:
            link = await mongo_conn.db.links.find_one({'link_id': int(arg), 'deleted': False})
            if link:
                await mongo_conn.db.links.update_one({'link_id': int(arg)}, {
                    '$set': {'invited_number': int(link.get('invited_number')) + 1}})
            await mongo_conn.db.users.update_one({'user_id': user_id}, {'$set': {'new_user': False}})

    # Сохраняем количество отправленных сообщений
    await state.update_data(sent_count=0)
    # Запускаем рассылку сообщений
    asyncio.create_task(send_messages_periodically(chat_id, state))


async def send_messages_periodically(chat_id: int, state: FSMContext):
    data = await state.get_data()
    sent_count = data.get("sent_count", 0)

    message_dict = await mongo_conn.db.saved_messages.find_one({"message_id": {"$gt": 0}})

    while sent_count < config.start_sleep_count:

        if message_dict is not None:
            new_message = types.Message.to_object(message_dict)
            if new_message.caption is not None:
                await bot.send_message(chat_id, new_message.caption,
                                       entities=new_message.caption_entities,
                                       reply_markup=new_message.reply_markup,
                                       disable_web_page_preview=True)
            else:
                await bot.send_message(chat_id, new_message.text,
                                       entities=new_message.entities,
                                       reply_markup=new_message.reply_markup,
                                       disable_web_page_preview=True)
        else:
            await bot.send_message(chat_id, "Привет", parse_mode='html')
        sent_count += 1
        await state.update_data(sent_count=sent_count)
        await asyncio.sleep(config.start_sleep_time)  # Интервал между сообщениями в секундах

