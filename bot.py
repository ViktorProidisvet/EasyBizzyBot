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

#Обработчик команды /help
@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = ( "Я - бот ассистент интернет-магазина.\n"
                "Вот что я умею:\n"
                "/start - Приветствие\n"
                "/help - Показать это сообщение\n"
                "/catalog - Показать список товаров\n"
                  )
    bot.send_message(message.chat.id, help_text)

# статичный список товаров - в дальнейшем добавить БД!
products = [
    {"id": 1, "sku": "TSH001", "name": "Футболка", "price": 500, "size": "M", "color": "синий"},
    {"id": 2, "sku": "JNS002", "name": "Джинсы", "price": 1200, "size": "L", "color": "черный"},
    {"id": 3, "sku": "HAT003", "name": "Кепка", "price": 300, "size": "универсальный", "color": "красный"}
]

@bot.message_handler(commands=['catalog'])
def catalog_message(message):
    response = "🛍️ Каталог товаров:\n\n"
    for product in products:
        response += f"Артикул: {product['sku']}\n" \
                    f"Название: {product['name']}\n" \
                    f"Цена: {product['price']} грн\n" \
                    f"Размер: {product['size']}\n" \
                    f"Цвет: {product['color']}\n\n"
    bot.send_message(message.chat.id, response)


#Временное хранилище заказов
orders = {}

@bot.message_handler(commands=['order'])
def order_start(message):
    bot.send_message(message.chat.id, "Введите артикул товара, который хотите заказать:")
    bot.register_next_step_handler(message, get_product_by_sku)

def get_product_by_sku(message):
    sku = message.text.strip().upper()
    product = next((p for p in products if p['sku'] == sku), None)

    if not product:
        bot.send_message(message.chat.id, "❌ Товар с таким артикулом не найден. Попробуйте ещё раз.")
        return

#Сохранение товара в заказы:
    orders[message.chat.id] = {'product': product}
    bot.send_message(message.chat.id, f"✅ Вы выбрали: {product['name']} за {product['price']} грн\n\nВведите ваше имя:")
    bot.register_next_step_handler(message, get_costumer_name)

def get_costumer_name(message):
    orders[message.chat.id]['name'] = message.text.strip()
    bot.send_message(message.chat.id, "Введите ваш номер телефона:")
    bot.register_next_step_handler(message, get_costumer_phone)

def get_costumer_phone(message):
    orders[message.chat.id]['phone'] = message.text.strip()
    bot.send_message(message.chat.id, "Введите адрес доставки:")
    bot.register_next_step_handler(message, get_costumer_address)

def get_costumer_address(message):
    orders[message.chat.id]['address'] = message.text.strip()

    order = orders[message.chat.id]
    summary = (
            "📦 Новый заказ:\n"
            f"Товар: {order['product']['name']} ({order['product']['sku']})\n"
            f"Цена: {order['product']['price']} грн\n"
            f"Имя клиента: {order['name']}\n"
            f"Телефон: {order['phone']}\n"
            f"Адрес: {order['address']}"
    )

    bot.send_message(message.chat.id, "✅ Спасибо! Ваш заказ оформлен:")
    bot.send_message(message.chat.id, summary)

# Запуск бота
bot.polling()
