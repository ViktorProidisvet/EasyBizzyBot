# EasyBizzyBot - телеграм-бот для интернет-магазинов
# Пока используем только статичные данные (без базы данных)
import telebot

# Токен бота (вставьте ваш токен от @BotFather)
BOT_TOKEN = "7876667144:AAFa9b4Th4t2lZAnUXn8QW-t2MLrZN2mfM0"

# создаем объект бота
bot = telebot.TeleBot(BOT_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '🚀 Привет! Я EasyBizzyBot!')

# Запуск бота
bot.polling()
