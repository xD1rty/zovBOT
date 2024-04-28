import asyncio
from db import get_all_groups, get_tg_ids_of_group, nearest_zovs
from datetime import datetime, timedelta

async def alarms(bot):
    alerted_30 = []
    alerted_5 = []
    while True:
        groups = await get_all_groups()
        group_zovs = {group.id: await nearest_zovs(group.id) for group in groups}

        now = datetime.now()
        print(group_zovs.items())
        for zov in group_zovs.items():
            for user in await get_tg_ids_of_group(zov[0]):
                print(zov[1][0].starttime.replace(tzinfo=None) - datetime.now())
                if zov[1][0].starttime.replace(tzinfo=None) - datetime.now() < timedelta(minutes=5) and user["tg_id"] not in alerted_5:
                    await bot.send_message(user["tg_id"], "Напоминаю, осталось 5 минут до встречи в jit.si")
                    alerted_5.append(user["tg_id"])
                elif zov[1][0].starttime.replace(tzinfo=None) - datetime.now() < timedelta(minutes=30) and user["tg_id"] not in alerted_30 and user["tg_id"] not in alerted_5:
                    print(user)
                    await bot.send_message(user["tg_id"], f"Привет, до встречи осталось пол часа! Ваша ссылка: https://meet.jit.si/{zov[1][0].secret_meet_code}")
                    alerted_30.append(user["tg_id"])

        await asyncio.sleep(60)
    