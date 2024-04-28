from tortoise import Tortoise
import asyncio
import db
from datetime import timedelta, datetime

async def init():
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    await Tortoise.init(
        # db_url='mysql://root:podstepinlenok@bamaec.ru:24566/zovbot',
        db_url='sqlite://zovbot.db?cache=shared&timeout=5000',
        modules={'models': ['db.models']}
    )

    # Generate the schawema
    await Tortoise.generate_schemas()

    

asyncio.run(init())

