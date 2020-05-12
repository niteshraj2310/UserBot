from requests import get, post, exceptions
import asyncio
import os
from datetime import datetime
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, LOGS, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register


def progress(current, total):
    logger.info("Downloaded {} of {}\nCompleted {}".format(current, total, (current / total) * 100))


@register(outgoing=True, pattern=r"^.npaste(?: |$)([\s\S]*)")
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    downloaded_file_name = None
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.paste <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await bot.download_media(
                previous_message,
                TEMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8")
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.paste <long text to include>`"
    py_file =  ""
    if downloaded_file_name.endswith(".py"):
        py_file += ".py"
        data = message
        key = requests.post('https://nekobin.com/api/documents', json={"content": data}).json().get('result').get('key')
        url = f'https://nekobin.com/{key}{py_file}'
        reply_text = f'Nekofied to *Nekobin* : {url}'
        await event.edit(reply_text)
    else:
        data = message
        key = requests.post('https://nekobin.com/api/documents', json={"content": data}).json().get('result').get('key')
        url = f'https://nekobin.com/{key}'
        reply_text = f'Nekofied to *Nekobin* : {url}'
        await event.edit(reply_text)
