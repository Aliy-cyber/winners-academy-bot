from dataclasses import dataclass
from typing import List


@dataclass
class Course:
    id: str
    name: str
    icon: str
    target: str
    duration: str
    description: str
    benefits: List[str]


COURSES = [
    Course(
        id="grammar",
        name="Grammatika \u2014 Beginner",
        icon="\U0001f4d6",
        target="0 dan boshlovchilar uchun",
        duration="4\u20136 oy",
        description=(
            "Ingliz tilini mutlaqo bilmaydigan yoki alifbodan boshlamoqchi bo\u2019lganlar uchun. "
            "To\u2019g\u2019ri talaffuz, baza grammatika qoidalari va kundalik muloqot ko\u2019nikmalari o\u2019rgatiladi."
        ),
        benefits=[
            "Ingliz tili alifbosi va talaffuzi",
            "Asosiy grammatika qoidalari (Present, Past, Future)",
            "Kundalik hayotda ishlatiladigan 500+ so\u2019z",
            "Pre-IELTS kursiga to\u2019liq tayyorgarlik",
        ],
    ),
    Course(
        id="pre_ielts",
        name="Pre-IELTS",
        icon="\U0001f4d8",
        target="Bazaviy bilimga egalar uchun (A2\u2013B1)",
        duration="3\u20135 oy",
        description=(
            "IELTS imtihoniga kirish oldidan chuqur bilim va ko\u2019nikmalarni mustahkamlaydigan kurs. "
            "Akademik so\u2019z boyligi, murakkab grammatika va erkin muloqotga tayyorgarlik."
        ),
        benefits=[
            "IELTS 4-skillini (Reading, Listening, Writing, Speaking) o\u2019rganish",
            "Akademik so\u2019z boyligi 1000+ so\u2019z",
            "Mock imtihonlari va haftalik testlar",
            "IELTS kursiga to\u2019liq tayyorgarlik",
        ],
    ),
    Course(
        id="ielts",
        name="IELTS",
        icon="\U0001f393",
        target="B1 va undan yuqori daraja uchun",
        duration="3\u20136 oy",
        description=(
            "Chet el universitetlari, xalqaro grantlar va professional sertifikatlar uchun "
            "IELTS 6.5\u20138.5 ball olish maqsadidagi professional kurs. "
            "IELTS 8.5 sohibi Ahmadshoh Murodullayevdan ta\u2019lim."
        ),
        benefits=[
            "Reading, Listening, Writing, Speaking \u2014 4 ta skill chuqur o\u2019rgatiladi",
            "Haqiqiy IELTS formatida mock imtihonlar",
            "Shaxsiy zaif tomonlarni aniqlash va ustida ishlash",
            "IELTS 6.5\u20138.5 ballga erishish kafolati",
        ],
    ),
    Course(
        id="cefr",
        name="CEFR Guruhlari",
        icon="\U0001f3c5",
        target="Abituriyentlar va o\u2019qituvchilar uchun",
        duration="2\u20134 oy",
        description=(
            "Milliy sertifikat olish maqsadidagi kurs. B2 va C1 darajalaridagi "
            "CEFR sertifikati abituriyentlarga universitetga kirishda, o\u2019qituvchilarga esa "
            "malaka oshirishda 100% imtiyoz beradi."
        ),
        benefits=[
            "CEFR B2 va C1 darajalariga tayyorgarlik",
            "Milliy sertifikat imtiyozlari (universitetga 100% imtiyoz)",
            "O\u2019qituvchilar uchun malaka oshirish sertifikati",
            "Intensiv va tez natijalik dastur",
        ],
    ),
]

COURSE_MAP = {c.id: c for c in COURSES}
