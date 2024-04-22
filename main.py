import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from random import choice
import sys
import requests
from scripts import db_session
from scripts.user import User
from scripts.date_user import Date_user
from scripts.money_user import Money_user


BOT_TOKEN = "6738472088:AAEoKitKwg6ACoomXgppzp3IQpXd43zMDgA"
find_city = [['москва', '37.520657,55.650667'], ['одинцово', '37.278230,55.678740'],
             ['санкт-петербург', '30.092569,59.940675'], ['великий новгород', '31.310137,58.560956'],
             ['нижний новгород', '43.833528,56.304645'], ['кострома', '40.901099,57.796071'],
             ['киров', '49.570865,58.583540'],
             ['сочи', '39.580041,43.713351'], ['париж', '2.347042,48.858823'], ['вена', '16.376247,48.216271'],
             ['анапа', '37.313574,44.921751'], ['калининград', '20.473801,54.704901'],
             ['красноярск', '92.874172,56.023097'], ['рязань', '39.718238,54.670371'],
             ['казань', '49.099982,55.767306'], ['псков', '28.358700,57.811740'], ['рим', '12.509593,41.894075'],
             ['изборск', '27.862106,57.709340'], ['лос-анджелес', '-118.411708,34.019109'],
             ['нью-йорк', '-73.979745,40.706902'], ['лондон', '-0.090420,51.491708'], ['марсель', '5.412660,43.304837'],
             ['стокгольм', '17.980247,59.333793'], ['крым', '34.526191,45.226951'],
             ['севастополь', '33.548088,44.584571'], ['мехико', '-99.138654,19.374968'],
             ['тула', '37.618551,54.181173'],
             ['ростов-на-дону', '39.628128,47.254342'], ['пекин', '116.341702,39.960675'],
             ['орландо', '-81.393923,28.534487'], ['мадрид', '-3.703579,40.477905'], ['венеция', '12.338450,45.436982'],
             ['милан', '9.156186,45.478322'], ['барселона', '2.140209,41.392710']]
