#main file
import telebot
from config import TOKEN
import scheludeAPI as schelude

bot = telebot.TeleBot(TOKEN)


# Бот будет отвечать только на текстовые сообщения
# @bot.message_handler(content_types=['text'])
# def echo(message):
#     bot.send_message(message.chat.id, message.text)

BOLD = '\033[1m'
NORMAL = '\033[0m'





@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'start message')





@bot.message_handler(commands=['today'])
def today(message):
    day = schelude.todaySchecude('3532703/90001')

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




@bot.message_handler(commands=['tomorrow'])
def tomorrow(message):
    day = schelude.tomorrowSchelude('3532703/90001')

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
        answer = 'Сегодня выходной :)'
    bot.send_message(message.chat.id, answer, parse_mode='Markdown')


@bot.message_handler(commands=['thisweek'])
def thisweek(message):
    json = schelude.thisWeekSchelude('3532703/90001')
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

@bot.message_handler(commands=['nextweek'])
def nextweek(message):
    json = schelude.nextWeekSchelude('3532703/90001')
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


if __name__ == '__main__':
    bot.polling(none_stop=True)