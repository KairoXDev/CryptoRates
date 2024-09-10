import requests  # Импортируем модуль requests для выполнения HTTP-запросов
from tkinter import *  # Импортируем все из модуля tkinter для создания графического интерфейса
from tkinter import messagebox as mb  # Импортируем модуль для всплывающих сообщений
from tkinter import ttk  # Импортируем ttk из tkinter для расширенных виджетов
from ttkthemes import ThemedStyle  # Импортируем ThemedStyle из ttkthemes


# Функция для обновления метки с названием выбранной криптовалюты
def update_crypto_label(event):
    code = crypto_combobox.get()  # Получаем выбранную криптовалюту из выпадающего списка
    crypto_label.config(text=code)  # Обновляем метку для отображения названия выбранной криптовалюты

# Функция для получения и отображения курса выбранной криптовалюты относительно выбранной валюты
def get_crypto_rate():
    crypto_code = crypto_combobox.get()  # Получаем код выбранной криптовалюты из выпадающего списка
    currency_code = currency_combobox.get()  # Получаем код выбранной валюты из выпадающего списка
    if crypto_code and currency_code:  # Проверяем, выбраны ли криптовалюта и валюта
        try:
            # Отправляем запрос к CoinGecko API для получения курса криптовалюты к выбранной валюте
            crypto_response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_code}&vs_currencies={currency_code}")
            crypto_response.raise_for_status()  # Проверяем, успешен ли запрос
            crypto_data = crypto_response.json()  # Преобразуем ответ в JSON формат

            if currency_code in crypto_data[crypto_code]:  # Проверяем, есть ли данные по курсу к выбранной валюте
                crypto_rate = crypto_data[crypto_code][currency_code]  # Извлекаем курс криптовалюты к выбранной валюте
                # Обновляем метку для отображения результата
                result_label.config(text=f"Курс {crypto_code.capitalize()} к {currency_code.upper()}: {crypto_rate:.2f} {currency_code.upper()}")
            else:
                mb.showerror("Ошибка","Курс к выбранной валюте не найден!")  # Если данные не найдены, показываем сообщение об ошибке
        except Exception as e:
            mb.showerror("Ошибка", f"Произошла ошибка: {e}")  # Если произошла ошибка, показываем сообщение об ошибке
    else:
        mb.showwarning("Внимание!","Выберите криптовалюту и валюту!")  # Если криптовалюта или валюта не выбраны, показываем предупреждение

# Список популярных криптовалют для выбора
crypto_list = ['bitcoin', 'ethereum', 'ripple', 'litecoin', 'cardano']

# Список доступных валют для выбора
currency_list = ['usd', 'eur', 'rub', 'aed', 'cny', 'jpy']

# Создаем главное окно приложения
window = Tk()
window.title("Курс криптовалют к валютам")  # Устанавливаем заголовок окна
window.geometry("400x400")  # Задаем размеры окна

# Применяем стиль (тему) из ttkthemes
style = ThemedStyle(window)
style.set_theme('breeze')  # Можно выбрать любую доступную тему (arc, breeze, black, clearlooks, elegance, keramik, plastik, radiance, scidblue, scidgreen, scidpurple, scidred, scidyellow, tcl, winnative, xpnative)


# Метка с текстом "Выберите криптовалюту"
Label(text="Выберите криптовалюту").pack(padx=10, pady=10)

# Выпадающий список для выбора криптовалюты
crypto_combobox = ttk.Combobox(values=crypto_list)  # Создаем выпадающий список со значениями криптовалют
crypto_combobox.pack(padx=10, pady=10)  # Размещаем выпадающий список на окне
crypto_combobox.bind("<<ComboboxSelected>>", update_crypto_label)  # Привязываем функцию обновления метки при выборе криптовалюты

# Метка для отображения названия выбранной криптовалюты
crypto_label = ttk.Label()

# Метка с текстом "Выберите валюту"
Label(text="Выберите валюту").pack(padx=10, pady=10)


# Выпадающий список для выбора валюты
currency_combobox = ttk.Combobox(values=currency_list)  # Создаем выпадающий список со значениями валют
currency_combobox.pack(padx=10, pady=10)  # Размещаем выпадающий список на окне

# Кнопка для получения курса выбранной криптовалюты к выбранной валюте
Button(text="Получить курс", command=get_crypto_rate).pack(padx=10, pady=40)  # Кнопка запускает запрос на получение курса


# Метка для отображения результата - курс криптовалюты к выбранной валюте
result_label = ttk.Label()  # Создаем метку для вывода результата
result_label.configure(font=("Courier", 12, "normal"))   # Изменяем шрифт, размер и стиль
result_label.pack(padx=10, pady=20)  # Размещаем метку на окне с отступами

window.mainloop()  # Запускаем главный цикл приложения
