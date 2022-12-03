import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN) #создаём объект бота


@bot.message_handler(commands=["start", "help"])
def help(messege: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<колличество переводимой валюты> \nЧтобы увидеть список доступных валют: /values"
    bot.reply_to(messege, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ") #задаём переменную для трех значений разделённых пробелом

        if len(values) != 3: #если значение не равно трём, принудительно вызываем указанное исключение
            raise ConvertionException("Слишком много параметров!")

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду.\n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} = {total_base}"
        bot.send_message(message.chat.id, text)

bot.polling()