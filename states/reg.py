from aiogram.fsm.state import State, StatesGroup

class CompanyRegistration(StatesGroup):
    name = State()
    company_id = State()
    chat_id = State()

class ReferralRegistration(StatesGroup):
    name = State()