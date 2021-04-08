#ver 1.0.1
import requests
from bs4 import BeautifulSoup

import pytz
import datetime


def __findJSON(html):
    scripts = html.find_all('script')
    for script in scripts:
        if 'window.__INITIAL_STATE__' in str(script):
            json = str(script)[41:]

    return json


def __getGroupNameFromElement(element):
    i = 0
    groupName = ''
    while i < len(element):
        if element[i:i+4] == 'name':
            i += 7
            while element[i] != '"':
                groupName += element[i]
                i += 1
        else:
            i += 1
    return groupName


def __getElementFromJson(element, json):
    global ii
    res = 'none'
    while ii < len(json):
        if json[ii:ii+len(element)] == element:
            ii += len(element) + 1
            while json[ii] != '"':
                ii += 1
            res = ''
            ii += 1
            while json[ii] != '"':
                res += json[ii]
                ii += 1
            res += ''
            ii += 1
            break
        else:
            ii += 1
    return res


def __parseScheludeJSON(json):
    i = 0
    while json[i:i+8] != '"data":{':
        i += 1

    i += 7
    while json[i] != '[':
        i += 1
    json = json[i:]
    i = 0
    i += 1

    figcounter = 0
    kvcounter = 1
    while figcounter != 0 or kvcounter != 0:
        if json[i] == '[':
            kvcounter += 1
        elif json[i] == ']':
            kvcounter -= 1
        elif json[i] == '{':
            figcounter += 1
        elif json[i] == '}':
            figcounter -= 1

        i += 1


    json = json[:i]
    global ii
    ii = 0

    result = []
    for dayNumber in range(1, 8):
        dayLessons = []
        if dayNumber == 1:
            dayName = 'Понедельник'
        elif dayNumber == 2:
            dayName = 'Вторник'
        elif dayNumber == 3:
            dayName = 'Среда'
        elif dayNumber == 4:
            dayName = 'Четверг'
        elif dayNumber == 5:
            dayName = 'Пятница'
        elif dayNumber == 6:
            dayName = 'Суббота'
        elif dayNumber == 7:
            dayName = 'Воскресенье'


        date = __getElementFromJson('date', json)
        if f'"weekday":{dayNumber}' not in json:
            moreLessons = False
            result.append({'day_number': dayNumber, 'date': date, 'day_name': dayName, 'lessons': 'Выходной'})
        else:
            moreLessons = True
            while moreLessons:
                lesson = {}
            
                #lesson.update({'day':  dayNumber})
                lesson.update({'subject_name': __getElementFromJson('subject', json)})
                lesson.update({'time': f'{__getElementFromJson("time_start", json)} - {__getElementFromJson("time_end", json)}'})
                lesson.update({'subject_type': __getElementFromJson('name', json)})
                if lesson['subject_name'] != 'Военная подготовка' and lesson['subject_name'] != 'Элективная физическая культура и спорт':
                    
                    lesson.update({'teacher': f'{__getElementFromJson("first_name", json)} {__getElementFromJson("middle_name", json)} {__getElementFromJson("last_name", json)}'})
                    lesson.update({'auditory': f'{__getElementFromJson("name", json)}, {__getElementFromJson("name", json)}'})
                    lesson.update({'lms_url': __getElementFromJson('lms_url', json)})
                if lesson['subject_name'] == 'Элективная физическая культура и спорт':

                    # __getElementFromJson("first_name", json)
                    # __getElementFromJson("middle_name", json)
                    # __getElementFromJson("last_name", json)
                    #__getElementFromJson("name", json)
                    __getElementFromJson('lms_url', json)
                
                    
                dayLessons.append(lesson)
                
                ii += 1
                if json[ii-1:ii+1] != '},':
                    moreLessons = False

            result.append({'day_number': dayNumber, 'date': date, 'day_name': dayName, 'lessons': dayLessons})  

    return(result)




