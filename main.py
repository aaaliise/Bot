import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from random import choice
import json
import requests
from scripts import db_session
from scripts.user import User
from scripts.date_user import Date_user
from scripts.money_user import Money_user
import os

BOT_TOKEN = "6738472088:AAEoKitKwg6ACoomXgppzp3IQpXd43zMDgA"
FIND_CITY = [['москва', '37.520657,55.650667'], ['одинцово', '37.278230,55.678740'],
             ['санкт-петербург', '30.092569,59.940675'], ['великий новгород', '31.310137,58.560956'],
             ['нижний новгород', '43.833528,56.304645'], ['кострома', '40.901099,57.796071'],
             ['киров', '49.570865,58.583540'],
             ['сочи', '39.580041,43.713351'], ['париж', '2.347042,48.858823'], ['вена', '16.376247,48.216271'],
             ['анапа', '37.313574,44.921751'], ['калининград', '20.473801,54.704901'],
             ['красноярск', '92.874172,56.023097'], ['рязань', '39.718238,54.670371'],
             ['казань', '49.099982,55.767306'], ['псков', '28.358700,57.811740'], ['рим', '12.509593,41.894075'],
             ['изборск', '27.862106,57.709340'], ['лос-анджелес', '-118.411708,34.019109'],
             ['нью-йорк', '-73.979745,40.706902'], ['лондон', '-0.090420,51.491708'], ['марсель', '5.412660,43.304837'],
             ['стокгольм', '17.980247,59.333793'], ['ялта', '34.152003,44.502989'],
             ['севастополь', '33.548088,44.584571'], ['мехико', '-99.138654,19.374968'],
             ['тула', '37.618551,54.181173'],
             ['ростов-на-дону', '39.628128,47.254342'], ['пекин', '116.341702,39.960675'],
             ['орландо', '-81.393923,28.534487'], ['мадрид', '-3.703579,40.477905'], ['венеция', '12.338450,45.436982'],
             ['милан', '9.156186,45.478322'], ['барселона', '2.140209,41.392710']]