logging.basicConfig(filename='example2.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
list_for_joke = ['A', '12', '24.04.24']

reply_keyboard = [['Да', 'Нет']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

casino1_keyboard = [['50', '10', '100'], ['30', '5', '200'], ['70', '600', '20']]
markup1 = ReplyKeyboardMarkup(casino1_keyboard, one_time_keyboard=False)

db_session.global_init("db/bot.db")
dbs = db_session.create_session()
dbs.commit()


async def start(update, context):
    chat_id = update.effective_message.chat_id
    await context.bot.send_photo(chat_id, 'data/orig.webp', reply_markup=ReplyKeyboardRemove(),
                                 caption=f"Привет! Я бот!\nНапиши или выбери команду из меню")
    user = update.effective_user
    db_sess = db_session.create_session()
    user1 = db_sess.query(User).filter(User.user_id == update.message.chat.id).first()
    if not user1:
        user = User()
        user.user_id = update.message.chat.id
        if update.message.chat.username:
            user.username = update.message.chat.username
        db_sess.add(user)
        money = Money_user(user_id=update.message.chat.id, money=0)
        db_sess.add(money)
        user = Date_user()
        user.name = update.message.chat.first_name
        user.user_id = update.message.chat.id
        if update.message.chat.last_name:
            user.surname = update.message.chat.last_name
        else:
            user.surname = ''
        db_sess.add(user)
        db_sess.commit()
    else:
        print(user1.surname)
        if not user1.surname:
            user1.surname = ''
            print(user1.surname)
        elif update.message.chat.last_name != user1.surname:
            user1.surname = update.message.chat.last_name
        elif update.message.chat.username != user1.username:
            user1.username = update.message.chat.username
        db_sess.commit()

    # await context.bot.forward_message(chat_id, '-4199349308', update.message.message_id)
    # await update.message.reply_html(
    # rf"Привет {user.mention_html()}! Я бот! Напиши или выбери команду из меню")


async def echo(update, context):
    await update.message.reply_text(
        f'Я не понял твою команду "{update.message.text}", перезапусти бот\n(напиши /stop, а затем /start)\n'
        f'и попробуй снова ввести свою команду\n'
        f'(проследи за исправностью написания).\nЕсли не получается напиши команду\n/help, надеюсь она тебе поможет.')


async def help_command(update, context):
    await update.message.reply_text(
        "Я не умею помогать,\nИ в том признаться не боюсь,\nНо, чтобы время не терять,\nЯ помогать учусь.\nИ пусть не получается пока,\nНо я так быстро не сдаюсь,\nЯ научусь наверняка.\nМогу дать слово, только попроси...")


async def reader_find(update, context):
    chat_id = update.effective_message.chat_id
    city = context.user_data['city'][0]
    print(update.message.text.strip().lower(), city)
    if update.message.text.lower() == city:
        await update.message.reply_text(f"Да, это правильно, получи 50🪙\n"
                                        f"Хочешь продолжить игру? Нажми на кнопку", reply_markup=markup)
        db_sess = db_session.create_session()
        for money in db_sess.query(Money_user).filter(Money_user.user_id == update.message.chat.id):
            money.money += 50
        db_sess.commit()
    else:
        places = context.user_data['city'][1]
        map_request = f"https://static-maps.yandex.ru/1.x/?l=map&ll={places}&spn=1.000,1.000&l=map"
        response = requests.get(map_request)
        map_file = f"map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        await context.bot.send_photo(chat_id, 'map.png', reply_markup=markup,
                                     caption=f"Это неправильный ответ, это {city.capitalize()}.\nВзгляни на этот город с высоты.\nХочешь продолжить игру? Нажми на кнопку", )
    return 1


async def find(update, context):
    chat_id = update.effective_message.chat_id
    if update.message.text == "/find":
        await update.message.reply_text("Отгадай города. Я буду показывать город, а ты пиши мне его название")
    if update.message.text in ["Да", "/find"]:
        city = choice(find_city)
        context.user_data['city'] = city
        print(city[0])
        await context.bot.send_photo(chat_id, f'data/{city[0]}.jpg', reply_markup=ReplyKeyboardRemove(),
                                     caption='Что это за город?')
        return 2
    else:
        await update.message.reply_text("Пока, ждем в гости! Вызывай новую команду, как понадоблюсь",
                                        reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


async def money(update, context):
    db_sess = db_session.create_session()
    for money in db_sess.query(Money_user).filter(Money_user.user_id == update.message.chat.id):
        await update.message.reply_text(f'В твоём распоряжении на данный момент {money.money}🪙')


async def casino(update, context):
    db_sess = db_session.create_session()
    for money in db_sess.query(Money_user).filter(Money_user.user_id == update.message.chat.id):
        if money.money > 0:
            if update.message.text in ["Да", "/casino"]:
                await update.message.reply_text(f"В твоём распоряжении на данный момент {money.money}🪙\nВыбери ставку",
                                                reply_markup=markup1)
            elif update.message.text == 'Нет':
                await update.message.reply_text("Пока, ждем в гости! Вызывай новую команду, как понадоблюсь",
                                                reply_markup=ReplyKeyboardRemove())
                return ConversationHandler.END
            else:
                await update.message.reply_text(
                    f'Я не понял твою команду "{update.message.text}", перезапусти бот\n(напиши /stop, а затем /start)\n'
                    f'и попробуй снова ввести свою команду\n'
                    f'(проследи за исправностью написания).\nЕсли не получается напиши команду\n/help (после перезапуска), \nнадеюсь она тебе поможет.')
        else:
            await update.message.reply_text("У тебя закончились 🪙, поэтому ты не можешь играть в казино.\nТы можешь заработать 🪙 в /find или /play\nВызывай новую команду, как понадоблюсь",
                                            reply_markup=ReplyKeyboardRemove())
    return 4


async def casino2(update, context):
    db_sess = db_session.create_session()
    text = update.message.text
    comand = choice(['1', '2'])
    if text:
        if comand == '1':
            for money in db_sess.query(Money_user).filter(Money_user.user_id == update.message.chat.id):
                money.money += 1
                money.money *= int(text)
            await update.message.reply_text(f"Ты везучий. Твои 🪙 увеличились в {text} раз\n"
                                            f"Хочешь продолжить игру в казино? Нажми на кнопку", reply_markup=markup)
        else:
            for money in db_sess.query(Money_user).filter(Money_user.user_id == update.message.chat.id):
                money.money //= int(text)
            await update.message.reply_text(f"Ну, что ж, не повезло. Твои 🪙 уменьшились в {text} раз\n"
                                            f"Хочешь продолжить игру? Нажми на кнопку", reply_markup=markup)
        db_sess.commit()
    return 3


async def joke(update, context):
    if update.message.text in ['Да', '/joke']:
        await update.message.reply_text('Введите акционнерный код:')
    else:
        await update.message.reply_text("Пока, ждем в гости! Вызывай новую команду, как понадоблюсь",
                                        reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    return 6


async def joke2(update, context):
    if update.message.text in list_for_joke:
        db_sess = db_session.create_session()
        for money in db_sess.query(Money_user).filter(Money_user.user_id == update.message.chat.id):
            money.money += 50
        db_sess.commit()
        await update.message.reply_text(f"Ты использовал свой купон и получил 50🪙\n"
                                        f"Хочешь продолжить обналичивать свои коды? Нажми на кнопку",
                                        reply_markup=markup)
    else:
        await update.message.reply_text(f"Я не знаю такого кода\n"
                                        f"Хочешь продолжить обналичивать свои коды? Нажми на кнопку",
                                        reply_markup=markup)
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
    app.add_handler(CommandHandler("play", help_command))
    app.add_handler(CommandHandler("stop", stop))
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
