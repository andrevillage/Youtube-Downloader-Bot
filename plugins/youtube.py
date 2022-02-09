from datetime import datetime, timedelta
from pyrogram import Client, Filters, InlineKeyboardMarkup, InlineKeyboardButton
from bot import user_time
from config import youtube_next_fetch
from helper.ytdlfunc import extractYt, create_buttons
import wget
import os
from PIL import Image

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

ytregex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"


@Client.on_message(filters.regex(pattern=".*http.*"))
async def echo(bot, update):
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "banned":
                await bot.delete_messages(
                    chat_id=update.chat.id,
                    message_ids=update.message_id,
                    revoke=True
                )
                return
        except UserNotParticipant:
            await update.reply_text(
                text="**Botu yalnızca kanal aboneleri kullanabilir.**",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="Kanala Katıl", url=f"https://t.me/{update_channel}")]
                ])
            )
            return
        except Exception:
            await update.reply_text("Ters giden bir şey mi var. @thebans ile iletişime geçin")
            return
    if not await db.is_user_exist(update.chat.id):
        await db.add_user(update.chat.id)
    ban_status = await db.get_ban_status(update.chat.id)
    if ban_status['is_banned']:
        await update.reply_text(f"Sen yasaklısın dostum\n\nSebep: {ban_status['ban_reason']}")
        return
    await message.reply_chat_action("typing")
    try:
        title, thumbnail_url, formats = extractYt(url)

        now = datetime.now()
        user_time[message.chat.id] = now + \
                                     timedelta(minutes=youtube_next_fetch)

    except Exception:
        await message.reply_text("`YouTube Verileri Alınamadı...\nYouTube IP Adresini Engellemiş Olabilir. \n#error`")
        return
    buttons = InlineKeyboardMarkup(list(create_buttons(formats)))
    sentm = await message.reply_text("🔎 YouTube Bağlantısı İşleniyor...")
    try:
        # Todo add webp image support in thumbnail by default not supported by pyrogram
        # https://www.youtube.com/watch?v=lTTajzrSkCw
        img = wget.download(thumbnail_url)
        im = Image.open(img).convert("RGB")
        output_directory = os.path.join(os.getcwd(), "downloads", str(message.chat.id))
        if not os.path.isdir(output_directory):
            os.makedirs(output_directory)
        thumb_image_path = f"{output_directory}.jpg"
        im.save(thumb_image_path,"jpeg")
        await message.reply_photo(thumb_image_path, caption=title, reply_markup=buttons)
        await sentm.delete()
    except Exception as e:
        print(e)
        try:
            thumbnail_url = "https://telegra.ph/file/ce37f8203e1903feed544.png"
            await message.reply_photo(thumbnail_url, caption=title, reply_markup=buttons)
        except Exception as e:
            await sentm.edit(
            f"<code>{e}</code> #Error")

