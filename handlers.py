from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config import is_trial_active
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

    @dp.message_handler(commands=["start"])
    async def cmd_start(message: types.Message, state: FSMContext):
        # Перевірка триального періоду
        if not is_trial_active():
            await message.answer("⏳ Ваш пробний період завершився. Щоб продовжити — необхідно оформити оплату ($50).")
            return

        await state.finish()
        await message.answer(dialogs["start"])
        await message.answer(dialogs["q1"])
        await LeadForm.q1.set()

    @dp.message_handler(state=LeadForm.q1)
    async def answer_q1(message: types.Message, state: FSMContext):
        await state.update_data(q1=message.text)
        await message.answer(dialogs["q2"])
        await LeadForm.q2.set()

    @dp.message_handler(state=LeadForm.q2)
    async def answer_q2(message: types.Message, state: FSMContext):
        await state.update_data(q2=message.text)
        await message.answer(dialogs["q3"])
        await LeadForm.q3.set()

    @dp.message_handler(state=LeadForm.q3)
    async def answer_q3(message: types.Message, state: FSMContext):
        await state.update_data(q3=message.text)
        await message.answer(dialogs["contact"])
        await LeadForm.contact.set()

    @dp.message_handler(state=LeadForm.contact)
    async def contact_step(message: types.Message, state: FSMContext):
        contact = message.text.strip()

        # Перевірка телефону або ніку
        if not valid_phone(contact) and not contact.startswith("@"):
            await message.answer("❗️Будь ласка, введіть коректний номер телефону або @username.")
            return

        data = await state.get_data()

        # Збереження заявки в базу
        save_lead(
            user_id=message.from_user.id,
            name=message.from_user.full_name,
            phone=contact,
            answers=[data["q1"], data["q2"], data["q3"]]
        )

        # Фінальне повідомлення для користувача (єдине)
        await message.answer(
            "🎉 Дякуємо! Ваша заявка успішно прийнята.\n"
            "Менеджер зв'яжеться з вами найближчим часом."
        )

        # Завершуємо стан — бот ігнорує наступні дії
        await state.finish()
