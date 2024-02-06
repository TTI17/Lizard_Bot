# database.py collects data about users using messages
from os import makedirs
import json
from aiogram.types import Message
from dispatcher import dp
from config import bot

@dp.message_handler()
async def check_users(message: Message):
    user_data = dict(await bot.get_chat_member(message.chat.id, message.from_user.id))
    chat_data = (await bot.get_chat(chat_id=message.chat.id))
    
    chat_data_name = str(chat_data['title'])
    
    # Save user data
    chat_info_path = f'./chat_info_data/{chat_data_name}/{message.from_user.id}'
    makedirs(chat_info_path, exist_ok=True)
    
    with open(f'{chat_info_path}/{message.from_user.id}.json', 'w', encoding='utf-8') as file:
        json.dump(user_data, file, ensure_ascii=False, indent=4)