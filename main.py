import aiohttp
import asyncio
# from bot import app
from slugify import slugify
from datetime import datetime
# from database.hotstar import get_user_preferences

API_URL = "https://api.hotstar.com/o/v1/show/detail?contentId={show_id}" 
SERIAL_URLS = [
    "https://www.hotstar.com/in/shows/ghum-hai-kisikey/1260043179",
    "https://www.hotstar.com/in/shows/anupama/1260022017",
    "https://www.hotstar.com/in/tv/chashni/1260132522",
    "https://www.hotstar.com/in/tv/teri-meri-doriyaann/1260127842",
    "https://www.hotstar.com/in/tv/faltu/1260121083",
    "https://www.hotstar.com/in/tv/pandya-store/1260053090",
    "https://www.hotstar.com/in/tv/imlie/1260048110",
    "https://www.hotstar.com/in/tv/yeh-hai-chahatein/1260015192",
    "https://www.hotstar.com/in/tv/yeh-rishta/586",
    "https://www.hotstar.com/in/tv/meri-saas-bhoot-hai/1260128800",
    "https://www.hotstar.com/in/tv/dheere-dheere-se/1260125771",
    "https://www.hotstar.com/in/tv/ajooni/1260108191",
    "https://www.hotstar.com/in/tv/na-umra-ki-seema-ho/1260108189",
    "https://www.hotstar.com/in/tv/woh-to-hai-albelaa/1260087189",
    "https://www.hotstar.com/in/tv/titlie/1260142842",
    "https://www.hotstar.com/in/tv/do-dil/1260143176",
]

