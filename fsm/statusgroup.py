from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class ProfileStatesGroup(StatesGroup):
    age = State()