from dataclasses import dataclass
from typing import List


@dataclass
class Question:
    id: int
    level: str
    text: str
    options: List[str]
    correct: int  # 0-indexed


QUESTIONS: List[Question] = [
    # A1 (1-3)
    Question(1, "A1", "Choose the correct form: 'She ___ a student.'",
             ["am", "is", "are", "be"], 1),
    Question(2, "A1", "What is the plural of 'child'?",
             ["childs", "childes", "children", "childrens"], 2),
    Question(3, "A1", "I ___ to school every day.",
             ["go", "goes", "going", "went"], 0),
    # A2 (4-6)
    Question(4, "A2", "Yesterday I ___ a film.",
             ["watch", "watches", "watched", "watching"], 2),
    Question(5, "A2", "Which sentence is correct?",
             ["She don't like coffee.", "She doesn't likes coffee.",
              "She doesn't like coffee.", "She not like coffee."], 2),
    Question(6, "A2", "There ___ many books on the shelf.",
             ["is", "are", "be", "am"], 1),
    # B1 (7-9)
    Question(7, "B1", "If it ___ tomorrow, we will stay at home.",
             ["rain", "rains", "rained", "will rain"], 1),
    Question(8, "B1", "The book ___ written by Tolstoy.",
             ["is", "was", "were", "has"], 1),
    Question(9, "B1", "The film was so boring that I nearly fell ___.",
             ["asleep", "awake", "alone", "apart"], 0),
    # B2 (10-12)
    Question(10, "B2", "By the time she arrived, he ___ for an hour.",
             ["waited", "has waited", "had been waiting", "was waiting"], 2),
    Question(11, "B2", "His argument was not very ___, so nobody agreed with him.",
             ["persuasive", "pleasant", "precise", "possible"], 0),
    Question(12, "B2", "She said: 'I am tired.' She said that she ___.",
             ["is tired", "was tired", "were tired", "had been tired"], 1),
    # C1 (13-15)
    Question(13, "C1", "Choose the correct meaning of 'ubiquitous':",
             ["Rare and unusual", "Appearing everywhere at the same time",
              "Extremely expensive", "Difficult to understand"], 1),
    Question(14, "C1", "Which sentence is grammatically correct?",
             ["Had I known about the meeting, I would have attended it.",
              "If I would have known, I would attend.",
              "Had I knew about it, I attended.",
              "I would have attend if I knew."], 0),
    Question(15, "C1", "The government needs to ___ action on climate change.",
             ["do", "make", "take", "have"], 2),
]


def get_level_by_score(score: int) -> dict:
    if score <= 3:
        return {
            "level": "A1 \u2014 Beginner",
            "emoji": "\U0001f331",
            "course": "Grammatika \u2014 Beginner",
            "course_id": "grammar",
            "comment": "Siz ingliz tilini 0 dan boshlaysiz. 4\u20136 oy ichida kuchli baza yaratasiz!",
        }
    elif score <= 6:
        return {
            "level": "A2 \u2014 Elementary",
            "emoji": "\U0001f4d7",
            "course": "Grammatika \u2014 Beginner / Pre-IELTS",
            "course_id": "grammar",
            "comment": "Asosiy bilimingiz bor. Grammatika kursini tugatib Pre-IELTS ga o\u2019tasiz!",
        }
    elif score <= 9:
        return {
            "level": "B1 \u2014 Intermediate",
            "emoji": "\U0001f4d8",
            "course": "Pre-IELTS",
            "course_id": "pre_ielts",
            "comment": "Yaxshi daraja! Pre-IELTS kursi bilan 3\u20134 oyda IELTS ga tayyorlanasiz.",
        }
    elif score <= 12:
        return {
            "level": "B2 \u2014 Upper-Intermediate",
            "emoji": "\U0001f4d9",
            "course": "IELTS",
            "course_id": "ielts",
            "comment": "Zo\u2019r natija! Bevosita IELTS kursiga o\u2019tishingiz mumkin. 6.5\u20137.5 ball realistik maqsad!",
        }
    else:
        return {
            "level": "C1 \u2014 Advanced",
            "emoji": "\U0001f3c6",
            "course": "IELTS / CEFR C1",
            "course_id": "ielts",
            "comment": "Ajoyib! Yuqori darajadagi o\u2019quvchisiz. IELTS 7.5\u20138.5 maqsad qo\u2019yish mumkin!",
        }
