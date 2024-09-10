import asyncio
from datetime import datetime


async def fetch_data(session, url):
    try:
        async with session.get(url) as response:
            data = await response.json()
            return data.get("response", {})
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return {}


async def get_friends_vk(session, user_id, access_token):
    url = f'https://api.vk.com/method/friends.get?user_id={user_id}&fields=nickname&access_token={access_token}&v=5.130'
    response = await fetch_data(session, url)
    return response.get("items", [])


async def get_posts_vk(session, user_id, access_token):
    url = f'https://api.vk.com/method/wall.get?owner_id={user_id}&access_token={access_token}&v=5.130'
    response = await fetch_data(session, url)
    return response.get("items", [])


async def get_user_data_vk(session, user_id, access_token):
    fields = "bdate,city,country,education,contacts,personal,connections,followers_count"
    url = f'https://api.vk.com/method/users.get?user_ids={user_id}&fields={fields}&access_token={access_token}&v=5.130'

    user_data = await fetch_data(session, url)
    if user_data:
        user_data = user_data[0]  # Извлекаем данные пользователя из списка
        friends_data, posts_data = await asyncio.gather(
            get_friends_vk(session, user_id, access_token),
            get_posts_vk(session, user_id, access_token)
        )
        user_data['friends'] = friends_data
        user_data['posts'] = posts_data
        return user_data
    else:
        return {"error": "Не удалось получить данные пользователя"}


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