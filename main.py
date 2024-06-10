from flask import Flask,render_template
from threading import Thread

import telebot
import random
import datetime
import requests
import os

from telebot import types
from bs4 import BeautifulSoup

bot_token = token=os.environ.get('token')
weather_api = 'c504a5e558cf4816ec8efa2fc962a225'
EUR_UAH = 'https://minfin.com.ua/currency/eur/'
EUR_UAH_BANK = 'https://minfin.com.ua/currency/banks/eur/'
USD_UAH_BANK = 'https://minfin.com.ua/currency/banks/usd/'
BTC_USD = 'https://www.binance.com/ru/price/bitcoin'
ETH_USD = 'https://www.binance.com/ru/price/ethereum'
user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
                            ' AppleWebKit/537.36 (KHTML, like Gecko)'
                            ' Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100'}

bot = telebot.TeleBot(bot_token)

app = Flask(__name__)

@app.route('/')
def index():
  return "Alive"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t=Thread(target=run)
  t.start
  

@bot.message_handler(commands=['start'])
def start(message):
    mainMenu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)

    rndm = types.KeyboardButton('🔸 Случайные числа')
    wthr = types.KeyboardButton('☀️ Прогноз погоды')
    exchng = types.KeyboardButton('📊 Курсы валют')
    inf = types.KeyboardButton('📕 Информация')

    mainMenu.add(rndm, wthr, exchng, inf)

    hello = (f"Привет <b>{message.from_user.first_name} {message.from_user.last_name}</b>!\n"
             f"Это бот с <b>функциями случайных чисел, прогноза погоды, курсов валют и информацией</b>.")
    bot.send_message(message.chat.id, hello, parse_mode='html', reply_markup=mainMenu)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == '🔸 Случайные числа':
        rndmMenu = types.ReplyKeyboardMarkup(resize_keyboard=True)

        to10 = types.KeyboardButton('🔸 От 1 до 10')
        to100 = types.KeyboardButton('🔸 От 1 до 100')
        to1000 = types.KeyboardButton('🎲 Кинуть кубик')
        back = types.KeyboardButton('⬅️ Назад')

        rndmMenu.add(to10, to100, to1000, back)

        rndm_choise = "Выберите промежуток случайных чисел."
        bot.send_message(message.chat.id, rndm_choise, parse_mode='html', reply_markup=rndmMenu)
    elif message.text == '🔸 От 1 до 10':
        rndm10 = f"Ваше число: <u>{random.randint(1, 10)}</u>"
        bot.send_message(message.chat.id, rndm10, parse_mode='html')
    elif message.text == '🔸 От 1 до 100':
        rndm100 = f"Ваше число: <u>{random.randint(1, 100)}</u>"
        bot.send_message(message.chat.id, rndm100, parse_mode='html')
    elif message.text == '🎲 Кинуть кубик':
        bot.send_dice(message.chat.id)
    elif message.text == '☀️ Прогноз погоды':
        wthrMenu = types.ReplyKeyboardMarkup(resize_keyboard=True)

        back = types.KeyboardButton('⬅️ Назад')

        wthrMenu.add(back)
        wthr_req_text = f"Введите название местности, где вы хотите узнать погоду."
        wthr_req = bot.send_message(message.chat.id, wthr_req_text, parse_mode='html', reply_markup=wthrMenu)
        bot.register_next_step_handler(wthr_req, get_weather)
    elif message.text == '📊 Курсы валют':
        exchngMenu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)

        btnUSD = types.KeyboardButton('USD')
        btnEUR = types.KeyboardButton('EUR')
        btnBTC = types.KeyboardButton('BTC')
        btnETH = types.KeyboardButton('ETH')
        back = types.KeyboardButton('⬅️ Назад')

        exchngMenu.add(btnUSD, btnEUR, btnBTC, btnETH, back)

        exchng_choise = f"Выберите, курс какой валюты вы хотите узнать."
        bot.send_message(message.chat.id, exchng_choise, parse_mode='html', reply_markup=exchngMenu)
    elif message.text == 'USD':
        try:
            full_page_usd_bank = requests.get(USD_UAH_BANK, headers=user_agent)
            soup_usd_bank = BeautifulSoup(full_page_usd_bank.content, 'html.parser')
            convert_usd_bank = soup_usd_bank.findAll("td", {"class": "mfm-text-nowrap"})

            for div in soup_usd_bank.findAll("span", {"class": "mfm-hover-show mfm-table-trend icon-up-open"}):
                div.decompose()
            for div in soup_usd_bank.findAll("span", {"class": "mfm-hover-show mfm-table-trend icon-down-open"}):
                div.decompose()
            for div in soup_usd_bank.findAll("span", {"class": "mfm-text-light-grey mfm-posr"}):
                div.decompose()

            s_usd = convert_usd_bank[0].text.strip().split()

            exchng_usd = (f"---Курс доллара в банках---\n"
                          f"Покупка доллара: ₴ {s_usd[0]}\n"
                          f"Продажа доллара: ₴ {s_usd[1]}\n")
            bot.send_message(message.chat.id, exchng_usd, parse_mode='html')
        except:
            bot.send_message(message.chat.id, "Курс сейчас не доступен...", parse_mode='html')
    elif message.text == 'EUR':
        try:
            full_page_eur_bank = requests.get(EUR_UAH_BANK, headers=user_agent)
            soup_eur_bank = BeautifulSoup(full_page_eur_bank.content, 'html.parser')
            convert_eur_bank = soup_eur_bank.findAll("td", {"class": "mfm-text-nowrap"})

            for div in soup_eur_bank.findAll("span", {"class": "mfm-hover-show mfm-table-trend icon-up-open"}):
                div.decompose()
            for div in soup_eur_bank.findAll("span", {"class": "mfm-hover-show mfm-table-trend icon-down-open"}):
                div.decompose()
            for div in soup_eur_bank.findAll("span", {"class": "mfm-text-light-grey mfm-posr"}):
                div.decompose()

            s_eur = convert_eur_bank[0].text.strip().split()

            exchng_eur = (f"---Курс евро в банках---\n"
                          f"Покупка евро: ₴ {s_eur[0]}\n"
                          f"Продажа евро: ₴ {s_eur[1]}\n")
            bot.send_message(message.chat.id, exchng_eur, parse_mode='html')
        except:
            bot.send_message(message.chat.id, "Курс сейчас не доступен...", parse_mode='html')
    elif message.text == 'BTC':
        try:
            full_page_btc = requests.get(BTC_USD)
            soup_btc = BeautifulSoup(full_page_btc.content, 'html.parser')
            convert_btc = soup_btc.findAll(name="div", attrs="css-1bwgsh3")
            final_btc = convert_btc[0].text

            exchng_btc = (f"---Курс Биткоина---\n"
                          f"Ценна Биткоина: {final_btc}\n")
            bot.send_message(message.chat.id, exchng_btc, parse_mode='html')
        except:
            bot.send_message(message.chat.id, "Курс сейчас не доступен...", parse_mode='html')
    elif message.text == 'ETH':
        try:
            full_page_eth = requests.get(ETH_USD, headers=user_agent)
            soup_eth = BeautifulSoup(full_page_eth.content, 'html.parser')
            convert_eth = soup_eth.findAll("div", {"class": "css-1bwgsh3"})

            exchng_eth = (f"---Курс Эфириума---\n"
                          f"Ценна Эфириума: {convert_eth[0].text.strip()}")
            bot.send_message(message.chat.id, exchng_eth, parse_mode='html')
        except:
            bot.send_message(message.chat.id, "Курс сейчас не доступен...", parse_mode='html')
    elif message.text == '📕 Информация':
        infMenu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        inf_me = types.KeyboardButton('📗 Информация о пользователе')
        inf_bot = types.KeyboardButton('📙 Информация о боте')
        back = types.KeyboardButton('⬅️ Назад')

        infMenu.add(inf_me, inf_bot, back)

        inf_choise = f"Выберите о ком вы хотите узнать информацию."
        bot.send_message(message.chat.id, inf_choise, parse_mode='html', reply_markup=infMenu)
    elif message.text == '📗 Информация о пользователе':
        inf_me = (f"---Информация о тебе---\n"
                  f"Имя: {message.from_user.first_name}\n"
                  f"Фамилия: {message.from_user.last_name}\n"
                  f"Никнейм: {message.from_user.username}\n"
                  f"ID: {message.from_user.id}\n"
                  f"Бот: {message.from_user.is_bot}\n"
                  f"Премиум: {message.from_user.is_premium}")
        bot.send_message(message.chat.id, inf_me, parse_mode='html')
    elif message.text == '📙 Информация о боте':
        inf_bot = (f"Это простой бот с функциями:\n"
                   f"· Генерации случайных чисел\n"
                   f"· Прогноза погоды\n"
                   f"· Курсов валют(по МинФин) и криптовалют(по Бинанс)\n"
                   f"· Интересной информации")
        bot.send_message(message.chat.id, inf_bot, parse_mode='html')
    elif message.text == '⬅️ Назад':
        mainMenu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)

        rndm = types.KeyboardButton('🔸 Случайные числа')
        wthr = types.KeyboardButton('☀️ Прогноз погоды')
        exchng = types.KeyboardButton('📊 Курсы валют')
        inf = types.KeyboardButton('📕 Информация')

        mainMenu.add(rndm, wthr, exchng, inf)

        bck = f"Обратно в главное меню..."
        bot.send_message(message.chat.id, bck, parse_mode='html', reply_markup=mainMenu)
    else:
        dont_und = f"Я тебя не понимаю..."
        bot.send_message(message.chat.id, dont_und, parse_mode='html')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    smile = {
        "Thunderstorm": "Гроза 🌩",
        "Drizzle": "Морось 🌫",
        "Rain": "Дождь 🌧️",
        "Snow": "Снег ❄️",
        "Clear": "Солнце ☀️",
        "Clouds": "Облака ☁️",
        "Mist": "Туман 🌫",
        "Smoke": "Дым 🌫",
        "Haze": "Туман 🌫",
        "Dust": "Пыль 🌫",
        "Fog": "Туман 🌫",
        "Sand": "Песок 🌫",
        "Ash": "Пепел 🌫",
        "Squall": "Шквал 🌫",
        "Tornado": "Торнадо 🌪"
    }
    if message.text != '⬅️ Назад':
        try:
            weather_url = f'http://api.openweathermap.org/data/2.5/weather?appid={weather_api}&q={message.text}&units=metric'

            data = requests.get(weather_url).json()

            city = data['name']
            temp = data['main']['temp']

            weather_description = data['weather'][0]['main']
            if weather_description in smile:
                wd = smile[weather_description]
            else:
                wd = "Я не понимаю что за окном..."

            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            wind = data['wind']['speed']
            sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
            sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
            lenght_of_day = sunset - sunrise

            wthr_info = (f"Погода в месте: {city}\n"
                         f"Температура: {temp}C°\n"
                         f"{wd}\n"
                         f"Ощущается как: {feels_like}C°\n"
                         f"Влажность: {humidity}%\n"
                         f"Давление: {pressure} мм.рт.ст\n"
                         f"Скорость ветра: {wind} м/с\n"
                         f"Восход: {sunrise}\n"
                         f"Закат: {sunset}\n"
                         f"Продолжительность дня: {lenght_of_day}")

            wthr_text = bot.send_message(message.chat.id, wthr_info, parse_mode='html')
            bot.register_next_step_handler(wthr_text, get_weather)

        except:
            wthr_wrm = f"Проверьте правильность написания местоположения!"
            wthr_text = bot.send_message(message.chat.id, wthr_wrm, parse_mode='html')
            bot.register_next_step_handler(wthr_text, get_weather)
    elif message.text == '⬅️ Назад':
        mainMenu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)

        rndm = types.KeyboardButton('🔸 Случайные числа')
        wthr = types.KeyboardButton('☀️ Прогноз погоды')
        exchng = types.KeyboardButton('📊 Курсы валют')
        inf = types.KeyboardButton('📕 Информация')

        mainMenu.add(rndm, wthr, exchng, inf)

        bck = f"Обратно в главное меню..."
        bot.send_message(message.chat.id, bck, parse_mode='html', reply_markup=mainMenu)


if __name__ == "__main__":
    bot.polling(none_stop=True)
