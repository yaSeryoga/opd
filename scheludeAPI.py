import requests
from bs4 import BeautifulSoup
#from selenium import webdriver

import datetime


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
        scripts = soup.find_all('script')
        for script in scripts:
            if 'window.__INITIAL_STATE__' in str(script):
                groupsJson = str(script)[41:]
        #print(groupsJson)
        groupsJson = groupsJson.split('},')
        for element in groupsJson:
            if group in element:
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




def todaySchecude(group, lang):
    now = datetime.datetime.now()
    print(now.month, now.hour, now.minute)
    print('today')
    url = _getGroupScheludeURL(group)
    response = requests.get(url)
    #print(response.text)
    soup = BeautifulSoup(response.content, 'html.parser')
    days = soup.find_all('li', {'class': 'schedule__day'})
    # for day in days:
    #     for line in lines:
    #         if  
    
    



def tomottowSchelude(group, lang):
    print('tomorrow')


def thisWeekSchelude(group, lang):
    print('this week')


def nextWeekSchelude(group, lang):
    print('next week') 

#3540202/00201
#3532703/90001
print(_getGroupScheludeURL('4831001/00002'))
#todaySchecude('3532703/90001', 'RU')