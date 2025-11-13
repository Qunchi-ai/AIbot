from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import ADMIN_ID
from dialogs import dialogs
from db import save_lead
from utils import valid_phone


class LeadForm(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    contact = State()


def register_handlers(dp: Dispatcher):
    dp.middleware.setup(LoggingMiddleware())

    # ------------------------------------
    # /start — без триала, просто старт
    # ------------------------------------
    @dp.message_handler(commands=["start"])
    async def cmd_start(message: types.Message, state: FSMContext):
        await state.finish()
        await message.answer(dialogs["start"])
        await message.answer(dialogs["q1"])
        await LeadForm.q1.set()

    # ------------------------------------
    @dp.message_handler(state=LeadForm.q1)
    async def answer_q1(message: types.Message, state: FSMContext):
        await state.update_data(q1=message.text)
        await message.answer(dialogs["q2"])
        await LeadForm.q2.set()

    # ------------------------------------
    @dp.message_handler(state=LeadForm.q2)
    async def answer_q2(message: types.Message, state: FSMContext):
        await state.update_data(q2=message.text)
        await message.answer(dialogs["q3"])
        await LeadForm.q3.set()

    # ------------------------------------
    @dp.message_handler(state=LeadForm.q3)
    async def answer_q3(message: types.Message, state: FSMContext):
        await state.update_data(q3=message.text)
        await message.answer(dialogs["contact"])
        await LeadForm.contact.set()

    # ------------------------------------
    @dp.message_handler(state=LeadForm.contact)
    async def contact_step(message: types.Message, state: FSMContext):

        contact = message.text.strip()

        # проверка телефона или ника
        if not valid_phone(contact) and not contact.startswith("@"):
            await message.answer("❗️Будь ласка, введіть коректний номер телефону або @username.")
            return

        data = await state.get_data()

        # сохраняем в базу
        save_lead(
            user_id=message.from_user.id,
            name=message.from_user.full_name,
            phone=contact,
            answers=[data["q1"], data["q2"], data["q3"]]
        )

        # ответ пользователю
        await message.answer(dialogs["final"])

        # отправка админу
        if ADMIN_ID != 0:
            await message.bot.send_message(
                ADMIN_ID,
                f"📩 Нова заявка:\n\n"
                f"👤 {message.from_user.full_name}\n"
                f"📞 {contact}\n\n"
                f"1️⃣ {data['q1']}\n"
                f"2️⃣ {data['q2']}\n"
                f"3️⃣ {data['q3']}"
            )

        # конец диалога
        await state.finish()
