from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards import get_general_kb
from model import DBSQL_Manager

class GeneralStates(StatesGroup):
    start = State()
    registration = State()
    login = State()
    statistic = State()


router = Router()
db = DBSQL_Manager()

@router.message(StateFilter(None), Command('start'))
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer(f'{message.chat.id}')
    await message.answer('Привет, я создан для финансов. Для регистрации напишите \n/registration\n'
                         'если уже зарегестрированы напишите \n/login\n'
                         'или нажмите соответствующие кнопки', reply_markup=get_general_kb())
    await state.set_state(GeneralStates.start)





@router.message(Command('help'))
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer(f'1. **`/start`** - Приветственное сообщение и краткая инструкция по использованию бота.\n'
                            '2. **`/register`** - Регистрация нового пользователя в системе.\n'
                            '3. **`/login`** - Авторизация пользователя для доступа к его данным.\n'
                            '4. **`/add_income [сумма] [категория]`** - Добавление дохода с указанием суммы и категории.\n'
                            '5. **`/add_expense [сумма] [категория]`** - Добавление расхода с указанием суммы и категории.\n'
                            '6. **`/set_goal [сумма] [описание]`** - Установка финансовой цели с указанием суммы и описания.\n'
                            '7. **`/view_transactions [период]`** - Просмотр истории транзакций за указанный период.\n'
                            '8. **`/statistics`** - Просмотр статистики по расходам и доходам, а также прогрессу в достижении финансовых целей.\n'
                            '9. **`/help`** - Список доступных команд и описание их использования.')
    
