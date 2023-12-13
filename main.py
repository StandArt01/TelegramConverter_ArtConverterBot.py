import telebot
from config import TOKEN, keys
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['voice', ])
def function_name(message):
    bot.reply_to(message, "This is a message handler")

@bot.message_handler(commands=['start', 'help'])
def echo(message):
    instructions = "Приветсвую! Я бот, который поможет вам узнать цену на определенное количество валюты.\n" \
                   "Для получения цены введите сообщение в формате: <валюта1> <валюта2> <количество>\n" \
                   "Например: USD RUB 100\n" \
                   "Для списка доступных валют введите /values"
    bot.send_message(message.chat.id, instructions)

@bot.message_handler(commands=['values'])
def values(message):
    values_info = "Доступные валюты: EUR, USD, RUB"
    bot.send_message(message.chat.id, values_info)

@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException("Неверный формат запроса. Пожалуйста, используйте формат: <валюта1> <валюта2> <количество>")

        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
        text = f"{amount} {quote} в {base} = {total_base} "
        bot.send_message(message.chat.id, text)

    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка пользователя: {e}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка в обработке команды: {e}")

if __name__ == "__main__":
    bot.polling(none_stop=True)