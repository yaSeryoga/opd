#main file
import telebot
from config import TOKEN
import scheludeAPI as schelude

bot = telebot.TeleBot(TOKEN)


# Бот будет отвечать только на текстовые сообщения
# @bot.message_handler(content_types=['text'])
# def echo(message):
#     bot.send_message(message.chat.id, message.text)






#@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Это Телеграм бот для просмотра расписания Политехнического университета!\n'
                                        'Мы умеем:\n'
                                        '/todayYOUR_GROUP - получить расписание на сегодня (группу нужно вводить в формате 3532703_90001)\n'
                                        '/tomorrowYOUR_GROUP - получить расписакние на завтра\n'
                                        '/thisweekYOUR_GROUP - получить расписание на эту неделю\n'
                                        '/nextweekYOUR_GROUP - получить расписание на следующую неделю\n'
                                        '\nПосле того, как Вы в первый раз используйте какую-нибудь команду, появятся кнопки, которые облегчат работу с ботом :)\n'
                                        'Попробуйте что-нибудь, например, /today3532703_90001\n'
                                        '\nP.S. Проект находится на стадии разработки, так что, если появились какие-нибудь баги, просьба писать сюда: @ya_seryoga - мы, со своей стороны, сделаем всё возможное'
                                        )





#@bot.message_handler(commands=['today'])
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
        bot.send_message(message.chat.id, answer, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, day)




#@bot.message_handler(commands=['tomorrow'])
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
        bot.send_message(message.chat.id, answer, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, day)


#@bot.message_handler(commands=['thisweek'])
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

        #print(answer)
        bot.send_message(message.chat.id, answer, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, json)

#@bot.message_handler(commands=['nextweek'])
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

        #print(answer)
        bot.send_message(message.chat.id, answer, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, json)



@bot.message_handler(func=lambda m: True)
def replyall(message):
    text = message.text.upper()
    text = text.replace('_', '/')
   
    if text[:6] == '/START' or text[:5] == '/HELP':
        start(message)
    elif text[:6] == '/TODAY':
        today(message, text[6:])
    elif text[:9] == '/TOMORROW':
        tomorrow(message, text[9:])
    elif text[:9] == '/THISWEEK':
        thisweek(message, text[9:])
    elif text[:9] == '/NEXTWEEK':
        nextweek(message, text[9:])
    else:
        bot.send_message(message.chat.id, 'Неправильный запрос, проверьте команду или посмотрите /help')




if __name__ == '__main__':
    bot.polling(none_stop=True)