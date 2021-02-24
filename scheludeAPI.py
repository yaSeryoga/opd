import requests
from bs4 import BeautifulSoup
#from selenium import webdriver

import datetime


def _getGroupScheludeURL(group):
    if group[:3] == '353':  #ИКНТ бакалавры
        url = 'https://ruz.spbstu.ru/faculty/95/groups'
        response = requests.get(url)
    elif group[:3] == '354':  #ИКНТ магистры
        url = 'https://ruz.spbstu.ru/faculty/95/groups'
        response = requests.get(url)
        #как нажать на кнопку "магистр??"     

    elif group[:3] == '483':
        url = 'https://ruz.spbstu.ru/faculty/122/groups'
        response = requests.get(url)
    
    
    if response.status_code == 200:

        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            if group in link:
                finalurl = 'https://ruz.spbstu.ru/' + link.get('href')
            
        return finalurl
    else:
        return 'САЙТ ЛЕЖИТ'




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
print(_getGroupScheludeURL('4831001/00001'))
#todaySchecude('3532703/90001', 'RU')