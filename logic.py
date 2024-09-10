import aiohttp
import asyncio
from datetime import datetime


async def get_friends_vk(user_id, access_token):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f'https://api.vk.com/method/friends.get?user_id={user_id}&fields=nickname&access_token={access_token}&v=5.130'
            ) as response:
                data = await response.json()
                if "response" in data:
                    return data["response"]["items"]
                else:
                    return []
        except Exception as e:
            print(f"Ошибка при получении друзей: {e}")
            return []


async def get_posts_vk(user_id, access_token):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f'https://api.vk.com/method/wall.get?owner_id={user_id}&access_token={access_token}&v=5.130'
            ) as response:
                data = await response.json()
                if "response" in data:
                    return data["response"]["items"]
                else:
                    return []
        except Exception as e:
            print(f"Ошибка при получении постов: {e}")
            return []


async def get_user_data_vk(user_id, access_token):
    fields = "bdate,city,country,education,contacts,personal,connections,followers_count"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f'https://api.vk.com/method/users.get?user_ids={user_id}&fields={fields}&access_token={access_token}&v=5.130'
            ) as response:
                data = await response.json()
                if "response" in data:
                    user_data = data["response"][0]
                    friends_data, posts_data = await asyncio.gather(
                        get_friends_vk(user_id, access_token),
                        get_posts_vk(user_id, access_token)
                    )
                    user_data['friends'] = friends_data
                    user_data['posts'] = posts_data
                    return user_data
                else:
                    return data
        except Exception as e:
            print(f"Ошибка при получении данных пользователя: {e}")
            return {"error": str(e)}


def translate_to_russian(key):
    translations = {
        "political": "Политические взгляды",
        "langs": "Языки",
        "inspired_by": "Вдохновляется",
        "people_main": "Главное в людях",
        "life_main": {
            "1": "Семья и дети",
            "2": "Карьера и деньги",
            "3": "Развлечения и отдых",
            "4": "Наука и исследования",
            "5": "Совершенствование мира",
            "6": "Саморазвитие",
            "7": "Красота и искусство",
            "8": "Слава и влияние"
        },
        "smoking": "Отношение к курению",
        "alcohol": {
            "0": "Негативное",
            "1": "Компромиссное",
            "2": "Нейтральное",
            "3": "Положительное"
        },
        "friends": "Друзья",
        "followers_count": "Количество подписчиков",
        "likes": "Лайки",
        "text": "Текст",
        "date": "Дата",
        "religion": "Религия",
        "religion_id": "Id религии",
        "langs_full": "Информация о религии"
    }
    return translations.get(key, key)


def format_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
