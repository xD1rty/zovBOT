import datetime
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.reg import ReferralRegistration, CompanyRegistration
from keyboards.inline import add_to_chat
from aiogram.enums import ChatType
import os

from pyrogram import Client

from pyrogram.raw.functions.contacts import ResolveUsername

pyrogram_client = Client(
    "bot",
    bot_token=os.getenv("TG_TOKEN"),
    api_id=os.getenv("API_ID"),
    api_hash=os.getenv("API_HASH")
)

from dateutil.parser import parse

import db

main_router = Router()


@main_router.message(CommandStart(), F.chat.type == ChatType.PRIVATE)
async def start_bot(message: Message, command: Command, state: FSMContext):
    if command.args == None:
        await message.answer("Здравствуйте! Для регистрации введите некоторые данные. \n"
                             "Для начала, хотел бы попросить название компании")
        await state.set_state(CompanyRegistration.name)
    else:
        await message.answer("Вы добавлены в группу!")


@main_router.message(CompanyRegistration.name, F.chat.type == ChatType.PRIVATE)
async def get_username_and_request_id(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Очень крутое название. Введите пожалуйста ID вашей компании. \n"
                         "Это может быть ее название прописными английскими буквами")
    await state.set_state(CompanyRegistration.company_id)


@main_router.message(CompanyRegistration.company_id, F.chat.type == ChatType.PRIVATE)
async def get_id_and_request_chat_invite(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    await message.answer("Добавь бота в чат. После добавления бот пришлет айди, напишите мне его", reply_markup=add_to_chat)
    await state.set_state(CompanyRegistration.chat_id)

@main_router.message(CompanyRegistration.chat_id, F.chat.type == ChatType.PRIVATE)
async def get_id_and_request_chat_invite_2(message: Message, bot: Bot, state: FSMContext):
    try:
        data = await state.get_data()
        await message.answer("Все готово! Компания зарегистрирована")
        await bot.send_message(int(message.text), f"Привет, {data['name']}! \nМы вас приветствуем!\nСсылка для вступления в команду - t.me/soZOVon_bot?start={data['id']}")
        await state.clear()
    except TypeError:
        await message.answer("Введите ID еще раз!")

@main_router.message(CommandStart())
async def start_chat_bot(message: Message):
    await message.answer(f"ID вашей группы: {message.chat.id}")

@main_router.message(Command("meet"))
async def schedule_meet(message: Message):
    time = parse(message.text.split("\n")[2])
    participants = message.text.split("\n")[1]
    
    try:
        await pyrogram_client.start()
    except:
        pass
    
    ids = {}

    for i in participants.split(" "):
        res = await pyrogram_client.invoke(ResolveUsername(username=i.replace("@", "")))
        ids[i] = res.users[0].id

    org = await db.register(message.from_user.username, message.from_user.id)
    group = await db.create_group(org.id)

    for k in ids:
        user = await db.register(k, ids[k])

        await db.add_user_to_group(user.id, group.id)
    
    await db.create_zov(time, group.id)

    await message.answer("Встреча создана!")
