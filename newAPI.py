import requests
import datetime


from pprint import pp, pprint

def _getFacultyId(group):
    if group[:3] == '353' or group[:3] == '354' or group[:3] == '356' or group[:4] == 'в353' or group[:4] == 'в354' or group[:4] == 'з353' or group[:4] == 'з354':  #ИКНТ
        # url = 'https://ruz.spbstu.ru/faculty/95/groups'
        id = 95
    elif group[:3] == '483' or group[:3] == '484' or group[:3] == '485':  #инфобез
        # url = 'https://ruz.spbstu.ru/faculty/122/groups'
        id = 122
    elif group[:3] == '383' or group[:3] == '384' or group[:3] == '385' or group[:3] == '386' or group[:4] == 'в383' or group[:4] == 'в384' or group[:4] == 'з383' or group[:4] == 'з384':  #ГИ
        # url = 'https://ruz.spbstu.ru/faculty/101/groups'
        id = 101
    elif group[:3] =='470' or group[:3] =='473' or group[:3] =='474' or group[:3] =='476' or group[:4] =='в473' or group[:4] =='з473' or group[:4] =='з474': #ИБСиБ
	    # url = 'https://ruz.spbstu.ru/faculty/119/groups'
        id = 119
    elif group[:3] == '426':  #физра 
        # url = 'https://ruz.spbstu.ru/faculty/121/groups'
        id = 121
    elif group[:3] =='434':#Институт передовых производственных технологий
        # url = 'https://ruz.spbstu.ru/faculty/111/groups'
        id = 111
    elif group[:3] =='195' or group[:4]=='в195' or group[:4] == 'ФиТ_' or group[:5] == 'КИиЭ_':  #институт ядерной энергетики
        # url = 'https://ruz.spbstu.ru/faculty/120/groups'
        id = 120
    elif group[:3]=='363' or group[:3]=='364' or group[:3]=='365' or group[:3]=='366': #ИПММ
        # url = 'https://ruz.spbstu.ru/faculty/99/groups'
        id = 99
    elif group[:3]=='333' or group[:3]=='334' or group[:3]=='335' or group[:3]=='336' or group[:4]=='з333':#ИММиТ
        # url = 'https://ruz.spbstu.ru/faculty/94/groups'
        id = 94
    elif group[:3]=='340' or group[:3]=='343' or group[:3]=='344' or  group[:3]=='346' or group[:4]== 'з343':#ИФНиТ
        # url = 'https://ruz.spbstu.ru/faculty/98/groups'
        id = 98
    elif group[:3]=='310' or group[:3]=='313' or group[:3]=='314' or group[:3]=='315' or group[:3]=='316' or group[:4]=='в313' or group[:4]=='з313' or group[:4]=='з314':#ИСИ
        # url = 'https://ruz.spbstu.ru/faculty/92/groups'
        id = 92
    elif group[:3]=='320' or group[:3]=='323' or group[:3]=='324' or group[:3]=='325' or group[:3]=='326' or group[:4]=='з323' or group[:4]=='з324':#ИЭ
        # url = 'https://ruz.spbstu.ru/faculty/93/groups'
        id = 93
    elif group[:3]=='373' or group[:3]=='374'or group[:3]=='375' or group[:3]=='376' or group[:4]=='в373' or group[:4]=='в374' or group[:4]=='з373' or group[:4]=='з374' or group[:4]=='з375' or group[:4]=='з376':#ИПМЭиТ
        # url = 'https://ruz.spbstu.ru/faculty/100/groups'
        id = 100
    else:
        return 1

    return id


def _getFacultyGroups(faculty_id):
    r = requests.get(f'https://ruz.spbstu.ru/api/v1/ruz/faculties/{faculty_id}/groups')
    if r.status_code == 200:
        return(r.json()['groups'])
    else:
        return r.json()


def _getDayName(weekday):
    if weekday == 1: return 'Понедельник'
    elif weekday == 2: return 'Вторник'
    elif weekday == 3: return 'Среда'
    elif weekday == 4: return 'Четверг'
    elif weekday == 5: return 'Пятница'
    elif weekday == 6: return 'Суббота'
    elif weekday == 7: return 'Воскресенье'
    else: return None


def __addDayNameToWeekSchedule(weekSchedule):
    for i in range(len(weekSchedule['days'])):
        weekSchedule['days'][i].update({'day_name': (_getDayName(weekSchedule['days'][i]['weekday']))})
    return weekSchedule


def getUserGroupInfo(group):
    facultyId = _getFacultyId(group)
    if facultyId != 1:
        groupList = _getFacultyGroups(facultyId)
        for element in groupList:
            if element['name'] == group:
                return element
        return 1
    else:
        return 1


def getThisWeekSchedule(group):
    groupInfo = getUserGroupInfo(group)
    if groupInfo != 1:
        groupId = groupInfo['id']
        r = requests.get(f'https://ruz.spbstu.ru/api/v1/ruz/scheduler/{groupId}')
        return __addDayNameToWeekSchedule(r.json())
    else:
        return 1

        



def getNextWeekSchedule(group):
    groupInfo = getUserGroupInfo(group)
    if groupInfo != 1:
        groupId = groupInfo['id']
        nextWeekDate = str(datetime.datetime.today() + datetime.timedelta(days=7))[:10]
        r = requests.get(f'https://ruz.spbstu.ru/api/v1/ruz/scheduler/{groupId}?date={nextWeekDate}')
        return __addDayNameToWeekSchedule(r.json())
    else:
        return 1



def getTodaySchedule(group):
    offset = datetime.timezone(datetime.timedelta(hours=3))
    weekday = datetime.datetime.now(offset).today().weekday() + 1
    weekSchedule = getThisWeekSchedule(group)
    if weekSchedule != 1:
        for element in weekSchedule['days']:
            if element['weekday'] == weekday:
                return element
        return {  # return this json if there is no any lessons
            'weekday': weekday,
            'date': str(datetime.date.today()),
            'lessons': False
        }
    else:
        return 1

def getTomorrowSchedule(group):
    offset = datetime.timezone(datetime.timedelta(hours=3))
    weekday = datetime.datetime.now(offset).today().weekday() + 1
    if weekday != 7:
        weekSchedule = getThisWeekSchedule(group)
        weekday += 1
    else:
        weekSchedule = getNextWeekSchedule(group)
        weekday = 1

    if weekSchedule != 1:
        for element in weekSchedule['days']:
            if element['weekday'] == weekday:
                return element
        return {  # return this json (with 'lessons': False) if there is no any lessons
            'weekday': weekday,
            'date': str(datetime.date.today()),
            'lessons': False
        }
    else:
        return 1



# pprint(getTomorrowSchedule('3532703/90101'))
# pprint(getNextWeekSchedule('3532703/90101'))
# pprint(getThisWeekSchedule('3532703/90101'))
# pprint(getTodaySchedule('3532703/90101'))
# pprint(getUserGroupInfo('3532703/90101'))