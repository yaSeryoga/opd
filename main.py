#ver 1.0
import telebot
from telebot import types
from config import TOKEN
import scheludeAPI as schelude

bot = telebot.TeleBot(TOKEN)


def start(message):
    bot.send_message(message.chat.id, 'Привет! Это Телеграм бот для просмотра расписания Политехнического университета!\n\n'
        'Для того, чтобы посмотреть расписание, отправьте нам номер группы. Псоле этого появятся кнопки, с помощью которых можно будет легко узнать всю нужную информацию\n\n'
        'У нас есть такие вот функции:\n'
        '/todayYOUR_GROUP - получить расписание на сегодня (группу нужно вводить в формате 3532703_90001)\n'
        '/tomorrowYOUR_GROUP - получить расписакние на завтра\n'
        '/thisweekYOUR_GROUP - получить расписание на эту неделю\n'
        '/nextweekYOUR_GROUP - получить расписание на следующую неделю\n'
        '/help - помощь по эксплуатации\n'
        '/info - посмотреть информацию о боте\n'
        '\nКнопки меняются каждый раз, когда Вы выбираете другую группу!\n\n'
        'Попробуйте что-нибудь, например, /today3532703_90001\n'
        '\nP.S. Проект находится на стадии разработки, так что, если появились какие-нибудь жалобы или предложения, просьба писать сюда: @ya_seryoga - мы, со своей стороны, сделаем всё возможное, чтобы стать лучше'
    )



def help(message):
    bot.send_message(message.chat.id, 'Для того, чтобы выбрать группу, просто напишите её номер в чат\n\n'
        'У нас есть такие вот функции:\n'
        '/todayYOUR_GROUP - получить расписание на сегодня (группу нужно вводить в формате 3532703_90001)\n'
        '/tomorrowYOUR_GROUP - получить расписакние на завтра\n'
        '/thisweekYOUR_GROUP - получить расписание на эту неделю\n'
        '/nextweekYOUR_GROUP - получить расписание на следующую неделю\n'
        '/help - помощь по эксплуатации\n'
        '/info - посмотреть информацию о боте\n'
        '\nКнопки меняются каждый раз, когда Вы выбираете другую группу!'
    )


def info(message):
    bot.send_message(message.chat.id, 'Бот разработан в рамках дисциплины "Основы проектной деятельности" командой ИКНТ-2614\n'
                                        'Версия от 09.04.2021')


def today(message, group):
    day = schelude.todaySchecude(group)
    if 'Ошибка' not in day:
        answer = ''
        if day["date"] != 'none':
                answer += f'*Сегодня, {day["day_name"]}, {day["date"][8:10]}.{day["date"][5:7]}*\n\n' 
                k = 1
                if day["lessons"] != 'Выходной':
                    for lesson in day["lessons"]:
                        answer += f'{k}. *{lesson["subject_name"]}*\n_{lesson["subject_type"]}_\n'
                        k += 1
                        answer += f'{lesson["time"]}\n'
                        if lesson['subject_name'] != 'Военная подготовка' and lesson['subject_name'] != 'Элективная физическая культура и спорт':
                            answer += f'_{lesson["teacher"]}_\n'
                            answer += f'{lesson["auditory"]}\n'
                            answer += f'[СДО]({lesson["lms_url"]})\n\n'
                else:
                    answer += 'Выходной\n\n'
        else:
            answer = 'Сегодня выходной :)'
        
        group = group.replace('/', '_')
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_today = types.KeyboardButton(f'/today{group}')
        item_tomorrow = types.KeyboardButton(f'/tomorrow{group}')
        item_thisweek = types.KeyboardButton(f'/thisweek{group}')
        item_nextweek = types.KeyboardButton(f'/nextweek{group}')
        item_help = types.KeyboardButton('/help')
        markup_reply.add(item_today, item_tomorrow, item_thisweek, item_nextweek, item_help)

        bot.send_message(message.chat.id, answer, parse_mode='Markdown', reply_markup=markup_reply)
    else:
        bot.send_message(message.chat.id, day)




def tomorrow(message, group):
    day = schelude.tomorrowSchelude(group)
    if 'Ошибка' not in day:
        answer = ''
        if day["date"] != 'none':
                answer += f'*Завтра, {day["day_name"]}, {day["date"][8:10]}.{day["date"][5:7]}*\n\n' 
                k = 1
                if day["lessons"] != 'Выходной':
                    for lesson in day["lessons"]:
                        answer += f'{k}. *{lesson["subject_name"]}*\n_{lesson["subject_type"]}_\n'
                        k += 1
                        answer += f'{lesson["time"]}\n'
                        if lesson['subject_name'] != 'Военная подготовка' and lesson['subject_name'] != 'Элективная физическая культура и спорт':
                            answer += f'_{lesson["teacher"]}_\n'
                            answer += f'{lesson["auditory"]}\n'
                            answer += f'[СДО]({lesson["lms_url"]})\n\n'
                else:
                    answer += 'Выходной\n\n'
        else:
            answer = 'Завтра выходной :)'
        

        group = group.replace('/', '_')
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_today = types.KeyboardButton(f'/today{group}')
        item_tomorrow = types.KeyboardButton(f'/tomorrow{group}')
        item_thisweek = types.KeyboardButton(f'/thisweek{group}')
        item_nextweek = types.KeyboardButton(f'/nextweek{group}')
        item_help = types.KeyboardButton('/help')
        markup_reply.add(item_today, item_tomorrow, item_thisweek, item_nextweek, item_help)

        bot.send_message(message.chat.id, answer, parse_mode='Markdown', reply_markup=markup_reply)
    else:
        bot.send_message(message.chat.id, day)



