from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResult,
    InlineQueryResultArticle,
    InputTextMessageContent,
    ChosenInlineResult,
    LinkPreviewOptions
)

inline_router = Router()

@inline_router.inline_query()
async def new_conference(query: InlineQuery) -> None:
    data, username, time = query.query, [], ""
    if data.startswith("@"):
        ...