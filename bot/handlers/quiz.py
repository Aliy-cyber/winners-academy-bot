from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from bot.data.questions import QUESTIONS, get_level_by_score
from bot.keyboards.inline import quiz_options_keyboard, quiz_result_keyboard

router = Router()


class QuizFSM(StatesGroup):
    answering = State()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_question_text(q_id: int, level: str) -> str:
    """Build the header text for a question message."""
    question = QUESTIONS[q_id - 1]
    return (
        f"\U0001f4dd Savol {q_id}/15 | Daraja: {level}\n\n"
        f"{question['text']}"
    )


def _get_level_label(q_id: int) -> str:
    """Return a rough difficulty label based on question position."""
    if q_id <= 5:
        return "Boshlang'ich"
    elif q_id <= 10:
        return "O'rta"
    return "Yuqori"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

@router.callback_query(F.data == "quiz_start")
async def quiz_start(call: CallbackQuery, state: FSMContext):
    """Begin the quiz — send question 1."""
    await call.answer()
    await state.clear()
    await state.update_data(score=0, current_q=1)
    await state.set_state(QuizFSM.answering)

    q_id = 1
    level = _get_level_label(q_id)
    question = QUESTIONS[q_id - 1]

    await call.message.answer(
        _build_question_text(q_id, level),
        reply_markup=quiz_options_keyboard(q_id, question["options"]),
    )


# ---------------------------------------------------------------------------
# Answer handler
# ---------------------------------------------------------------------------

@router.callback_query(StateFilter(QuizFSM.answering), F.data.startswith("quiz_answer:"))
async def quiz_answer(call: CallbackQuery, state: FSMContext):
    """Process an answer, advance to next question or show results."""
    await call.answer()

    # Parse callback data: quiz_answer:<q_id>:<answer_idx>
    parts = call.data.split(":")
    q_id = int(parts[1])
    answer_idx = int(parts[2])

    question = QUESTIONS[q_id - 1]
    is_correct = answer_idx == question["correct"]

    data = await state.get_data()
    score = data.get("score", 0)
    if is_correct:
        score += 1
    await state.update_data(score=score)

    next_q = q_id + 1

    if q_id < 15:
        # Send next question
        level = _get_level_label(next_q)
        next_question = QUESTIONS[next_q - 1]
        feedback = "\u2705 To'g'ri!" if is_correct else f"\u274c Noto'g'ri. To'g'ri javob: {question['options'][question['correct']]}"
        await call.message.answer(feedback)
        await call.message.answer(
            _build_question_text(next_q, level),
            reply_markup=quiz_options_keyboard(next_q, next_question["options"]),
        )
        await state.update_data(current_q=next_q)
    else:
        # Quiz finished — show results
        level_info = get_level_by_score(score)
        level_name = level_info["name"]
        emoji = level_info["emoji"]
        comment = level_info["comment"]

        result_text = (
            f"\U0001f3c6 Test yakunlandi!\n\n"
            f"\U0001f4ca Natijangiz: {score}/15\n"
            f"{emoji} Darajangiz: {level_name}\n\n"
            f"\U0001f4a1 {comment}\n\n"
            "\U0001f680 Endi sinov darsiga yoziling va professional ustozlar bilan "
            "ingliz tilini o'rganing!"
        )

        # Persist quiz result into FSM so register handler can pick it up
        await state.update_data(quiz_score=score, quiz_level=level_name)
        await state.set_state(None)  # leave state open for register flow

        await call.message.answer(
            result_text,
            reply_markup=quiz_result_keyboard(level_name),
        )
