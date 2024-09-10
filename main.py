import asyncio
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import aiohttp
from logic import get_user_data_vk
import formatting


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

        self.save_button = ttk.Button(frame, text="Сохранить результат", command=self.save_result)
        self.save_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.result_text = tk.Text(frame, width=50, height=15, wrap="word")
        self.result_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)

    def crawl(self):
        user_id = self.user_id_entry.get()
        access_token = self.access_token_entry.get()

        if not user_id or not access_token:
            messagebox.showerror("Ошибка ввода", "Пожалуйста, введите корректно ID пользователя и токен доступа")
            return

        # Запуск асинхронного поиска данных в основном потоке
        asyncio.run(self.run_async_task(user_id, access_token))

    async def run_async_task(self, user_id, access_token):
        async with aiohttp.ClientSession() as session:
            data = await get_user_data_vk(session, user_id, access_token)
            self.display_result(data)

    def display_result(self, data):
        self.result_text.delete(1.0, tk.END)
        if isinstance(data, dict):
            formatted_data = formatting.format_and_translate_data(data)
            self.result_text.insert(tk.END, formatted_data)
        else:
            self.result_text.insert(tk.END, "Ошибка: " + str(data))

    def save_result(self):
        result = self.result_text.get(1.0, tk.END).strip()

        if not result:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(result)
            messagebox.showinfo("Успех", "Результат успешно сохранен!")


def main():
    root = tk.Tk()
    app = SocialMediaCrawler(root)
    root.mainloop()


if __name__ == "__main__":
    main()
