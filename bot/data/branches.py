from dataclasses import dataclass, field
from typing import List


@dataclass
class Teacher:
    name: str
    specialization: str
    level: str
    extra: str = ""


@dataclass
class Branch:
    id: str
    name: str
    icon: str
    address: str
    landmark: str
    latitude: float
    longitude: float
    teachers: List[Teacher] = field(default_factory=list)


BRANCHES = [
    Branch(
        id="yubileniy",
        name="Yubileyniy filiali",
        icon="🏫",
        address="Yubileyniy filiali, Termiz",
        landmark="Ezaz kafesi oldida, Yuridik kollej ro'parasida",
        latitude=37.2242,
        longitude=67.2783,
        teachers=[
            Teacher("Miss Kamola", "Kids (9–13 yosh) va Pre-IELTS", "B2+"),
            Teacher("Miss Dilnora", "0 dan Ingliz tili", "B2"),
        ],
    ),
    Branch(
        id="dubay",
        name="Dubay filiali",
        icon="🏙️",
        address="Dubay filiali, Termiz",
        landmark="Dubay restorani yonida",
        latitude=37.2180,
        longitude=67.2710,
        teachers=[
            Teacher("Ustoz", "Pre-IELTS va IELTS", "B2+"),
        ],
    ),
    Branch(
        id="yashil_dunyo",
        name="Yashil Dunyo filiali",
        icon="🌿",
        address="Yashil Dunyo filiali, Termiz",
        landmark="Kinoteatrning 2-qavati, Yashil bozor ro'parasida",
        latitude=37.2205,
        longitude=67.2820,
        teachers=[
            Teacher("Chori Tursunpo'latov", "0 dan Ingliz tili", "B2"),
            Teacher("Lobar Yaxshiboyeva", "Kids (9–13 yosh) va Pre-IELTS", "B2+"),
        ],
    ),
    Branch(
        id="limonariya",
        name="Limonariya filiali",
        icon="🍋",
        address="Limonariya filiali, Termiz",
        landmark="Yangi Termiz davlat pedagogika universiteti yonida",
        latitude=37.2310,
        longitude=67.2650,
        teachers=[
            Teacher("Ustoz", "Grammatika va Pre-IELTS", "B2"),
        ],
    ),
    Branch(
        id="avtovokzal",
        name="Avtovokzal filiali",
        icon="🚌",
        address="Avtovokzal filiali, Termiz",
        landmark="Hakim at-Termiziy jome masjidi yon tomoni, eski angorski stoyankasi oldida",
        latitude=37.2150,
        longitude=67.2700,
        teachers=[
            Teacher("Ilhombek Safarmuro'v", "0 dan Ingliz tili va Pre-IELTS", "B2"),
        ],
    ),
    Branch(
        id="sentr",
        name="Sentr filiali",
        icon="🏛️",
        address="Sentr filiali, Termiz",
        landmark="Shahar dehqon bozori yonida",
        latitude=37.2260,
        longitude=67.2760,
        teachers=[
            Teacher("Ahmadshoh Murodullayev", "IELTS (barcha 4 skill)", "C1 | IELTS 8.5", "Surxondaryoda IELTS 8.5 olgan eng yuqori ball sohibi"),
        ],
    ),
]

BRANCH_MAP = {b.id: b for b in BRANCHES}