def _getGroupScheludeURL(group):
    if group[:3] == '353' or group[:3] == '354' or group[:3] == '356' or group[:4] == 'в353' or group[:4] == 'в354' or group[:4] == 'з353' or group[:4] == 'з354':  #ИКНТ
        url = 'https://ruz.spbstu.ru/faculty/95/groups'
    elif group[:3] == '483' or group[:3] == '484' or group[:3] == '485':  #инфобез
        url = 'https://ruz.spbstu.ru/faculty/122/groups'
    elif group[:3] == '383' or group[:3] == '384' or group[:3] == '385' or group[:3] == '386' or group[:4] == 'в383' or group[:4] == 'в384' or group[:4] == 'з383' or group[:4] == 'з384':  #ГИ
        url = 'https://ruz.spbstu.ru/faculty/101/groups'
    elif group[:3] =='470' or group[:3] =='473' or group[:3] =='474' or group[:3] =='476' or group[:4] =='в473' or group[:4] =='з473' or group[:4] =='з474': #ИБСиБ
	    url = 'https://ruz.spbstu.ru/faculty/119/groups'
    elif group[:3] == '426':  #физра 
        url = 'https://ruz.spbstu.ru/faculty/121/groups'
    elif group[:3] =='434':#Институт передовых производственных технологий
        url = 'https://ruz.spbstu.ru/faculty/111/groups'
    elif group[:3] =='195' or group[:4]=='в195' or group[:4] == 'ФиТ_' or group[:5] == 'КИиЭ_':  #институт ядерной энергетики
        url = 'https://ruz.spbstu.ru/faculty/120/groups'
    elif group[:3]=='363' or group[:3]=='364' or group[:3]=='365' or group[:3]=='366': #ИПММ
        url = 'https://ruz.spbstu.ru/faculty/99/groups'
    elif group[:3]=='333' or group[:3]=='334' or group[:3]=='335' or group[:3]=='336' or group[:4]=='з333':#ИММиТ
        url = 'https://ruz.spbstu.ru/faculty/94/groups'
    elif group[:3]=='340' or group[:3]=='343' or group[:3]=='344' or  group[:3]=='346' or group[:4]== 'з343':#ИФНиТ
        url = 'https://ruz.spbstu.ru/faculty/98/groups'
    elif group[:3]=='310' or group[:3]=='313' or group[:3]=='314' or group[:3]=='315' or group[:3]=='316' or group[:4]=='в313' or group[:4]=='з313' or group[:4]=='з314':#ИСИ
        url = 'https://ruz.spbstu.ru/faculty/92/groups'
    elif group[:3]=='320' or group[:3]=='323' or group[:3]=='324' or group[:3]=='325' or group[:3]=='326' or group[:4]=='з323' or group[:4]=='з324':#ИЭ
        url = 'https://ruz.spbstu.ru/faculty/93/groups'
    elif group[:3]=='373' or group[:3]=='374'or group[:3]=='375' or group[:3]=='376' or group[:4]=='в373' or group[:4]=='в374' or group[:4]=='з373' or group[:4]=='з374' or group[:4]=='з375' or group[:4]=='з376':#ИПМЭиТ
        url = 'https://ruz.spbstu.ru/faculty/100/groups'
    else:
        return 'Группа не найдена'
    
    
    response = requests.get(url)


    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')
        groupsJson = __findJSON(soup)
        
        groupsJson = groupsJson.split('},')
        for element in groupsJson:
            if group == __getGroupNameFromElement(element):
                for char in element:
                    if char == 'i' and element[element.index(char) + 1] == 'd':
                        charid = element.index(char) + 4
                        groupid = ''
                        while element[charid] != ',':
                            groupid += element[charid]
                            charid += 1

        
        finalurl = url + '/' + groupid

        return finalurl

    else:
        return f'Ошибка {response.status_code}'




def todaySchecude(group):
    url = _getGroupScheludeURL(group)
    response = requests.get(url)
    

    offset = datetime.timezone(datetime.timedelta(hours=3))
    todayDate = str(datetime.datetime.now(offset))[:10]

    soup = BeautifulSoup(response.text, 'html.parser')
    scheludeJSON = __findJSON(soup)

    weekday = datetime.datetime.now(offset).today().weekday()

    weekSchelude = __parseScheludeJSON(scheludeJSON)
    return weekSchelude[weekday]


def tomorrowSchelude(group):
    weekday = datetime.datetime.today().weekday()
    
    if weekday != 6:
        weekSchelude = thisWeekSchelude(group)
        return weekSchelude[weekday+1]
    else:
        weekSchelude = nextWeekSchelude(group)
        return weekSchelude[0]
    


def thisWeekSchelude(group):
    url = _getGroupScheludeURL(group)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    scheludeJSON = __findJSON(soup)
  
    scheludeList = __parseScheludeJSON(scheludeJSON)
    return scheludeList


def nextWeekSchelude(group):
    url = _getGroupScheludeURL(group)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    buttons = soup.find_all('a')

    href = ''
    found = False
    for button in buttons:
        if found == False:
            if 'Следующая неделя' in button:
                i = 0
                button = str(button)
                while i < len(button):
                    if button[i:i+6] != 'href="':
                        i += 1
                    else:
                        i += 6
                        while button[i] != '"':
                            href += button[i]
                            i += 1
                        found = True
                        break


    url = 'https://ruz.spbstu.ru' + href

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    scheludeJSON = __findJSON(soup)
  
    scheludeList = __parseScheludeJSON(scheludeJSON)

    return(scheludeList)
