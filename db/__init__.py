from tortoise import Tortoise, run_async
from .models import User, Group, Zov
import random
import string

def generate_invite_code(length=8):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

async def register(nickname, tg_id):
    user = User(username=nickname, tg_id=tg_id)
    await user.save()
    return user

async def create_group(organizer):
    group = Group(organizer_id=organizer, invite_code=generate_invite_code(length=16))
    await group.save()
    await group.participants.add(await get_user_by_id(organizer))
    await group.save()

    return group

async def create_zov(time, group_id):
    zov = Zov(starttime=time, secret_meet_code=generate_invite_code(length=16), group_id=group_id)
    await zov.save()

async def get_group_by_invite_code(invite_code):
    return await Group.filter(invite_code=invite_code).first()

async def add_user_to_group(user_id, group_id):
    user = await User.filter(id=user_id).first()
    group = await Group.filter(id=group_id).first()
    await group.participants.add(user)
    await group.save()

async def nearest_zovs(group_id):
    return await Zov.filter(group_id=group_id).order_by('starttime')

async def get_tg_ids_of_group(group_id):
    return await User.filter(groups__id=group_id).values('tg_id')

async def get_zov_meet_link(zov_id):
    return await Zov.filter(id=zov_id).first().values('secret_meet_code')

async def get_user_by_id(id):
    return await User.filter(id=id).first()

async def get_all_groups():
    return await Group.all()

