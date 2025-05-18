from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from .general import GeneralStates, db
from config import PERIOD
from datetime import date, timedelta


class LoginStates(StatesGroup):
    login = State()
    logined = State()

router = Router()

@router.message(StateFilter(GeneralStates.start), Command('login'))
async def login_handler(message: types.Message, state: FSMContext):
    if db.check_id(message.chat.id):
        await message.answer('Введите свой логин')
        await state.set_state(LoginStates.login)
        return
    
    await message.answer('Вы не регистрировались в боте')
    await message.answer('Для регистрации нажмите /registration')
    state.set_state(GeneralStates.start)


@router.message(StateFilter(LoginStates.login), F.text)
async def login_handler(message: types.Message, state: FSMContext):
    if db.check_login(message.text):
        await state.set_state(LoginStates.logined)
        await message.answer('Теперь вы можете пользоваться функционалом бота /help')
        return

    await message.answer('Пользователь с таким логином не найден.')
    await message.answer('Введите логин ещё раз.')


#добавление доходов
@router.message(StateFilter(LoginStates.logined), Command('add_income'))
async def add_income(message: types.Message, state: FSMContext):
    parametrs = message.text.strip().split()
    if len(parametrs) != 3:
        await message.answer("Введите команду с параметрами сумма и категория\n" \
        "Пример: /add_income сумма категория")
        return
    
    try:
        amount = int(parametrs[1].strip())
        category = parametrs[2].strip()
    except:
        await message.answer("Неправильно заданны параметры.\n" \
        "Пример: /add_income сумма категория")
        return
    if amount > 0:
        id_user = message.chat.id
        db.add_income(id_user, amount, category)
        await message.answer('Доходы добавлены')
        await view_transactions(message, state)
    else:
        await message.answer("Сумма не может быть меньше или равна нулю")
        

#добавление расходов
@router.message(StateFilter(LoginStates.logined), Command('add_expense'))
async def add_expense(message: types.Message, state: FSMContext):
    parametrs = message.text.strip().split()
    if len(parametrs) != 3:
        await message.answer("Введите команду с параметрами сумма и категория\n" \
        "Пример: /add_expense сумма категория")
        return
    
    try:
        amount = int(parametrs[1].strip())
        category = parametrs[2].strip()
    except:
        await message.answer("Неправильно заданны параметры.\n" \
        "Пример: /add_expense сумма категория")
        return
    if amount > 0:
        id_user = message.chat.id
        db.add_expense(id_user, amount, category)
        await message.answer('Расходы добавлены')
    else:
        await message.answer("Сумма не может быть меньше или равна нулю")
        

#добавление цели
@router.message(StateFilter(LoginStates.logined), Command('set_goal'))
async def set_goal(message: types.Message, state: FSMContext):
    parametrs = message.text.strip().split()
    if len(parametrs) != 3:
        await message.answer("Введите команду с параметрами сумма и категория\n" \
        "Пример: /set_goal сумма описание")
        return
    
    try:
        amount = int(parametrs[1].strip())
        description = parametrs[2].strip()
    except:
        await message.answer("Неправильно заданны параметры.\n" \
        "Пример: /set_goal сумма описание")
        return
    
    if amount > 0:
        id_user = message.chat.id
        db.set_goal(id_user, amount, description)
        await message.answer('Цель добавлена')
    else:
        await message.answer("Сумма не может быть меньше или равна нулю")
        
    
