import requests
from bs4 import BeautifulSoup


def getGroupScheludeURL(group):
    if group[:3] == '353':
        url = 'https://ruz.spbstu.ru/faculty/95/groups'
        response = requests.get(url)
        #print(response.text)  #return html
        # for str in response.text.find_all('a'):
        #     if group in str:
        #         print(str)

        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        #print(links)

        for link in links:
            if group in link:
                url = 'https://ruz.spbstu.ru/' + link.get('href')

                
        #print(bufStr)
        #url = bufStr.get('href')
        print(url)




def todaySchecude(group):
    print('buf')


def tomottowSchelude(group):
    print('buf')


def thisWeekSchelude(group):
    print('buf')


def nextWeekSchelude(group):
    print('buf') 


getGroupScheludeURL('3532703/90001')