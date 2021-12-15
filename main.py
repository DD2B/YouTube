# By ~ @CVOOZ
# For and gives starts 🤍

import os
import asyncio
from urllib.parse import urlparse
from pyrogram.errors import UserNotParticipant, UserBannedInChannel
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from youtube_dl import YoutubeDL
from opencc import OpenCC
from config import Config
import wget

CVOOZ = Client(
   "Youtube Bot",
   api_id=Config.APP_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.TG_BOT_TOKEN,
)

YTDL_REGEX = (r"^((?:https?:)?\/\/)"
              r"?((?:www|m)\.)"
              r"?((?:youtube\.com|youtu\.be|xvideos\.com|pornhub\.com"
              r"|xhamster\.com|xnxx\.com))"
              r"(\/)([-a-zA-Z0-9()@:%_\+.~#?&//=]*)([\w\-]+)(\S+)?$")
s2tw = OpenCC('s2tw.json').convert


@CVOOZ.on_message(filters.command("start"))
async def start(client, message):
   if message.chat.type == 'private':
       await CVOOZ.send_message(
               chat_id=message.chat.id,
               text="""<b>أهلا بك عزيزي،

من خلال هذا البوت يمكنك تحميل الاغاني والفيديوهات من اليوتيوب اضغط على الخيارات بالأسفل لمزيد من المعلومات 
• BY : @CVOOZ
</b>""",   
                            reply_markup=InlineKeyboardMarkup(
                                [
                                [
                                        InlineKeyboardButton('قائمة المساعدة', callback_data="help"),
                                        InlineKeyboardButton('▷ DEV', url='https://T.ME/CVOOZ')
                                    ],]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")

@CVOOZ.on_message(filters.command("help"))
async def help(client, message):
    if message.chat.type == 'private':   
        await RR7PP.send_message(
               chat_id=message.chat.id,
               text="""<b><u>بوت اليوتيوب</u></b>

فقط ارسل رابط الفيديو او الاغنية لتحميلها وارسالها لك

<b>• DEV :</b> @CVOOZ""",
        reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            " رجـوع", callback_data="start"),
                                        InlineKeyboardButton(
                                            "حـول البـوت", callback_data="about"),
                                  ],]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")

@CVOOZ.on_message(filters.command("about"))
async def about(client, message):
    if message.chat.type == 'private':   
        await CVOOZ.send_message(
               chat_id=message.chat.id,
               text="""<b><u>YOUTUBE BOT INFO</u></b>

<b>• ‍🔧 المطور:</b> <a href="https://t.me/CVOOZ">اضغط هنا</a>

<b>• 📚 المكتبة:</b> <a href="https://github.com/pyrogram/pyrogram">Pyrogram</a>

<b>• 📢 قناة السورس:</b> @JAIITHON

<b>• 🌀 ملفات السورس:</b> <a href="https://github.com/xrzo/Youtube">اضغط هنا</a>""",
     reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "🔙 رجـوع", callback_data="help"),
                                        InlineKeyboardButton(
                                            "المطـور ⛓️️", url="https://t.me/XRZOC"),
                                  ],]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")


# https://docs.pyrogram.org/start/examples/bot_keyboards
# Reply with inline keyboard
@CVOOZ.on_message(filters.private
                   & filters.text
                   & ~filters.edited
                   & filters.regex(YTDL_REGEX))
async def ytdl_with_button(c: Client, message: Message):
    if Config.UPDATES_CHANNEL is not None:
        try:
            user = await c.get_chat_member(Config.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await c.send_message(
                    chat_id=message.chat.id,
                    text="▾∮ تم حظرك من استخدام البوت تواصل مع مطوري [اضغط هنا](https://t.me/CVOOZ).",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await c.send_message(
                chat_id=message.chat.id,
                text="**▾∮ يجب الاشتراك بقناة السورس اولا **",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("قناة السورس", url=f"https://t.me/JAIITHON")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await c.send_message(
                chat_id=message.chat.id,
                text="هنالك شي خطا تواصل مع مطوري [اضغط هنة](https://t.me/CVOOZ).",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    await message.reply_text(
        "**▾∮ اختر احد الصيغ للتحميل **",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🎵 اغنيـة",
                        callback_data="ytdl_audio"
                    ),
                    InlineKeyboardButton(
                        "فـيديو 🎬",
                        callback_data="ytdl_video"
                    )
                ]
            ]
        ),
        quote=True
    )


@CVOOZ.on_callback_query(filters.regex("^ytdl_audio$"))
async def callback_query_ytdl_audio(_, callback_query):
    try:
        url = callback_query.message.reply_to_message.text
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': '%(title)s - %(extractor)s-%(id)s.%(ext)s',
            'writethumbnail': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            message = callback_query.message
            await message.reply_chat_action("typing")
            info_dict = ydl.extract_info(url, download=False)
            # download
            await callback_query.edit_message_text("**▾∮ يتم تحميل الاغنية..**")
            ydl.process_info(info_dict)
            # upload
            audio_file = ydl.prepare_filename(info_dict)
            task = asyncio.create_task(send_audio(message, info_dict,
                                                  audio_file))
            while not task.done():
                await asyncio.sleep(3)
                await message.reply_chat_action("upload_document")
            await message.reply_chat_action("cancel")
            await message.delete()
    except Exception as e:
        await message.reply_text(e)
    await callback_query.message.reply_to_message.delete()
    await callback_query.message.delete()


