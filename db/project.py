import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from random import choice
from data.user import Table0
from data import db_session
from .db_session import SqlAlchemyBase

user = Table0()
user.name = "Пользователь 1"
user.about = "биография пользователя 1"
user.email = "email@email.ru"
db_sess = db_session.create_session()
db_sess.add(user)
db_sess.commit()


BOT_TOKEN = "6738472088:AAEoKitKwg6ACoomXgppzp3IQpXd43zMDgA"
find_city = ['москва', 'одинцово', 'санкт-петербург', 'великий новгород', 'нижний новгород', 'кострома', 'киров',
             'сочи', 'париж', 'вена',
             'анапа', 'калининград', 'красноярск', 'рязань', 'казань', 'псков', 'рим', 'изборск', 'лос-анджелес',
             'нью-йорк', 'лондон', 'марсель', 'стокгольм', 'крым', 'севастополь', 'мексика', 'китай', 'япония', 'тула',
             'ростов-на-дону', 'пекин', 'орландо', 'мадрид', 'венеция', 'милан', 'барселона']
logging.basicConfig(filename='example2.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
                    )

logger = logging.getLogger(__name__)
list_for_joke = ['A', '12', '24.04.24']

reply_keyboard = [['Да', 'Нет']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

casino1_keyboard = [['50', '10', '100'], ['30', '5', '200'], ['70', '600', '20']]
markup1 = ReplyKeyboardMarkup(casino1_keyboard, one_time_keyboard=False)


async def start(update, context):
    chat_id = update.effective_message.chat_id
    user = update.effective_user
    await context.bot.send_photo(chat_id, 'data/orig.webp', reply_markup=ReplyKeyboardRemove(), caption=f"Привет! Я бот!\nЯ Напиши или выбери команду из меню")
    #await context.bot.forward_message(chat_id, '-4199349308', update.message.message_id)
    #await update.message.reply_html(
        #rf"Привет {user.mention_html()}! Я бот! Напиши или выбери команду из меню")


async def echo(update, context):
    await update.message.reply_text(update.message.text)


async def help_command(update, context):
    await update.message.reply_text(
        "Я не умею помогать,\nИ в том признаться не боюсь,\nНо, чтобы время не терять,\nЯ помогать учусь.\nИ пусть не получается пока,\nНо я так быстро не сдаюсь,\nЯ научусь наверняка.\nМогу дать слово, только попроси...")


async def reader_find(update, context):
    chat_id = update.effective_message.chat_id
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
        await context.bot.send_photo(chat_id, f'data/{city}.jpg', reply_markup=ReplyKeyboardRemove(), caption='Что это за город?')
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


async def casino(update, context):
    await update.message.reply_text("Выбери ставку",
                                    reply_markup=markup1)
    return 4


async def casino2(update, context):
    text = update.message.text
    comand = choice(['1', '2'])
    if text:
        if comand == '1':
            with open('money.txt', 'rt') as f:
                f = f.read()
            with open('money.txt', 'w') as f1:
                f1.write(f'{int(f) * int(text)}')
            await update.message.reply_text(f"Ты везучий. Твои деньги увеличились в {text} раз",
                                            reply_markup=ReplyKeyboardRemove())
        else:
            with open('money.txt', 'rt') as f:
                f = f.read()
            with open('money.txt', 'w') as f1:
                f1.write(f'{int(f) // int(text)}')
            await update.message.reply_text(f"Ну, что ж, не повезло. Твои деньги уменьшились в {text} раз",
                                            reply_markup=ReplyKeyboardRemove())
    return 3


async def music(update, context):
    chat_id = update.effective_message.chat_id
    await context.bot.send_audio(chat_id, 'data/music.mp3')


async def joke(update, context):
    await update.message.reply_text('Введите акционнерный код:')
    return 6


async def joke2(update, context):
    if update.message.text in list_for_joke:
        with open('money.txt', 'rt') as f:
            f = f.read()
        with open('money.txt', 'w') as f1:
            f1.write(f'{int(f) + 50}')
        await update.message.reply_text(f"Ты использовал свой купон и получил 50🪙")
    return 5


async def stop(update, context):
    await update.message.reply_text("Пока, ждем в гости! Вызывай новую команду, как понадоблюсь",
                                    reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    app = Application.builder().token(token=BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("money", money))
    #app.add_handler(CommandHandler("casino", casino))
    # app.add_handler(CommandHandler("find", find))
    app.add_handler(CommandHandler("play", help_command))
    app.add_handler(CommandHandler("music", music))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('find', find)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, find)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, reader_find)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler('casino', casino)],
        states={
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, casino)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, casino2)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler('joke', joke)],
        states={
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, joke)],
            6: [MessageHandler(filters.TEXT & ~filters.COMMAND, joke2)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    app.add_handler(conv_handler)
    app.add_handler(conv_handler1)
    app.add_handler(conv_handler2)
    text_handler = MessageHandler(filters.TEXT, echo)
    app.add_handler(text_handler)
    app.run_polling()


if __name__ == "__main__":
    main()
