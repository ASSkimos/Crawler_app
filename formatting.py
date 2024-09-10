from datetime import datetime


def format_and_translate_data(data):
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

    def translate_to_russian(key):
        return translations.get(key, key)

    formatted_data = []

    if 'first_name' in data and 'last_name' in data:
        formatted_data.append(f"Имя: {data['first_name']} {data['last_name']}")
    if 'bdate' in data:
        formatted_data.append(f"Дата рождения: {data['bdate']}")
    if 'city' in data:
        formatted_data.append(f"Город: {data['city']['title']}")
    if 'country' in data:
        formatted_data.append(f"Страна: {data['country']['title']}")
    if 'education' in data:
        formatted_data.append(f"Образование: {data.get('university_name', 'Не указано')}")
    if 'contacts' in data:
        contacts = data['contacts']
        if 'mobile_phone' in contacts:
            formatted_data.append(f"Мобильный телефон: {contacts['mobile_phone']}")
        if 'home_phone' in contacts:
            formatted_data.append(f"Домашний телефон: {contacts['home_phone']}")
    if 'personal' in data:
        personal_info = data['personal']
        formatted_data.append("Пункты жизненной позиции:")
        for key, value in personal_info.items():
            formatted_data.append(f"{translate_to_russian(key)}: {value}")
    if 'friends' in data:
        friends = data['friends']
        formatted_data.append("Друзья:")
        for friend in friends:
            formatted_data.append(f"{friend['first_name']} {friend['last_name']} (ID: {friend['id']})")
    if 'followers_count' in data:
        formatted_data.append(f"Количество подписчиков: {data['followers_count']}")
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
