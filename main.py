import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import datetime as dt
import time
from random import choice

BOT_TOKEN = "6738472088:AAEoKitKwg6ACoomXgppzp3IQpXd43zMDgA"
find_city = ['москва', 'одинцово', 'санкт-петербург', 'великий новгород', 'нижний новгород', 'кострома', 'киров',
             'сочи', 'париж', 'вена',
             'анапа', 'калининград', 'красноярск', 'рязань', 'казань', 'псков', 'рим', 'изборск', 'лос-анджелес',
             'нью-йорк', 'лондон', 'марсель', 'стокгольм', 'крым', 'севастополь', 'мексика', 'китай', 'япония', 'тула',
             'ростов-на-дону', 'пекин', 'орландо', 'мадрид', 'венеция', 'милан', 'барселона']
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

reply_keyboard = [['Да', 'Нет']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот! Напиши или выбери команду из меню")


async def echo(update, context):
    await update.message.reply_text(update.message.text)


async def help_command(update, context):
    await update.message.reply_text("Я пока не умею помогать...")


async def reader_find(update, context):
    city = context.user_data['city']
    print(update.message.text.strip().lower(), city)
    if update.message.text.lower() == city:
        await update.message.reply_text(f"Да, это правильно, получи 50🪙\n"
                                        f"Хочешь продолжить игру? Нажми на кнопку", reply_markup=markup)
        with open('money.txt', 'rt') as f:
            f = f.read()
        with open('money.txt', 'w') as f1:
            f1.write(str(int(f.strip()) + 50))
    else:
        await update.message.reply_text(f"Это неправильный ответ, это {city.capitalize()}\n"
                                        f"Хочешь продолжить игру? Нажми на кнопку", reply_markup=markup)
    return 1


async def find(update, context):
    chat_id = update.effective_message.chat_id
    if update.message.text == "/find":
        await update.message.reply_text("Отгадай города. Я буду показывать город, а ты пиши мне его название")
    if update.message.text in ["Да", "/find"]:
        city = choice(find_city)
        context.user_data['city'] = city
        print(city)
        await context.bot.send_photo(chat_id, f'data/{city}.jpg', reply_markup=ReplyKeyboardRemove())
        print('отправлено')
        return 2
    else:
        await update.message.reply_text("Пока, ждем в гости! Вызывай новую команду, как понадоблюсь",
                                        reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


async def money(update, context):
    with open('money.txt', 'rt') as f:
        f = f.read()
    await update.message.reply_text(f)


async def stop(update, context):
    await update.message.reply_text("Пока, ждем в гости! Вызывай новую команду, как понадоблюсь",
                                    reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    app = Application.builder().token(token=BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("money", money))
    # app.add_handler(CommandHandler("find", find))
    app.add_handler(CommandHandler("play", help_command))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('find', find)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, find)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, reader_find)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    app.add_handler(conv_handler)
    text_handler = MessageHandler(filters.TEXT, echo)
    app.add_handler(text_handler)
    app.run_polling()


if __name__ == "__main__":
    main()