def thisweek(message, group):
    json = schelude.thisWeekSchelude(group)
    if 'Ошибка' not in json:
        answer = '*Расписание на неделю:*\n\n'
        for day in json:

            if day["date"] != 'none':
                answer += f'*{day["day_name"]}, {day["date"][8:10]}.{day["date"][5:7]}*\n\n' 
                k = 1
                if day["lessons"] != 'Выходной':
                    for lesson in day["lessons"]:
                        answer += f'{k}. *{lesson["subject_name"]}*\n_{lesson["subject_type"]}_\n'
                        k += 1
                        answer += f'{lesson["time"]}\n'
                        if lesson['subject_name'] != 'Военная подготовка' and lesson['subject_name'] != 'Элективная физическая культура и спорт':
                            answer += f'_{lesson["teacher"]}_\n'
                            answer += f'{lesson["auditory"]}\n'
                            answer += f'[СДО]({lesson["lms_url"]})\n\n'
                else:
                    answer += 'Выходной\n\n'

                answer += '\n\n'


        group = group.replace('/', '_')
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_today = types.KeyboardButton(f'/today{group}')
        item_tomorrow = types.KeyboardButton(f'/tomorrow{group}')
        item_thisweek = types.KeyboardButton(f'/thisweek{group}')
        item_nextweek = types.KeyboardButton(f'/nextweek{group}')
        item_help = types.KeyboardButton('/help')
        markup_reply.add(item_today, item_tomorrow, item_thisweek, item_nextweek, item_help)
        

        bot.send_message(message.chat.id, answer, parse_mode='Markdown', reply_markup=markup_reply)
    else:
        bot.send_message(message.chat.id, json)


def nextweek(message, group):
    json = schelude.nextWeekSchelude(group)
    if 'Ошибка' not in json:
        answer = '*Расписание на следующую неделю:*\n\n'
        for day in json:

            if day["date"] != 'none':
                answer += f'*{day["day_name"]}, {day["date"][8:10]}.{day["date"][5:7]}*\n\n' 
                k = 1
                if day["lessons"] != 'Выходной':
                    for lesson in day["lessons"]:
                        answer += f'{k}. *{lesson["subject_name"]}*\n_{lesson["subject_type"]}_\n'
                        k += 1
                        answer += f'{lesson["time"]}\n'
                        if lesson['subject_name'] != 'Военная подготовка' and lesson['subject_name'] != 'Элективная физическая культура и спорт':
                            answer += f'_{lesson["teacher"]}_\n'
                            answer += f'{lesson["auditory"]}\n'
                            if lesson["lms_url"] != '':
                                answer += f'[СДО]({lesson["lms_url"]})\n\n'
                            else: 
                                answer += '\n'
                        else:
                            answer += '\n'
                else:
                    answer += 'Выходной\n\n'

                answer += '\n\n'


        group = group.replace('/', '_')
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_today = types.KeyboardButton(f'/today{group}')
        item_tomorrow = types.KeyboardButton(f'/tomorrow{group}')
        item_thisweek = types.KeyboardButton(f'/thisweek{group}')
        item_nextweek = types.KeyboardButton(f'/nextweek{group}')
        item_help = types.KeyboardButton('/help')
        markup_reply.add(item_today, item_tomorrow, item_thisweek, item_nextweek, item_help)

        bot.send_message(message.chat.id, answer, parse_mode='Markdown', reply_markup=markup_reply)
    else:
        bot.send_message(message.chat.id, json)


def setgroup(message):
    group = message.text
    group = group.replace('/', '_')
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_today = types.KeyboardButton(f'/today{group}')
    item_tomorrow = types.KeyboardButton(f'/tomorrow{group}')
    item_thisweek = types.KeyboardButton(f'/thisweek{group}')
    item_nextweek = types.KeyboardButton(f'/nextweek{group}')
    item_help = types.KeyboardButton('/help')
    markup_reply.add(item_today, item_tomorrow, item_thisweek, item_nextweek, item_help)

    group = group.replace('_', '/')
    bot.send_message(message.chat.id, f'*Выбрана группа {group}*', parse_mode='Markdown', reply_markup=markup_reply)


@bot.message_handler(func=lambda m: True)
def replyall(message):
    text = message.text.upper().replace('_', '/')

    if text[:6] == '/TODAY':
        today(message, text[6:])
    elif text[:9] == '/TOMORROW':
        tomorrow(message, text[9:])
    elif text[:9] == '/THISWEEK':
        thisweek(message, text[9:])
    elif text[:9] == '/NEXTWEEK':
        nextweek(message, text[9:])
    elif 'Ошибка' not in schelude._getGroupScheludeURL(text):
        setgroup(message)
    elif text[:6] == '/START':
        start(message)
    elif  text[:5] == '/HELP':
        help(message)
    elif text[:5] == '/INFO':
        info(message) 
    else:
        bot.send_message(message.chat.id, 'Неправильный запрос, проверьте команду или посмотрите /help')




if __name__ == '__main__':
    bot.polling(none_stop=True)