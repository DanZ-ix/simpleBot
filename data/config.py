from configobj import ConfigObj
from mongodb.bot_data_connection import mongo_conn_controller

conf = ConfigObj("data/settings.ini", encoding='UTF8')

bot_token = conf['token']['token'] #"6062088609:AAFIQMq1EqjFp0RStjtkyZb3gxl45YoXmvg" #conf['token']['token']

class configs:
    def __init__(self):
        self.admin_ids = None
        self.channels_auto_join = None
        self.welcome_message = None
        self.auto_join_message = None
        self.db_name = None
        self.bot_token = None
        self.start_sleep_time = None
        self.start_sleep_count = None

    async def set_configs(self, bot_name):
        await mongo_conn_controller.connect_server()
        bot = await mongo_conn_controller.db.bots.find_one({"bot_name": bot_name})
        local = False #True
        try:
            if local:                       # bot.get('dialog_max_tokens')
                self.admin_ids = ["154134326"] # bot.get('admins')
                self.channels_auto_join = "123" #bot.get('auto_join_channel_id')
                self.welcome_message = "start button" # bot.get('start_message')
                self.auto_join_message = "auto_join" #  bot.get('auto_join_message')
                self.db_name = "Midjourney"  #  bot.get('db_name')
                self.start_sleep_time = 3
                self.start_sleep_count = 3
            else:
                self.admin_ids = bot.get('admins')
                self.channels_auto_join = bot.get('auto_join_channel_id')
                self.welcome_message = bot.get('start_message')
                self.auto_join_message = bot.get('auto_join_message')
                self.db_name = bot.get('db_name')
                self.start_sleep_time = bot.get('start_sleep_time', 10)
                self.start_sleep_count = bot.get('start_sleep_count', 3)

        except Exception as e:
            print("Не удалось загрузить настройки", e)


