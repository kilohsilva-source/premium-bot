from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler
)

TOKEN = "8787667902:AAHWx19NOx6ZJkLi1mpq57Hyn_mF2dRXMJM"

ADMIN_ID = 7355302122

MPESA_NUMBER = "0113433559"

VIP_LINK = "https://t.me/+Wce4AehbI9A4YjM8"


# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["📅 Daily"],
        ["📆 Weekly"],
        ["🗓 Monthly"],
        ["👑 Yearly"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    text = f"""
🔥 VIP ACCESS PLANS 🔥

📅 Daily - KES 50
📆 Weekly - KES 200
🗓 Monthly - KES 500
👑 Yearly - KES 1500

💰 Pay via M-PESA:
{MPESA_NUMBER}

📸 After payment:
Send screenshot here.
"""

    await update.message.reply_text(
        text=text,
        reply_markup=reply_markup
    )


# HANDLE SCREENSHOT
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user

    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Approve",
                callback_data=f"approve_{user.id}"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    caption = (
        f"💰 NEW PAYMENT SCREENSHOT\n\n"
        f"👤 Username: @{user.username}\n"
        f"🆔 ID: {user.id}\n"
        f"📛 Name: {user.first_name}"
    )

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=caption,
        reply_markup=reply_markup
    )

    await update.message.reply_text(
        "✅ Screenshot received.\nPlease wait for approval."
    )


# APPROVE BUTTON
async def approve_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("approve_"):

        user_id = int(data.split("_")[1])

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "✅ Payment confirmed!\n\n"
                f"Join VIP group:\n{VIP_LINK}"
            )
        )

        await query.edit_message_caption(
            caption=query.message.caption + "\n\n✅ APPROVED"
        )


# MAIN
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            handle_photo
        )
    )

    app.add_handler(
        CallbackQueryHandler(approve_callback)
    )

    print("Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()