import os
import time

import requests
from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from services import TGStatAPI, PostStats
from utils import my_types


bot = Bot(Config.BOT_TOKEN, parse_mode="html")
dp = Dispatcher(bot)

tg_api = TGStatAPI(Config.API_TOKEN)

CHANNEL = Config.SECRET_CHAT
CHANNELS = [
    "https://t.me/joinchat/AAAAAEW7PysA07Xr68XQgg",
    "https://t.me/joinchat/AAAAAEVZR6NQqIVytzIEJQ",
    "@nationaI_geographic",
    "@mir_animalsss",
    "@sobake_n",
    "https://t.me/zoomir_k",
    "https://t.me/tgvozduh",
    "@d_code",
    "@habr_com",
    "@exploitex",
    "@tproger_official",
    "@black_triangle_tg",
    "@open_source_friend",
    "@ru_travel_world",
    "https://tgstat.com/ru/channel/FdQuvptjsXczN2Zi",
    "https://tgstat.ru/channel/RjwWKhUW5awxNDky",
    "https://tgstat.ru/channel/AAAAAEKYU6LOmLtQtFlyiA",
    "https://t.me/koshki7",
    "https://tgstat.ru/channel/PjxSP7u7PUI0YzMy",
    "https://tgstat.ru/channel/@Nature",
    "https://t.me/TrendWatching24",
    "https://t.me/cyber_cab",
    "https://t.me/cyber_cab",
]


def orig_kb(link):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Original", url=link)
    )


async def on_startup(dp: Dispatcher):
    counter = 1
    for channel in CHANNELS:
        time.sleep(10)
        posts_data = []
        try:
            posts = tg_api.get_posts(channel)
        except:
            print(f"{counter}) {channel} is not found...")
            continue

        for post in posts:
            try:
                stats = tg_api.get_post_stats(post)
            except:
                print("Can't get post stats...")
                continue
            posts_data.append(my_types.APIPostData(post, stats))

        ps_frame = PostStats(posts_data)
        top_posts = ps_frame.get_best_posts()

        for post in top_posts:
            time.sleep(2)
            post_inf = post.post
            post_id = post_inf["id"]

            text = post_inf["text"]
            try:
                media_type = post_inf["media"]["media_type"]
            except KeyError:
                media_type = None
            link_to_dw_media = post_inf["media"]["file_url"]
            if link_to_dw_media == None:
                link_to_dw_media = post_inf["media"]["file_thumbnail_url"]
                media_type = "mediaPhoto"
                if link_to_dw_media == None:
                    media_type = None
            
            bot = dp.bot

            if not media_type:
                await bot.send_message(CHANNEL, text=text)

            if media_type == "mediaDocument":
                r = requests.get(link_to_dw_media, stream=True)
                with open(f"{post_id}.mp4", "wb") as file:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                            file.flush()

                video = open(f"{post_id}.mp4", "rb")
                await bot.send_video(CHANNEL, video, caption=text)
                os.remove(f"{post_id}.mp4")
                
            if media_type == "mediaPhoto":
                r = requests.get(link_to_dw_media, stream=True)
                with open(f"{post_id}.jpg", "wb") as file:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                            file.flush()
                photo = open(f"{post_id}.jpg", "rb")
                await bot.send_photo(CHANNEL, photo, caption=text)
                os.remove(f"{post_id}.jpg")
        
        print(f"{counter}/{len(CHANNELS)} done!")
        counter += 1


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)

