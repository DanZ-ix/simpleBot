from aiogram import Dispatcher
from .filter_commands import isUser, isAdmin

def setup(dp: Dispatcher):
  dp.filters_factory.bind(isUser)