if Config.AUDIO_THUMBNAIL == "No":
   async def send_audio(message: Message, info_dict, audio_file):
       basename = audio_file.rsplit(".", 1)[-2]
       # .webm -> .weba
       if info_dict['ext'] == 'webm':
           audio_file_weba = basename + ".weba"
           os.rename(audio_file, audio_file_weba)
           audio_file = audio_file_weba
       # thumbnail
       thumbnail_url = info_dict['thumbnail']
       thumbnail_file = basename + "." + \
           get_file_extension_from_url(thumbnail_url)
       # info (s2tw)
       webpage_url = info_dict['webpage_url']
       title = s2tw(info_dict['title'])
       caption = f"<b><a href=\"{webpage_url}\">{title}</a></b>"
       duration = int(float(info_dict['duration']))
       performer = s2tw(info_dict['uploader'])
       await message.reply_audio(audio_file, caption=caption, duration=duration,
                              performer=performer, title=title,
                              parse_mode='HTML', thumb=thumbnail_file)
       os.remove(audio_file)
       os.remove(thumbnail_file)

else:
    async def send_audio(message: Message, info_dict, audio_file):
       basename = audio_file.rsplit(".", 1)[-2]
       # .webm -> .weba
       if info_dict['ext'] == 'webm':
           audio_file_weba = basename + ".weba"
           os.rename(audio_file, audio_file_weba)
           audio_file = audio_file_weba
       # thumbnail
       lol = Config.AUDIO_THUMBNAIL
       thumbnail_file = wget.download(lol)
       # info (s2tw)
       webpage_url = info_dict['webpage_url']
       title = s2tw(info_dict['title'])
       caption = f"<b><a href=\"{webpage_url}\">{title}</a></b>"
       duration = int(float(info_dict['duration']))
       performer = s2tw(info_dict['uploader'])
       await message.reply_audio(audio_file, caption=caption, duration=duration,
                              performer=performer, title=title,
                              parse_mode='HTML', thumb=thumbnail_file)
       os.remove(audio_file)
       os.remove(thumbnail_file)

@CVOOZ.on_callback_query(filters.regex("^ytdl_video$"))
async def callback_query_ytdl_video(_, callback_query):
    try:
        # url = callback_query.message.text
        url = callback_query.message.reply_to_message.text
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': '%(title)s - %(extractor)s-%(id)s.%(ext)s',
            'writethumbnail': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            message = callback_query.message
            await message.reply_chat_action("typing")
            info_dict = ydl.extract_info(url, download=False)
            # download
            await callback_query.edit_message_text("**▾∮ يتم تحميل الفيديو...**")
            ydl.process_info(info_dict)
            # upload
            video_file = ydl.prepare_filename(info_dict)
            task = asyncio.create_task(send_video(message, info_dict,
                                                  video_file))
            while not task.done():
                await asyncio.sleep(3)
                await message.reply_chat_action("upload_document")
            await message.reply_chat_action("cancel")
            await message.delete()
    except Exception as e:
        await message.reply_text(e)
    await callback_query.message.reply_to_message.delete()
    await callback_query.message.delete()

if Config.VIDEO_THUMBNAIL == "No":
   async def send_video(message: Message, info_dict, video_file):
      basename = video_file.rsplit(".", 1)[-2]
      # thumbnail
      thumbnail_url = info_dict['thumbnail']
      thumbnail_file = basename + "." + \
          get_file_extension_from_url(thumbnail_url)
      # info (s2tw)
      webpage_url = info_dict['webpage_url']
      title = s2tw(info_dict['title'])
      caption = f"<b><a href=\"{webpage_url}\">{title}</a></b>"
      duration = int(float(info_dict['duration']))
      width, height = get_resolution(info_dict)
      await message.reply_video(
          video_file, caption=caption, duration=duration,
          width=width, height=height, parse_mode='HTML',
          thumb=thumbnail_file)

      os.remove(video_file)
      os.remove(thumbnail_file)

else:
   async def send_video(message: Message, info_dict, video_file):
      basename = video_file.rsplit(".", 1)[-2]
      # thumbnail
      lel = Config.VIDEO_THUMBNAIL
      thumbnail_file = wget.download(lel)
      # info (s2tw)
      webpage_url = info_dict['webpage_url']
      title = s2tw(info_dict['title'])
      caption = f"<b><a href=\"{webpage_url}\">{title}</a></b>"
      duration = int(float(info_dict['duration']))
      width, height = get_resolution(info_dict)
      await message.reply_video(
          video_file, caption=caption, duration=duration,
          width=width, height=height, parse_mode='HTML',
          thumb=thumbnail_file)

      os.remove(video_file)
      os.remove(thumbnail_file)

def get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]


def get_resolution(info_dict):
    if {"width", "height"} <= info_dict.keys():
        width = int(info_dict['width'])
        height = int(info_dict['height'])
    # https://support.google.com/youtube/answer/6375112
    elif info_dict['height'] == 1080:
        width = 1920
        height = 1080
    elif info_dict['height'] == 720:
        width = 1280
        height = 720
    elif info_dict['height'] == 480:
        width = 854
        height = 480
    elif info_dict['height'] == 360:
        width = 640
        height = 360
    elif info_dict['height'] == 240:
        width = 426
        height = 240
    return (width, height)


@CVOOZ.on_callback_query()
async def button(bot, update):
      cb_data = update.data
      if "help" in cb_data:
        await update.message.delete()
        await help(bot, update.message)
      elif "about" in cb_data:
        await update.message.delete()
        await about(bot, update.message)
      elif "start" in cb_data:
        await update.message.delete()
        await start(bot, update.message)

print(
    """
اشتغل البوت بنجاح ✅
اشترك @JAIITHON
"""
)

CVOOZ.run()
