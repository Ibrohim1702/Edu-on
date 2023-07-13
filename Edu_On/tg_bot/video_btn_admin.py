from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot.buttons import admin_inline_btn
from tg_bot.models import Course, Sub, Videos


def video_pag(update, context, key=True, dele=True, page=1, tur='cur'):
    if tur == 'vid':
        videos = Videos.objects.all().order_by('-pk')
    else:
        videos = Sub.objects.all().order_by('-pk')

    if len(videos) == 0:
        update.message.reply_text("Bu bo'limda hech narsa topilmadi")
        return 0

    if page > len(videos):
        context.bot.answer_callback_query(update.id, "Bundan keyin kurs yo'q ekan 🥲")
        return 0
    if page < 1:
        context.bot.answer_callback_query(update.id, "Bundan keyin kurs yo'q ekan 🥲")
        return 0

    if key:
        for i in range(page - 1, page):
            strr = f"Name: {videos[i].name}"
            if tur == 'cur':
                strr += f'\nCourse: {videos[i].course.name}'
            elif tur == 'vid':
                strr += f'\nSubCategoriya: {videos[i].sub.name}'

            update.message.edit_text(strr,
                                     reply_markup=admin_inline_btn("pagination_ctg",
                                                                   len=len(videos),
                                                                   ctg=videos[i],
                                                                   tur=tur,
                                                                   page=page))
    else:
        for i in range(page - 1, page):
            update.message.delete() if dele else None
            strr = f"Name: {videos[i].name}"
            if tur == 'cur':
                strr += f'\nCourse: {videos[i].course.name}'
            elif tur == 'vid':
                strr += f'\nSubCategoriya: {videos[i].sub.name}'

            update.message.reply_text(strr,
                                      reply_markup=admin_inline_btn("pagination_ctg",
                                                                    len=len(videos),
                                                                    ctg=videos[i],
                                                                    tur=tur,
                                                                    page=page))


def video_btn(type):
    btn = []
    if type == "course":
        course = Course.objects.all()
        if not course:
            return ReplyKeyboardMarkup([], resize_keyboard=True)
        for i in range(1, len(course), 2):
            btn.append([
                KeyboardButton(course[i - 1].name), KeyboardButton(course[i].name)
            ])
        if len(course) % 2:
            btn.append([KeyboardButton(course[len(course) - 1].name)])
        btn.append([KeyboardButton("🔙 Orqaga")])

    elif type == 'video':
        course = Sub.objects.all()
        if not course:
            return ReplyKeyboardMarkup([], resize_keyboard=True)
        for i in range(1, len(course), 2):
            btn.append([
                KeyboardButton(course[i - 1].name), KeyboardButton(course[i].name)
            ])
        if len(course) % 2:
            btn.append([KeyboardButton(course[len(course) - 1].name)])
        btn.append([KeyboardButton("🔙 Orqaga")])

    return ReplyKeyboardMarkup(btn, resize_keyboard=True)


def video_inline_btn(type, tur, root):
    btn = []
    if type == 'vid':
        btn = [
            [InlineKeyboardButton("Edit name", callback_data=f"edit_{root.id}_{tur}_name")],
            [InlineKeyboardButton("Edit Video", callback_data=f"edit_{root.id}_{tur}_video")],
            [InlineKeyboardButton("🔙Orqaga", callback_data=f"edit_{root.id}_{tur}_back")],
        ]

    return InlineKeyboardMarkup(btn)
