
import os
import logging
from telegram import Update, ReactionTypeEmoji
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters
)

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ["BOT_TOKEN"]
REACTION = "🔥"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "🤖 REO Auto Reaction Bot চালু!\n"
        "/status - Bot status\n"
        "/stats - সর্বশেষ পোস্টের তথ্য"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("✅ Bot is running.")


async def new_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = update.channel_post
    if not post:
        return

    context.application.bot_data["last_post"] = {
        "chat_id": post.chat_id,
        "message_id": post.message_id,
    }

    try:
        await context.bot.set_message_reaction(
            chat_id=post.chat_id,
            message_id=post.message_id,
            reaction=[ReactionTypeEmoji(REACTION)],
        )
        logging.info("Reaction added to post %s", post.message_id)
    except Exception:
        logging.exception("Could not add reaction")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = context.application.bot_data.get("last_post")
    if not post:
        await update.effective_message.reply_text(
            "এখনও কোনো নতুন চ্যানেল পোস্ট পাওয়া যায়নি।"
        )
        return

    await update.effective_message.reply_text(
        f"সর্বশেষ পোস্ট ID: {post['message_id']}\n"
        "Bot API দিয়ে সঠিক view count পড়া যায় না। "
        "চ্যানেলে পোস্টটি খুলে ভিউ দেখুন।"
    )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(
        MessageHandler(filters.UpdateType.CHANNEL_POST, new_post)
    )
    app.run_polling(allowed_updates=["message", "channel_post"])


if __name__ == "__main__":
    main()
