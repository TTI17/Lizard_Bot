from dispatcher import dp, bot
from aiogram import types

@dp.message_handler(content_types='new_chat_members')
async def new_member(message : types.Message):
    
    await message.delete()
    
    if message.from_user.username == None:
        await message.answer(f'Добро пожаловать в чат {message.chat.title}, {message.from_user.first_name}')
    
    else:    
        await message.answer(f'Добро пожаловать), @{message.from_user.username}')
    
    await bot.send_message(chat_id=1138005743,text=f'@{message.from_user.username} joined in group : {message.chat.title}')

@dp.message_handler(content_types=['left_chat_member'])
async def left_member(message: types.Message):
    
    await message.delete()

    if message.from_user.username == None:
        await message.answer(f'{message.from_user.first_name} покинул группу')

    else:
        await message.answer(f'@{message.from_user.username} покинул группу')
    
    await bot.send_message(chat_id=1138005743,text=f'@{message.from_user.username}({message.from_user.first_name}) покинул : {message.chat.title}')
