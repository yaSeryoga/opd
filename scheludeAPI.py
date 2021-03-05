import requests
from bs4 import BeautifulSoup

import pytz
import datetime


def _findJSON(html):
    scripts = html.find_all('script')
    for script in scripts:
        if 'window.__INITIAL_STATE__' in str(script):
            json = str(script)[41:]

    return json


def _getGroupNameFromElement(element):
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


def _getGroupScheludeURL(group):
    if group[:3] == '353' or group[:3] == '354' or group[:3] == '356' or group[:4] == 'в353' or group[:4] == 'в354' or group[:4] == 'з353' or group[:4] == 'з354':  #ИКНТ
        url = 'https://ruz.spbstu.ru/faculty/95/groups'
    elif group[:3] == '483' or group[:3] == '484' or group[:3] == '485':  #инфобез
        url = 'https://ruz.spbstu.ru/faculty/122/groups'
    elif group[:3] == '383':  #ГИ бакалавры
        url = 'https://ruz.spbstu.ru/faculty/101/groups'
    
    
    response = requests.get(url)


    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')
        groupsJson = _findJSON(soup)
        
        groupsJson = groupsJson.split('},')
        for element in groupsJson:
            #print(element)
            if group == _getGroupNameFromElement(element):
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
        return f'Error, response code: {response.status_code}'




def todaySchecude(group, lang='RU'):
    url = _getGroupScheludeURL(group)
    response = requests.get(url)
    

    offset = datetime.timezone(datetime.timedelta(hours=3))
    todayDate = str(datetime.datetime.now(offset))[:10]
    print(f'%{todayDate}%')

    soup = BeautifulSoup(response.text, 'html.parser')
    scheludeJSON = _findJSON(soup)
    print(scheludeJSON)
    weekDay = datetime.datetime.today().weekday()
    print('Антон' in scheludeJSON) 


    
    



def tomottowSchelude(group, lang):
    print('tomorrow')


def thisWeekSchelude(group, lang):
    print('this week')


def nextWeekSchelude(group, lang):
    print('next week') 

#3540202/00201
#3532703/90001
print(_getGroupScheludeURL('з3532703/90001'))
#todaySchecude('3532703/90001', 'RU')