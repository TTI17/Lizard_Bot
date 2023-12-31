import config
from aiogram import Dispatcher, Bot, executor, types
import logging
import time

from filters import*

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.token)
dp = Dispatcher(bot)

dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(IsChatCreator)
bot_answer = []

#for chat admins/creators
@dp.message_handler(commands=['ban', 'unban','get_admin', 'mute'], commands_prefix = "!/", is_admin=True, is_creator=True)
async def commands(message: types.Message):
    if message.text == '!ban':
        if not message.reply_to_message:
            await message.answer("Я не понимаю твоё сообщение, пожалуйста выдели пользователя")
            return
        
        await message.delete()
        await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        
        # sticker = open('./Telegram/sticker/sticker_ban.webp', 'rb')
        # await message.answer_sticker(sticker)
        await message.answer(f"@{message.reply_to_message.from_user.username} был забанен администратором")

        await bot.send_message(chat_id=1138005743,text=f'Данный пользователь: @{message.reply_to_message.from_user.username} был забанен в группе {message.chat.title}\nСсылка: https://t.me/{message.chat.title}')

    elif message.text == '!unban':
        if not message.reply_to_message:
            await message.answer("Я не понимаю твоё сообщение, пожалуйста выдели пользователя")
            return
        
        await message.delete()

        # sticker = open('.\Telegram\sticker\sticker.webp', 'rb')

        # await message.answer_sticker(sticker=sticker)
        
        await message.bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        await message.answer(f"@{message.reply_to_message.from_user.username} был разбанен")
        await bot.send_message(chat_id=message.reply_to_message.from_user.id, text=f"Ты был разбанен, может присоединяться к чату: https://t.me/{message.chat.username}")

        await bot.send_message(chat_id=1138005743,text=f'Данный пользователь: @{message.reply_to_message.from_user.username} был разбанен в группе {message.chat.title}\nСсылка: https://t.me/{message.chat.title}')

    elif message.text == '!get_admin':
        chat_id = message.chat.id
        
        if not message.reply_to_message:
            await message.reply("Please reply to a user's message to promote them to admin.")
            return

        # Get the user ID of the replied message
        replied_user_id = message.reply_to_message.from_user.id

        # Check if the user is already an admin
        chat_member = await bot.get_chat_member(chat_id, replied_user_id)
        if chat_member.status == 'administrator' or chat_member.status == 'creator':
            await message.reply("You are already an admin!")
        else:
            # Promote the user to admin
            await bot.promote_chat_member(chat_id, replied_user_id, can_change_info=True, can_delete_messages=True,
                                        can_invite_users=True, can_restrict_members=True, can_pin_messages=True,
                                        can_promote_members=False)

            await message.reply("Congratulations! The user has been promoted to admin.")

        
    elif message.text == '!mute':
        if not message.reply_to_message:
            await message.answer("Я не понимаю твоё сообщение, пожалуйста выдели пользователя")

        else:
            await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, until_date = time.time()+86400)
            await bot.send_message(chat_id=message.chat.id,text=f'{message.reply_to_message.from_user.first_name} был отправлен в мут на день' )

    

#for user chat
dp.filters_factory.bind(IsMemberFilter)
@dp.message_handler( commands_prefix = "!/", commands=['report', 'rules'])
async def commands_for_members(message:types.Message):
    if message.text == '!report':
        if not message.reply_to_message:
            await message.answer('Пожалуйста, выделите пользователя, на которого вы хотите кинуть репорт')
            return

        await message.delete()

        # chat = await message.bot.get_chat_administrators(message.chat.id)
        

        # await bot.send_message(chat_id=1138005743, text=f'{chat}')

        await bot.send_message(chat_id=1138005743,text=f'''Данный пользователь: @{message.reply_to_message.from_user.username} написал: "{message.reply_to_message.text}" в группе {message.chat.title}\nСсылка: https://t.me/{message.chat.title}
От кого: @{message.from_user.username}''')
        await bot.send_message(chat_id=message.from_user.id,text='Ваша заявка в обработке')
        # await message.answer('Ваша заявка в обработке')

    elif message.text == '!rules':
        await message.answer("""Правила чата:
        Чат создан для общения и для знакомств, 
        Если же вас как-то оскорбил участник чат - ответьте на его сообщение и напишите /report, администраторы рассмотрят данное оскорбление и будут иметь меры по вопросу о бане участника чата
        Для ознакомления с правилами чата, напишите команду !rules""")

#------------------------------------------------------------------
@dp.message_handler(content_types='new_chat_members')
async def new_member(message : types.Message):
    # sticker = open('./Telegram/sticker/sticker_help.webp', 'rb')
    
    await message.delete()
    # await message.answer_sticker(sticker)
    
    if message.from_user.username == None:
        await message.answer(f'Добро пожаловать в чат {message.chat.title}, {message.from_user.first_name}')
    
    else:    
        await message.answer(f'Добро пожаловать), @{message.from_user.username}')
    
    await bot.send_message(chat_id=1138005743,text=f'@{message.from_user.username} joined in group : {message.chat.title}')

@dp.message_handler(content_types=['left_chat_member'])
async def left_member(message: types.Message):
    # sticker = open('./Telegram/sticker/sticker_leave_member.webp', 'rb')
    
    await message.delete()
    # await message.answer_sticker(sticker)
    
    if message.from_user.username == None:
        await message.answer(f'{message.from_user.first_name} покинул группу')

    else:
        await message.answer(f'@{message.from_user.username} покинул группу')
    
    await bot.send_message(chat_id=1138005743,text=f'@{message.from_user.username}({message.from_user.first_name}) покинул : {message.chat.title}')

@dp.message_handler()
async def filters(message: types.Message):
    k = 0
    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    if member.is_chat_admin() == False:
        for i in range(len(config.ads_words)):
            if str(config.ads_words[i]) in message.text:
                try:
                    await message.delete()
                except Exception:
                    return True

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates= False)