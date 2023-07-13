from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import requests
from tg_bot.models import *
from tg_bot.services import get_videos


def btns_add_ctg(tur='ctg'):
    tur = 'Course' if tur == 'sub' else 'Kurs Turi' if tur == 'cur' else 'Video' if tur == 'vid' else 'category'
    return ReplyKeyboardMarkup([
        [KeyboardButton(f"Yangi {tur} qo'shish")],
        [KeyboardButton("◀ Orqaga")],
    ], resize_keyboard=True)


def btns(type=None, msg="", sub_id=0, page=1, ctg=None, sub=None, video=None):
    btn = []
    r = requests.get('https://eduon-backend.uz/api/v1/courses/categories/')
    data = r.json()

    if type == "menu":
        for i in range(1, len(data), 2):
            btn.append(
                [KeyboardButton(data[i - 1]['name']), KeyboardButton(data[i]['name'])]
            )
        if len(data) % 2:
            btn.append([
                KeyboardButton(data[len(data) - 1]['name'])
            ])
        btn.append([
            KeyboardButton("🔙 Orqaga")
        ])

    elif type == "sub":
        for i in data:
            if i['name'] == msg:
                data2 = i['subcategory']
                if len(data2) > 2:
                    for j in range(1, len(data2), 2):
                        btn.append(
                            [KeyboardButton(data2[j - 1]['name']), KeyboardButton(data2[j]['name'])]
                        )
                    if len(data2) % 2:
                        btn.append([
                            KeyboardButton(data2[-1]['name'])
                        ])
                btn.append(
                    [KeyboardButton("🔙 Orqaga")]
                )
                break

    # - Bepul bo'limi uchun

    elif type == "Boshmenu":
        btn = [
            [KeyboardButton("🆓 Bepul 🆓"), KeyboardButton("💎 Premium 💎")]
        ]

    elif type == "manu1":
        btn = [
            [KeyboardButton("Menu"), KeyboardButton("Biz bilan bog'lanish 📞")],
            [KeyboardButton("🔙 Orqaga")]
        ]

    elif type == "ctgs":
        btn = []
        ctgs = Category.objects.all()
        for i in range(1, len(ctgs), 2):
            btn.append([
                KeyboardButton(ctgs[i - 1].name), KeyboardButton(ctgs[i].name)
            ])
        if len(ctgs) % 2:
            btn.append([KeyboardButton(ctgs[len(ctgs) - 1].name)])
        btn.append([KeyboardButton("🔙 Orqaga")])

    elif type == "course":
        btn = []
        ctgs = Category.objects.filter(name=ctg).first()
        if not ctgs:
            return ReplyKeyboardMarkup([], resize_keyboard=True)

        course = Course.objects.filter(ctg=ctgs)
        if not course:
            return ReplyKeyboardMarkup([], resize_keyboard=True)
        for i in range(1, len(course), 2):
            btn.append([
                KeyboardButton(course[i - 1].name), KeyboardButton(course[i].name)
            ])
        if len(course) % 2:
            btn.append([KeyboardButton(course[len(course) - 1].name)])
        btn.append([KeyboardButton("🔙 Orqaga")])

    elif type == "subfree":
        btn = []
        ctgs = Course.objects.filter(name=sub).first()
        if not ctgs:
            return ReplyKeyboardMarkup([], resize_keyboard=True)
        course = Sub.objects.filter(course=ctgs)

        if not course:
            return []
        for i in range(1, len(course), 2):
            btn.append([
                KeyboardButton(course[i - 1].name), KeyboardButton(course[i].name)
            ])
        if len(course) % 2:
            btn.append([KeyboardButton(course[len(course) - 1].name)])
        btn.append([KeyboardButton("🔙 Orqaga")])

    elif type == 'video_name':
        videos = get_videos(video)

        for i in range(1, len(videos), 2):
            btn.append([
                KeyboardButton(videos[i - 1]['name']), KeyboardButton(videos[i]['name']),
            ])

        if len(videos) % 2:
            btn.append([KeyboardButton(videos[- 1]['name'])])
        btn.append([KeyboardButton("🔙 Orqaga")])
    return ReplyKeyboardMarkup(btn, resize_keyboard=True)


# print(j['name'])


def inline_btn(type, page=1, ctg_id=0, data=None):
    btn = []
    if type == "course":
        if not data:
            return []
        print(page)
        for i in range(page - 1, page):
            print(i)
            btn.append([
                InlineKeyboardButton("🔙 Ortga", callback_data=f"prev_{page}_{ctg_id}"),
                InlineKeyboardButton(f"{page}/{len(data)}", callback_data=f"pass"),
                InlineKeyboardButton("Keyingi 🔜", callback_data=f"next_{page}_{ctg_id}"),
            ])
            btn.append([InlineKeyboardButton("Kursni ko'rish",
                                             url=f"https://eduon.uz/chosenCourse/{data[i]['id']}")])
    return InlineKeyboardMarkup(btn)


def admin_btn(type=None):
    btn = []
    if type == "admin_menu":
        btn = [
            [KeyboardButton("Categorys"), KeyboardButton("Courses"), KeyboardButton("Kurs turi"),
             KeyboardButton("Videos")],
            [KeyboardButton("Reklama yuborish"), KeyboardButton("Users 👤")],
            [KeyboardButton("Botga qaytish 🏘")]
        ]
    elif type == 'conf':
        btn = [
            [KeyboardButton("Ha"), KeyboardButton("Yo'q")]
        ]

    return ReplyKeyboardMarkup(btn, resize_keyboard=True)


def admin_inline_btn(type, tur='ctg', page=1, len=1, ctg=None, video=None):
    btn = []

    if type == "pagination_ctg":
        btn = [
            [InlineKeyboardButton("Edit ⚙", callback_data=f"edit_{ctg.id}_{tur}"),
             InlineKeyboardButton("Delete ❌", callback_data=f"del_{ctg.id}_{tur}")],
            [InlineKeyboardButton("🔙Orqaga", callback_data=f"prev_{tur}_{page}"),
             InlineKeyboardButton(f"{page}/{len}", callback_data=f"{page}_{ctg.id}"),
             InlineKeyboardButton("Keyingi🔜", callback_data=f"next_{tur}_{page}")]
        ]
    elif type == 'conf':
        btn = [
            [InlineKeyboardButton("Ha ✅", callback_data=f"del_{ctg.id}_{tur}_ha"),
             InlineKeyboardButton("Yo'q ❌", callback_data=f"del_{ctg.id}_{tur}_no")],
            [InlineKeyboardButton("🔙Orqaga", callback_data=f"del_{ctg.id}_{tur}_back")],

        ]
    elif type == "ctg_edit":
        btn = [
            [InlineKeyboardButton("Edit name", callback_data=f"edit_{ctg.id}_{tur}_name")],
            [InlineKeyboardButton("🔙Orqaga", callback_data=f"edit_{ctg.id}_{tur}_back")],
        ]

    return InlineKeyboardMarkup(btn)
