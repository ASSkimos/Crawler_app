import requests
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


def get_friends_vk(user_id, access_token):
    response = requests.get(
        f'https://api.vk.com/method/friends.get?user_id={user_id}&fields=nickname&access_token={access_token}&v=5.130')
    data = response.json()
    if "response" in data:
        return data["response"]["items"]
    else:
        return []


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
    if key in translations:
        return translations[key]
    else:
        return key


def format_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


class SocialMediaCrawler:
    def __init__(self, root):
        self.root = root
        self.root.title("Краулер")
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        ttk.Label(frame, text="Введите ID пользователя:").grid(row=1, column=0, sticky=tk.W)
        self.user_id_entry = ttk.Entry(frame, width=30)
        self.user_id_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))
        ttk.Label(frame, text="Введите токен доступа:").grid(row=2, column=0, sticky=tk.W)
        self.access_token_entry = ttk.Entry(frame, width=50)
        self.access_token_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))
        self.crawl_button = ttk.Button(frame, text="Поиск", command=self.crawl)
        self.crawl_button.grid(row=3, column=0, columnspan=2, pady=10)
        self.result_text = tk.Text(frame, width=50, height=15, wrap="word")
        self.result_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)
        self.bind_paste(self.user_id_entry)
        self.bind_paste(self.access_token_entry)
        self.bind_paste(self.result_text)

    def bind_paste(self, widget):
        if isinstance(widget, tk.Text) or isinstance(widget, ttk.Entry):
            widget.bind("<Control-v>", self.paste)

    def paste(self, event):
        try:
            widget = event.widget
            clipboard_text = self.root.clipboard_get()
            widget.delete(0, tk.END) if isinstance(widget, ttk.Entry) else widget.delete(1.0, tk.END)
            widget.insert(tk.INSERT, clipboard_text)
            return "break"
        except tk.TclError:
            pass

    def crawl(self):
        user_id = self.user_id_entry.get()
        access_token = self.access_token_entry.get()

        if not user_id or not access_token:
            messagebox.showerror("Ошибка ввода", "Пожалуйста, введите корректно ID пользователя и токен доступа")
            return
        data = self.crawl_vk(user_id, access_token)

        self.display_result(data)

    def crawl_vk(self, user_id, access_token):
        fields = "bdate,city,country,education,contacts,personal,connections,followers_count"
        response = requests.get(
            f'https://api.vk.com/method/users.get?user_ids={user_id}&fields={fields}&access_token={access_token}&v=5.130')
        data = response.json()
        if "response" in data:
            user_data = data["response"][0]
            friends_data = get_friends_vk(user_id, access_token)
            posts_data = self.get_posts_vk(user_id, access_token)
            user_data['friends'] = friends_data
            user_data['posts'] = posts_data
            return user_data
        else:
            return data

    def get_posts_vk(self, user_id, access_token):
        response = requests.get(
            f'https://api.vk.com/method/wall.get?owner_id={user_id}&access_token={access_token}&v=5.130')
        data = response.json()
        if "response" in data:
            return data["response"]["items"]
        else:
            return []

    def format_data(self, data):
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
        if 'connections' in data:
            connections = data['connections']
            formatted_data.append("Связи:")
            for connection in connections.values():
                formatted_data.append(f"{translate_to_russian(connection['title'])}: {connection['count']}")
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

    def display_result(self, data):
        self.result_text.delete(1.0, tk.END)
        if isinstance(data, dict):
            formatted_data = self.format_data(data)
            self.result_text.insert(tk.END, formatted_data)
        else:
            self.result_text.insert(tk.END, "Ошибка: " + str(data))


if __name__ == "__main__":
    root = tk.Tk()
    app = SocialMediaCrawler(root)
    root.mainloop()