from datetime import datetime
from aiogram.dispatcher.filters import BoundFilter

from loader import types, conf, mongo_conn, bot, dp, admin_list
from utils.state_progress import state_profile


class isUser(BoundFilter):
    async def check(self, message: types.Message):
        chat, user_id = 'message' in message and message.message.chat.id or message.chat.id, str(message.from_user.id)
        fullname = message.from_user.full_name
        username = message.from_user.username or ''

        if mongo_conn.users.get(user_id) is None:
            obj = {'user_id': user_id, 'fullname': fullname, 'username': username, 'history': {}, 'dialogs': [],
                   'date': datetime.now(), 'message_filters': [], 'attempts_free': 1, 'attempts_pay': 0,
                   'attempts_channel': [], 'new_user': True}
            await mongo_conn.db.users.insert_one(obj)
        else:
            await mongo_conn.db.users.update_one({'user_id': int(user_id)}, {'$set': {'new_user': False}})
        return True


async def check_sub(user_id, chat_id):
    try:
        ch = await bot.get_chat_member(chat_id, user_id)
        return ch.status in ['creator', 'administrator', 'member']
    except:
        return True





class isAdmin(BoundFilter):
    async def check(self, message: types.Message):
        user_id = str(message.from_user.id)
        if user_id in admin_list:
            return True
        return False
