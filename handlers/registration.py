from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from .general import GeneralStates, db
from model import User


class RegistrationStates(StatesGroup):
    registration = State()
    name = State()
    verification = State()
    password = State()
    final = State()


router = Router()


@router.message(StateFilter(GeneralStates.start), Command('registration'))
async def start_handler(message: types.Message, state: FSMContext):
    if db.check_id(message.chat.id):
        await message.answer('Пользователь с таким id уже есть')
        await state.set_state(GeneralStates.start)
        await message.answer('Введите /login для авторизации')
        return

    await message.answer('Регистрация!, для продолжения введите логин')
    await state.update_data(id=message.chat.id)
    await state.set_state(RegistrationStates.name)


@router.message(StateFilter(RegistrationStates.name), F.text)
async def login_handler(message: types.Message, state: FSMContext):
    if db.check_login(message.text):
        await message.answer('Такой пользователь уже есть')
        await state.clear()
        await message.answer('Введите /login для авторизации')
        return
    
    await state.update_data(login=message.text)
    await state.set_state(RegistrationStates.final)
    await message.answer('Ваш логин принят')

    data = await state.get_data()
    id = data['id']
    login = data['login']
    password = data['id']
    user = User(id, login, password)

    db.add_user(user)

    await message.answer('Регистрация завершена')

    await state.set_state(GeneralStates.start)
    await message.answer('Для продолжения нажмите /login')


    




