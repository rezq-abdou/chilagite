from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import BOOKS, CATEGORY_ORDER

router = Router()

def main_keyboard():
    kb = InlineKeyboardBuilder()
    for key in CATEGORY_ORDER:
        cat = BOOKS[key]
        kb.button(text=cat["name_ar"], callback_data=f"cat_{key}")
    kb.adjust(2)
    return kb.as_markup()

WELCOME = (
    "📚 *مرحبًا بك في The Mindset Library*\n\n"
    "مكتبتك الرقمية المتكاملة — اختر المجال الذي يهمك واكتشف أفضل الكتب\n"
    "مع معلومات شاملة عن كل كتاب ورابط تحميل مباشر.\n\n"
    "👇 اختر المجال:"
)

@router.message(Command("start"))
async def cmd_start(msg: Message):
    await msg.answer(WELCOME, reply_markup=main_keyboard())

@router.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer(
        "📚 *The Mindset Library*\n\n"
        "الأمر /start — عرض القائمة الرئيسية\n"
        "الأمر /help — هذه المساعدة\n\n"
        "اختر مجالاً وستظهر لك الكتب مع التفاصيل."
    )

@router.message()
async def any_message(msg: Message):
    await msg.answer(WELCOME, reply_markup=main_keyboard())

@router.callback_query(F.data == "main_menu")
async def cb_main_menu(cq: CallbackQuery):
    await cq.message.edit_text("👇 اختر المجال:", reply_markup=main_keyboard())

@router.callback_query(F.data.startswith("cat_"))
async def cb_show_books(cq: CallbackQuery):
    cat_key = cq.data[4:]
    if cat_key not in BOOKS:
        await cq.answer("القسم غير موجود", show_alert=True)
        return
    cat = BOOKS[cat_key]

    kb = InlineKeyboardBuilder()
    for idx, book in enumerate(cat["books"]):
        kb.button(text=f"📖 {book['name']}", callback_data=f"bk_{idx}_{cat_key}")
    kb.button(text="🏠 القائمة الرئيسية", callback_data="main_menu")
    kb.adjust(1)

    await cq.message.edit_text(
        f"📚 *{cat['name_ar']}*\nاختر الكتاب لعرض التفاصيل:",
        parse_mode="Markdown",
        reply_markup=kb.as_markup()
    )

@router.callback_query(F.data.startswith("bk_"))
async def cb_show_book(cq: CallbackQuery):
    rest = cq.data[3:]
    idx_str, cat_key = rest.split("_", 1)
    idx = int(idx_str)

    if cat_key not in BOOKS:
        await cq.answer("القسم غير موجود", show_alert=True)
        return
    cat = BOOKS[cat_key]
    if idx >= len(cat["books"]):
        await cq.answer("الكتاب غير موجود", show_alert=True)
        return
    book = cat["books"][idx]

    text = (
        f"📖 *{book['name']}*\n"
        f"👤 *المؤلف:* {book['author']}\n"
        f"⭐ *التقييم:* {book['rating']}\n"
        f"📄 *عدد الصفحات:* {book['pages']}\n\n"
        f"📝 *نبذة عن الكتاب:*\n{book['description']}"
    )

    kb = InlineKeyboardBuilder()
    if book["url"]:
        kb.button(text="⬇ تحميل PDF", url=book["url"])
    kb.button(text="🔙 الرجوع للكتب", callback_data=f"cat_{cat_key}")
    kb.button(text="🏠 القائمة الرئيسية", callback_data="main_menu")
    kb.adjust(1)

    await cq.message.edit_text(text, parse_mode="Markdown", reply_markup=kb.as_markup(), disable_web_page_preview=False)
