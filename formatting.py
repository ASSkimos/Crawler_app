from datetime import datetime

def format_and_translate_data(data):  # форматирование выходных данных
    translations = {
        "political": "Политические взгляды",
        "langs": "Языки",
        "inspired_by": "Вдохновляется",
        "people_main": "Главное в людях",
        "life_main": "Главное в жизни",
        "smoking": "Отношение к курению",
        "alcohol": "Отношение к алкоголю",
        "friends": "Друзья",
        "followers_count": "Количество подписчиков",
        "likes": "Лайки",
        "text": "Текст",
        "date": "Дата",
        "religion": "Религия",
        "religion_id": "Id религии",
        "langs_full": "Информация о религии"
    }

    value_translations = {
        "political": {
            "1": "Коммунистические",
            "2": "Социалистические",
            "3": "Умеренные",
            "4": "Либеральные",
            "5": "Консервативные",
            "6": "Монархические",
            "7": "Ультраконсервативные",
            "8": "Индифферентные",
            "9": "Либертарианские"
        },
        "people_main": {
            "1": "Ум и креативность",
            "2": "Доброта и честность",
            "3": "Красота и здоровье",
            "4": "Власть и богатство",
            "5": "Смелость и упорство",
            "6": "Юмор и жизнелюбие"
        },
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
        "smoking": {
            "0": "Негативное",
            "1": "Компромиссное",
            "2": "Нейтральное",
            "3": "Положительное",
            "4": "Резко негативное"
        },
        "alcohol": {
            "0": "Негативное",
            "1": "Компромиссное",
            "2": "Нейтральное",
            "3": "Положительное"
        }
    }

    def translate_to_russian(key):
        return translations.get(key, key)

    def translate_value(key, value):
        if key in value_translations:
            return value_translations.get(key, {}).get(str(value), value)
        return value

    formatted_data = []

    if 'first_name' in data and 'last_name' in data:
        formatted_data.append(f"Имя: {data['first_name']} {data['last_name']}")
    if 'bdate' in data:
        formatted_data.append(f"Дата рождения: {data['bdate']}")
    if 'city' in data:
        formatted_data.append(f"Город: {data['city']['title']}")
    if 'country' in data:
        formatted_data.append(f"Страна: {data['country']['title']}")

    # Образование
    if 'education' in data:
        university = data.get('university_name', 'Не указано')
        faculty = data.get('faculty_name', 'Не указано')
        graduation = data.get('graduation', 'Не указано')
        formatted_data.append(f"Образование: {university}, Факультет: {faculty}, Год выпуска: {graduation}")

    if 'contacts' in data:
        contacts = data['contacts']
        if 'mobile_phone' in contacts:
            formatted_data.append(f"Мобильный телефон: {contacts['mobile_phone']}")
        if 'home_phone' in contacts:
            formatted_data.append(f"Домашний телефон: {contacts['home_phone']}")

    # Личная информация
    if 'personal' in data:
        personal_info = data['personal']
        formatted_data.append("Пункты жизненной позиции:")
        for key, value in personal_info.items():
            translated_value = translate_value(key, value)
            formatted_data.append(f"{translate_to_russian(key)}: {translated_value}")

    if 'friends' in data:
        friends = data['friends']
        formatted_data.append("Друзья:")
        for friend in friends:
            formatted_data.append(f"{friend['first_name']} {friend['last_name']} (ID: {friend['id']})")

    if 'followers_count' in data:
        formatted_data.append(f"Количество подписчиков: {data['followers_count']}")

    # Посты пользователя
    if 'posts' in data:
        posts = data['posts']
        formatted_data.append("Недавние публикации:")
        for post in posts:
            formatted_data.append(f"Текст: {post.get('text', 'Без текста')}")
            formatted_data.append(f"Дата: {format_date(post['date'])}")
            formatted_data.append(f"Лайки: {post['likes']['count']}")
            formatted_data.append("")

    return "\n".join(formatted_data)


def format_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
