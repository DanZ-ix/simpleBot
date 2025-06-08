import time


class OtherCommands():
    trash_data = {}
    logging = None
    bot, dp, types = None, None, None

    async def delete_commands(self, admin_id):
        await self.dp.bot.delete_my_commands(self.types.bot_command_scope.BotCommandScopeChat(admin_id))

    async def set_commands(self):
        await self.bot.set_my_commands([
            self.types.BotCommand("start", "start")
        ], self.types.bot_command_scope.BotCommandScopeAllPrivateChats('all_private_chats'))

    async def set_admin_commands(self, admins):
        for id in admins:
            try:
                await self.dp.bot.set_my_commands([
                    self.types.BotCommand("update_join_message", "Обновить рекламное сообщение"),
                    self.types.BotCommand("check_join_message", "Проверить рекламное сообщение"),
                    self.types.BotCommand("get_users", "Выгрузить пользователей"),
                    self.types.BotCommand("show_links", "Показать реферальные ссылки"),
                    self.types.BotCommand("add_link", "Добавить ссылку")
                ], self.types.bot_command_scope.BotCommandScopeChat(id))
            except:
                pass

other_commands = OtherCommands()