notified_episodes = set()

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0', 'Accept': '*/*', 'Accept-Language': 'eng', 'Accept-Encoding': 'gzip, deflate, br', 'Referer': 'https://www.hotstar.com/', 'x-country-code': 'IN', 'x-platform-code': 'PCTV', 'x-client-code': 'LR', 'hotstarauth': 'st=1669222094~exp=1669228094~acl=/*~hmac=47eefd6950b2da45cfddeaba7db97cf32767ab1fa60cf17a96546a021c00909b', 'x-hs-usertoken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ1bV9hY2Nlc3MiLCJleHAiOjE2Njk2MzY0NzMsImlhdCI6MTY2OTAzMTY3MywiaXNzIjoiVFMiLCJqdGkiOiIwYTkwYThlMGNmODE0YWQ1OWU5ODU4NzYzZjExYWNlZiIsInN1YiI6IntcImhJZFwiOlwiODk2MTU0NDVmZmVkNDVlM2FiYzY4NjFiZWIxMjAxZWZcIixcInBJZFwiOlwiMzQwNDBhN2E4MmRmNDJmN2EzM2MxMTBmZmM5ZjIyMmFcIixcIm5hbWVcIjpcIkd1ZXN0IFVzZXJcIixcImlwXCI6XCIxMTAuNDQuMTAuMjA0XCIsXCJjb3VudHJ5Q29kZVwiOlwiaW5cIixcImN1c3RvbWVyVHlwZVwiOlwibnVcIixcInR5cGVcIjpcImd1ZXN0XCIsXCJpc0VtYWlsVmVyaWZpZWRcIjpmYWxzZSxcImlzUGhvbmVWZXJpZmllZFwiOmZhbHNlLFwiZGV2aWNlSWRcIjpcIjg3M2ZkOGFjLWI2MzctNDAyNy04ZjMwLTc1NTZkMjhhZGMyMFwiLFwicHJvZmlsZVwiOlwiQURVTFRcIixcInZlcnNpb25cIjpcInYyXCIsXCJzdWJzY3JpcHRpb25zXCI6e1wiaW5cIjp7fX0sXCJpc3N1ZWRBdFwiOjE2NjkwMzE2NzM0MjN9IiwidmVyc2lvbiI6IjFfMCJ9.9WzjEvitAecX2qOct9gvSM-T7mimFymo3b-D7_C2_pM', 'Origin': 'https://www.hotstar.com', 'Connection': 'keep-alive', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-site', 'Sec-GPC': '1', 'TE': 'trailers'}



async def fetch_data_aiohttp(url, headers):
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()

    except aiohttp.ClientError as e:
        print(f"An error occurred with aiohttp: {e}")
        return None

async def get_msg(changed_content):
    if not changed_content:
        return None

    title = changed_content.get('title', '')
    show_name = slugify(changed_content.get("showName", ''))
    show = changed_content.get('showName', '')
    season_no = changed_content.get('seasonNo', '')
    episode_no = changed_content.get('episodeNo', '')
    language = get_language(changed_content.get('lang', []))
    release_date = get_formatted_date(changed_content.get("broadCastDate", ''))
    content_id = changed_content.get('contentId', '')
    show_content_id = changed_content.get('showContentId', '')

    episode_url = f"https://www.hotstar.com/in/tv/{show_name}/{show_content_id}/{content_id}"
    image_url = f"https://img1.hotstarext.com/image/upload/{changed_content.get('images', {}).get('h', '')}"

    msg = (
        "#NewEpisode #Hotstar #DSBots\n\n"
        f"**Series Name:** {show}\n"
        f"**Season Number:** {season_no}\n"
        f"**Episode Number:** {episode_no}\n"
        f"**Episode Name:** {title}\n"
        f"**Languages:** {language}\n"
        f"**Release Date:** {release_date}\n\n"
        f"**Link:** `{episode_url}`"
    )
    return msg, image_url, episode_url, language


def get_language(lang):
    language_mapping = {
        'Hindi': "Hindi",
        'Bengali': "Bengali",
        'Marathi': "Marathi",
        'Kannada': "Kannada",
        'Tamil': "Tamil",
        'Telugu': "Telugu",
    }
    return language_mapping.get(lang[0], lang[0]) if lang else ''


def get_formatted_date(broadcast_date):
    try:
        if isinstance(broadcast_date, int):
            # If broadcast_date is an integer, convert it to a string
            broadcast_date = str(broadcast_date)

        if broadcast_date.isdigit() and len(broadcast_date) == 10:
            # If the string is a 10-digit integer, assume it's a Unix timestamp
            date_object = datetime.utcfromtimestamp(int(broadcast_date))
        else:
            # Otherwise, assume it's a regular date string
            date_object = datetime.strptime(broadcast_date, "%Y-%m-%d")

        return date_object.strftime("%d-%m-%Y")
    except (ValueError, TypeError):
        return ''

# async def send_message_to_telegram(msg, image_url, language):
#     print(image_url)
#     print(language)
#     matching_users = [user for user, languages in get_user_preferences().items() if language in languages]
#     # matching_users = [1125671241,]
#     for user in matching_users:
#         try:
#             await app.send_photo(chat_id=user, photo=image_url, caption=msg)
#         except Exception as e:
#             # Log the error (you can customize this based on your logging system)
#             print(f"Error sending message to user {user}: {e}")
#             # Optionally, you can continue to the next user or take other actions as needed
#             continue

# from helpers.send_notification import get_ott_language_users
# async def send_message_to_users(caption, language, image_url):
#     ott = "hotstar"
#     matching_users = get_ott_language_users(language, ott)
#     for user in matching_users:
#         try:
#             await app.send_photo(chat_id=user, photo=image_url, caption=caption)
#         except Exception as e:
#             print(f"Error sending message to user {user}: {e}")


async def process_results(results):
    for result in results:
        if result is not None:
            try:
                res = result["body"]["results"]['trays']["items"][0]["assets"]["items"][0]
            except KeyError:
                pass
                res = result["body"]["results"]["trays"]["items"][1]["assets"]["items"][0]

            msg, image_url, serial_url, language = await get_msg(res)
            if serial_url not in notified_episodes:
                print(image_url)
                print(msg)
                # await send_message_to_users(msg, language, image_url)
                notified_episodes.add(serial_url)

async def process_results_temp(results):
    for result in results:
        if result is not None:
            try:
                res = result["body"]["results"]['trays']["items"][0]["assets"]["items"][0]
            except KeyError:
                pass
                res = result["body"]["results"]["trays"]["items"][1]["assets"]["items"][0]

            msg, image_url, serial_url, language = await get_msg(res)
            if serial_url not in notified_episodes:
                notified_episodes.add(serial_url)

async def hotstar_notification_temp():
    tasks = []

    for SERIAL_URL in SERIAL_URLS:
        show_id = SERIAL_URL.split("/")[-1]
        url = API_URL.format(show_id=show_id)
        tasks.append(fetch_data_aiohttp(url, HEADERS))

    results = await asyncio.gather(*tasks)
    print(results)
    await process_results_temp(results)


async def hotstar_notification():
    while True:
        tasks = []

        for SERIAL_URL in SERIAL_URLS:
            show_id = SERIAL_URL.split("/")[-1]
            url = API_URL.format(show_id=show_id)
            tasks.append(fetch_data_aiohttp(url, HEADERS))

        results = await asyncio.gather(*tasks)
        await process_results(results)
        await asyncio.sleep(3)
        print("sleep")

if __name__ == "__main__":
    asyncio.run(hotstar_notification_temp())
