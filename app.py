import telebot
from Config import keys, TOKEN
from Utility import ConvertException, CurrencyConvert

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_info(message: telebot.types.Message):
    text = "Чтобы начать работу, введите команду в следующем формате: \n<имя валюты> \
<в какую валюту переводим> \
<количество валюты, которую переводим> \n \
Увидеть список всех доступных валют : /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные для конвертации валюты:'
    for key in keys:
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertException("Необходимо ввести 3 параметра; за помощью - /help")

        quote, base, amount = values
        total_base = CurrencyConvert.convert(quote, base, amount)
    except ConvertException as e:
        bot.reply_to(message, f"Ошибка пользователя \n {e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду \n {e}")
    else:
        text = f"Цена {amount} {quote} в {base} - {total_base}"
        bot.send_message(message.chat.id, text)


bot.polling()