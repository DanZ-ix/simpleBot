import motor.motor_asyncio


# TODO Вынести всю лоику взаимодействия с БД в этот класс

class mongo_connection:
    client, db = None, None
    db_name = None

    def __init__(self, db_name):
        self.db_name = db_name

    async def connect_server(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://127.0.0.1:27017/?retryWrites=true&w=majority',
                                                             serverSelectionTimeoutMS=5000)
        self.db = self.client[self.db_name]

        self.users = {}
        async for user in self.db.users.find():
            self.users[user['user_id']] = {'fullname': user['fullname'], 'username': user['username']}

        print("mongodb Midjourney connect")