logging.basicConfig(filename='logging_file.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
Logger = logging.getLogger(__name__)
LIST_FOR_JOKE = ['A', '12', '24.04.24', 'С днем рождения!', '24.04', 'Самый лучший бот!', 'А можно премию?', 'ВИБР']

with open('city.json', encoding='utf-8') as file:
    data = json.load(file)

reply_keyboard = [['Да', 'Нет']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

casino1_keyboard = [['50', '10', '100'], ['30', '5', '200'], ['70', '600', '20']]
markup1 = ReplyKeyboardMarkup(casino1_keyboard, one_time_keyboard=False)

db_session.global_init("db/bot.db")
dbs = db_session.create_session()
dbs.commit()


async def start(update, context):
    global LIST_FOR_JOKE
    context.user_data["List_for_joke"] = LIST_FOR_JOKE
    chat_id = update.effective_message.chat_id
    await context.bot.forward_message(-4199349308, chat_id, update.message.message_id)
    if os.path.exists(f'photo/photo_{update.message.chat.id}.png'):
        await context.bot.send_photo(chat_id, f'photo/photo_{update.message.chat.id}.png',
                                     reply_markup=ReplyKeyboardRemove(),
                                     caption=f"Привет, {update.message.chat.first_name}! "
                                             f"Я бот!\nНапиши или выбери команду из меню\n"
                                     )
    else:
        await context.bot.send_photo(chat_id, 'data/orig.webp', reply_markup=ReplyKeyboardRemove(),
                                     caption=f"Привет, {update.message.chat.first_name}! "
                                             f"Я бот!\nНапиши или выбери команду из меню\n"
                                     )

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
        date = Date_user()
        date.name = update.message.chat.first_name
        date.user_id = update.message.chat.id
        if update.message.chat.last_name:
            date.surname = update.message.chat.last_name
        else:
            date.surname = ''
        db_sess.add(user)
        db_sess.commit()
    else:
        if not user1.surname:
            user1.surname = ''
        elif update.message.chat.last_name != user1.surname:
            user1.surname = update.message.chat.last_name
        elif update.message.chat.username != user1.username:
            user1.username = update.message.chat.username
        db_sess.commit()
    return ConversationHandler.END


async def help_command(update, context):
    await context.bot.forward_message(-4199349308, update.effective_message.chat_id, update.message.message_id)
    db_sess = db_session.create_session()
    date = db_sess.query(Date_user).filter(Date_user.user_id == update.message.chat.id).first()
    await update.message.reply_text(
        f"{date.name} {date.surname},\n"
        "Друг друга трудно нам понять,\n"
        "С тобой мы что-то не в ладу\n"
        "Надеюсь, помогу тебе сейчас\n"
        "---\n"
        "Для начала немного о функционале бота\n\n"
        "/start - запуск бота\n"
        "/money - нужна, чтобы узнать количество 🪙\n"
        "/find - игра 'угадай город по фото'\n"
        "/play -  игра 'в города'\n"
        "/casino - казино\n"
        "/joke - розыгрыши\n"
        "/stop - завершение игры, нужно нажимать, если ты хочешь прервать игру\n"
        "Чтобы поменять картинку в start, нужно отправить отправить эту картинку ФАЙЛОМ вне игр. "
        "И нажмите потом /start, чтобы посмотреть, что она загрузилась:)\n\n"
        "Теперь расскажу тебе о суть бота:\n"
        "В нем 2 главных раздела, которые сочетают в себе игры разных жанров: города, деньги-деньги – дребеденьги.\n"
        "В игре города (/play) бот играет с пользователем до тех пор, пока тот не захочет остановиться, или пока у "
        "кого-нибудь не закончатся слова.\n"
        "В игре угадай город (/find) пользователю даётся город и ему нужно определить, что за город изображён на "
        "фотографиях. За каждый правильный ответ в разделе города пользователь получает деньги, с помощью которых может "
        "играть в игры в разделе деньги-деньги – дребеденьги.\n"
        "В разделе деньги-деньги – дребеденьги пользователь может разделе казино (/casino) испытать удачу и выиграть "
        "деньги. Он выбирает сумму, бот ему пишет заработал или проиграл он свои деньги.\n"
        "В игре розыгрыши (/joke) будут розыгрыши, в которых пользователь может выиграть и получить деньги.\n"
        "Это был сюжет бота, а теперь расскажу, что делать, если что-то вдруг пойдёт не так\n"
        "Попробуй сделать так\n"
        "перезапусти бот\n(напиши /stop, а затем /start)\n"
        "и попробуй снова ввести свою команду\n"
        "(проследи за исправностью написания).\n"
        "Надеюсь я помог тебе и ты нашёл тут ответ на свой вопрос, если нет попробуй ещё раз ВНИМАТЕЛЬНО перечитать\n"
        "---\n"
        "Я не умею помогать,\n"
        "И в том признаться не боюсь,\n"
        "Но, чтобы время не терять,\nЯ помогать учусь."
        "\nИ пусть не получается пока,\nНо я так быстро не сдаюсь,"
        "\nЯ научусь наверняка.\nМогу дать слово, только попроси...")
    return ConversationHandler.END


async def reader_find(update, context):
    await context.bot.forward_message(-4199349308, update.effective_message.chat_id, update.message.message_id)
    chat_id = update.effective_message.chat_id
    city = context.user_data['city'][0]
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
    global FIND_CITY
    await context.bot.forward_message(-4199349308, update.effective_message.chat_id, update.message.message_id)
    chat_id = update.effective_message.chat_id
    if update.message.text == "/find":
        db_sess = db_session.create_session()
        date = db_sess.query(Date_user).filter(Date_user.user_id == update.message.chat.id).first()
        await update.message.reply_text(
            f"{date.name} {date.surname}, отгадай города. Я буду показывать город, а ты пиши мне его название")
    if update.message.text in ["Да", "/find"]:
        city = choice(FIND_CITY)
        context.user_data['city'] = city
        await context.bot.send_photo(chat_id, f'data/{city[0]}.jpg', reply_markup=ReplyKeyboardRemove(),
                                     caption='Что это за город?')
        return 2
    else:
        await update.message.reply_text("Ты завершил эту игру! Вызывай новую команду",
                                        reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


async def money(update, context):
    await context.bot.forward_message(-4199349308, update.effective_message.chat_id, update.message.message_id)
    db_sess = db_session.create_session()
    for money in db_sess.query(Money_user).filter(Money_user.user_id == update.message.chat.id):
        await update.message.reply_text(f'В твоём распоряжении на данный момент {money.money}🪙')
        return ConversationHandler.END


async def casino(update, context):
    await context.bot.forward_message(-4199349308, update.effective_message.chat_id, update.message.message_id)
    db_sess = db_session.create_session()
    for money in db_sess.query(Money_user).filter(Money_user.user_id == update.message.chat.id):
        if money.money > 0:
            if update.message.text in ["Да", "/casino"]:
                await update.message.reply_text(f"В твоём распоряжении на данный момент {money.money}🪙\nВыбери ставку",
                                                reply_markup=markup1)
            elif update.message.text == 'Нет':
                await update.message.reply_text("Ты завершил эту игру! Вызывай новую команду",
                                                reply_markup=ReplyKeyboardRemove())
                return ConversationHandler.END
            else:
                await update.message.reply_text(
                    f'Я не понял твою команду "{update.message.text}", перезапусти бот\n(напиши /stop, а затем /start)\n'
                    f'и попробуй снова ввести свою команду\n'
                    f'(проследи за исправностью написания).\nЕсли не получается напиши команду\n/help (после перезапуска), \nнадеюсь она тебе поможет.')
        else:
            await update.message.reply_text(
                "У тебя закончились 🪙, поэтому ты не можешь играть в казино.\nТы можешь заработать 🪙 в /find или /play\nВызывай новую команду, как понадоблюсь",
                reply_markup=ReplyKeyboardRemove())
    return 4


async def casino2(update, context):
    await context.bot.forward_message(-4199349308, update.effective_message.chat_id, update.message.message_id)
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
    await context.bot.forward_message(-4199349308, update.effective_message.chat_id, update.message.message_id)
    if update.message.text in ['Да', '/joke']:
        await update.message.reply_text('Введите акционнерный код:')
    else:
        await update.message.reply_text("Ты завершил эту игру! Вызывай новую команду",
                                        reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    return 6


async def joke2(update, context):
    await context.bot.forward_message(-4199349308, update.effective_message.chat_id, update.message.message_id)
    list_for_joke = context.user_data["List_for_joke"]
    if update.message.text in list_for_joke:
        list_for_joke.remove(update.message.text)
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
    context.user_data["List_for_joke"] = list_for_joke
    return 5


async def play(update, context):
    await context.bot.forward_message(-4199349308, update.effective_message.chat_id, update.message.message_id)
    context.user_data['list_of_words_for_play'] = []
    context.user_data['word'] = ''
    if update.message.text == "/play":
        db_sess = db_session.create_session()
        date = db_sess.query(Date_user).filter(Date_user.user_id == update.message.chat.id).first()
        await update.message.reply_text(
            f"{date.name} {date.surname}, поиграем в города России!\nТы начинаешь.\nПравила очень просты\n0.Все города, которые можно называть, только из России.\n1.Город, который тебе нужно назвать, начинается на последную букву предшесвующего города и удовлетворяет правилу № 0, КРОМЕ ПЕРВОГО\n2.Первый город ты можешь назвать любой, удовлетворяющий правилу №0\n3. Чтобы прекратить игру напиши (или выбери из меню) /stop")
        return 8
    else:
        await update.message.reply_text("Ты завершил эту игру! Вызывай новую команду")
        return ConversationHandler.END


async def play2(update, context):
    await context.bot.forward_message(-4199349308, update.effective_message.chat_id, update.message.message_id)
    list_for_play = context.user_data['list_of_words_for_play']
    name_city = update.message.text.strip()
    global data
    if context.user_data['word'] == '' or context.user_data['word'][-1] == name_city[0].lower() or \
            ((context.user_data['word'][-1] == 'ь' or context.user_data['word'][-1] == 'ы')
             and context.user_data['word'][-2] == name_city[0].lower()):
        if name_city in data[name_city[0].lower()] and name_city.lower() not in list_for_play:
            list_for_play.append(name_city.lower())
            if name_city[-1] in ['ь', 'ы']:
                letter = name_city[-2]
            else:
                letter = name_city[-1]
            name_city_answer = choice(data[letter])
            count_city = 0

            while name_city_answer.lower() in list_for_play and count_city < len(data[letter]):
                name_city_answer = choice(data[letter])
                count_city += 1
            if count_city == len(data[letter]):
                db_sess = db_session.create_session()
                for money in db_sess.query(Money_user).filter(Money_user.user_id == update.message.chat.id):
                    money.money += 100
                db_sess.commit()
                await update.message.reply_text(
                    f'Городов на букву {letter} в России больше нет\nТы выиграл, получи 100🪙')
                return ConversationHandler.END
            list_for_play.append(name_city_answer.lower())
            context.user_data['word'] = name_city_answer.lower()
            await update.message.reply_text(name_city_answer)
        elif name_city not in data[name_city[0].lower()]:
            await update.message.reply_text('Этого города нет в России, напиши другой или '
                                            'пишите названия городов с большой буквы (Москва)')
        elif name_city.lower() in list_for_play:
            await update.message.reply_text('Это слово уже было, напиши другое')

        context.user_data['list_of_words_for_play'] = list_for_play
    else:
        await update.message.reply_text(
            'Ты ввёл некоректное слово (см. правило игры №1), введи другое, с соблюдением всех правил')
    return 8


async def downloader(update, context):
    file = await context.bot.get_file(update.message.document)
    await file.download_to_drive(f'photo/photo_{update.message.chat.id}.png')
    return ConversationHandler.END


async def stop(update, context):
    await context.bot.forward_message(-4199349308, update.effective_message.chat_id, update.message.message_id)
    await update.message.reply_text("Ты завершил эту игру! Вызывай новую команду",
                                    reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    app = Application.builder().token(token=BOT_TOKEN).build()

    for_find = ConversationHandler(
        entry_points=[CommandHandler('find', find)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, find)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, reader_find)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    for_casino = ConversationHandler(
        entry_points=[CommandHandler('casino', casino)],
        states={
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, casino)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, casino2)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    for_joke = ConversationHandler(
        entry_points=[CommandHandler('joke', joke)],
        states={
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, joke)],
            6: [MessageHandler(filters.TEXT & ~filters.COMMAND, joke2)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    for_play = ConversationHandler(
        entry_points=[CommandHandler('play', play)],
        states={
            7: [MessageHandler(filters.TEXT & ~filters.COMMAND, play)],
            8: [MessageHandler(filters.TEXT & ~filters.COMMAND, play2)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    app.add_handlers(
        handlers={1: [for_find], 2: [for_casino], 3: [for_joke], 4: [for_play], 5: [CommandHandler("start", start)],
                  6: [CommandHandler("help", help_command)], 7: [CommandHandler("money", money)],
                  8: [MessageHandler(filters.Document.ALL, downloader)]})
    app.run_polling()


if __name__ == "__main__":
    main()