#просмотр истории транзакций 
@router.message(StateFilter(LoginStates.logined), Command('view_transactions'))
async def view_transactions(message: types.Message, state: FSMContext):
    parametrs = message.text.strip().split()
    if len(parametrs) == 1:
        await message.answer("Введите команду с параметрами период и категория(не обязательно)\n" \
                            "Пример: /view_transactions месяц\n" \
                            "/view_transactions день еда")
        return
    elif len(parametrs) == 2:
        try:
            period = parametrs[1].strip()
            delta = int(PERIOD[period])
            period = date.today() - timedelta(delta)
            id_user = message.chat.id
            incomes = db.view_incomes(id_user, period)
            expenses = db.view_expenses(id_user, period)

        except:
            await message.answer("Неправильно заданны параметры.\n" \
                                "Пример: /view_transactions день\неделя\месяц\год\n" \
                                "/view_transactions день еда")
            return
        
    elif len(parametrs) == 3:
        try:
            period = parametrs[1].strip()
            category = parametrs[2].strip()
            delta = int(PERIOD[period])
            period = date.today() - timedelta(delta)
            id_user = message.chat.id
            incomes = db.view_incomes(id_user, period, category)
            expenses = db.view_expenses(id_user, period, category)

        except:
            await message.answer("Неправильно заданны параметры.\n" \
                                "Пример: /view_transactions день\неделя\месяц\год\n" \
                                "/view_transactions день еда")
            return
        
    await message.answer('Доходы')
    for income in incomes:
        await message.answer(f'{income}')
    await message.answer('Расходы')
    for expense in expenses:
        await message.answer(f'{expense}')
        

@router.message(StateFilter(LoginStates.logined), Command('goal'))
async def view_transactions(message: types.Message, state: FSMContext):
    id_user = message.chat.id
    delta = db.get_sum_incomes(id_user)[0] - db.get_sum_expenses(id_user)[0]
    goal = db.get_goal(id_user)
    if delta >= goal[0]:
        db.delete_goal(id_user)
        await message.answer(f'Вы достигли цели {goal[1]}')

    return


@router.message(StateFilter(LoginStates.logined), Command('statistics'))
async def statistics(message: types.Message, state: FSMContext):
    
    await message.answer(f'Какую статистику вы хотите получить?\n'
                        '/amount_incomes - весь доход за всё время\n'
                        '/amount_expenses - все расходы\n'
                        '/balance - баланс\n'
                        '/category_incomes - доходы по категориям\n'
                        '/category_expenses - расходы по категориям\n')

@router.callback_query(F.data == "amount_incomes")
@router.message(StateFilter(LoginStates.logined), Command('amount_incomes'))
async def amount_incomes(message: types.Message, state: FSMContext):
    id_user = message.chat.id
    amount = db.get_sum_incomes(id_user)[0] 
    await message.answer(f'Сумма доходов равна {amount}')
    

@router.message(StateFilter(LoginStates.logined), Command('amount_expenses'))
async def amount_expenses(message: types.Message, state: FSMContext):
    id_user = message.chat.id
    amount = db.get_sum_expenses(id_user)[0]
    await message.answer(f'Сумма расходов равна {amount}')


@router.message(StateFilter(LoginStates.logined), Command('balance'))
async def balance(message: types.Message, state: FSMContext):
    amount_incomes = db.get_sum_incomes
    amount_expenses = db.get_sum_expenses
    balance = amount_incomes - amount_expenses 
    await message.answer(f'Баланс равен {balance}')
    

@router.message(StateFilter(LoginStates.logined), Command('category_incomes'))
async def category_incomes(message: types.Message, state: FSMContext):
    id_user = message.chat.id
    total = db.get_sum_incomes(id_user)[0]
    categories = db.get_incomes_structure(id_user)
    for category, amount in categories:
        percent = (amount / total) * 100
        await message.answer(f'{category}: {percent:1f}% от общих доходов {total}')

    
@router.message(StateFilter(LoginStates.logined), Command('category_expenses'))
async def category_expenses(message: types.Message, state: FSMContext):
    id_user = message.chat.id
    total = db.get_sum_expenses(id_user)[0]
    categories = db.get_expense_structure(id_user)
    for category, amount in categories:
        percent = (amount / total) * 100
        await message.answer(f'{category}: {percent:.1f}% от общих расходов {total}')
    