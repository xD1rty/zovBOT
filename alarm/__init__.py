import asyncio
from db import get_all_groups, get_tg_ids_of_group, nearest_zovs
from datetime import datetime, timedelta

async def alarms(bot):
    while True:
        groups = await get_all_groups()
        group_zovs = {group.id: await nearest_zovs(group.id) for group in groups}

        now = datetime.now()
        now_plus_30 = (now + timedelta(minutes=30)).time()
        now_plus_5 = (now + timedelta(minutes=5)).time()

        for zov in group_zovs.items():
            for user in get_tg_ids_of_group(zov.group_id):
                if zov.starttime.time() == now_plus_30:
                    await bot.send_message(user, f"Привет, до встречи осталось пол часа! Ваша ссылка: https://meet.jit.si/{zov.secret_meet_code}")
                elif zov.starttime.time() == now_plus_5:
                    await bot.send_message(user, "Напоминаю, осталось 5 минут до встречи в jit.si")

        await asyncio.sleep(60)
    