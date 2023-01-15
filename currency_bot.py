import telebot
from config import TOKEN, currencies
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Бот-конвертер приветствует вас!\n \
Для начала работы введите команду в следующем формате:\n \
<валюта, цену которой вы хотите узнать> \
<валюта, в которой надо узнать цену первой валюты> \
<количество первой валюты>\n \
Для ознакомления со списком доступных валют введите /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for currency in currencies.keys():
        text = '\n'.join((text, currency))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Введите 3 параметра!')

        base, quote, amount = values
        result = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя:\n{e}")

    except Exception as e:
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.send_message(message.chat.id, result)

bot.polling()
