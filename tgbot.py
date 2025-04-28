from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

# Функция для проверки цены товара
def check_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Здесь замените "price-class" на класс цены на сайте Wildberries
    price_element = soup.find("span", class_="price__wrap")
    
    if price_element:
        price = int(price_element.text.replace(" ", "").replace("₽", ""))
        return price
    return None

# Функция для команды start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Привет! Отправьте мне ссылку на товар, и я буду уведомлять вас о снижении цены.")

# Функция для обработки ссылки
async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    price = check_price(url)
    if price:
        await update.message.reply_text(f"Цена товара: {price}₽. Я буду следить за изменением цены!")
        # Здесь можно сохранить ссылку и цену для отслеживания
    else:
        await update.message.reply_text("Не удалось получить цену товара. Пожалуйста, проверьте ссылку.")

# Создание приложения Telegram
app = ApplicationBuilder().token("7544681395:AAH5ZQkb6_cAB-HTzfQHclElC1E2e85l8b8").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("track", track))

if __name__ == "__main__":
    print("Бот запущен!")
    app.run_polling()
