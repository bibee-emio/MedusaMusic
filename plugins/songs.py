import os
from funcs.download import Descargar
from pyrogram import Client as Medusa, filters
from pyrogram.types import Message
from pyrogram.errors.exceptions import MessageNotModified
from youtubesearchpython import VideosSearch


text = (
    '__I can\'t guess the song which in your mind.'
    ' So please be kind to specify the song name.__'
    '\n\nSyntax: ```/song <song name>```'
)

descargar = Descargar('downloads/')

@Medusa.on_message(
    filters.command(['song'],prefixes=['/', '!'])
    & (filters.group | filters.private)
    & ~ filters.edited)
async def song_dl(_, msg: Message):

    if len(msg.command) == 1:
        return await msg.reply(text=text, parse_mode='md')

    r_text = await msg.reply('Processing...')
    url = msg.text.split(None, 1)[1]
    url = extract_the_url(url=url)
    
    if url == 0:return await r_text.edit('I could not find that song. Try with another keywords...')

    await r_text.edit('Downloading...')

    ytinfo = descargar.get_song(url)

    if ytinfo == 0:
        await r_text.edit(f'Something Wrong\n\n☕️Take a Coffee and come again... :(')
        return

    try:
        await r_text.edit_text('Uploading...')
    except MessageNotModified:
        pass

    await msg.reply_audio(
            audio=f'downloads/{ytinfo.title.replace("/","|")}-{ytinfo.video_id}.mp3', 
            thumb='src/Medusa320px.png',
            duration=int(ytinfo.length),
            performer=str(ytinfo.author),
            title=f'{str(ytinfo.title)}',
            caption=f"<a href='{url}'>__{ytinfo.title}__</a>\n\n__Downloaded by @MedusaMousikibot__"
        )

    await r_text.delete()
    os.remove(f'downloads/{ytinfo.title.replace("/","|")}-{ytinfo.video_id}.mp3')



def extract_the_url(url: str):
    '''Extracting the youtube URL'''

    v = VideosSearch(url, limit=1)
    v_result = v.result()

    if not v_result['result']:
        return 0
    url = v_result['result'][0]['link']
    return url
