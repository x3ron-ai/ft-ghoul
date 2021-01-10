# -*- coding: <utf-8> -*-

from VK_cfg import settings
import vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import random
from datetime import datetime, timedelta
import requests
import sqlite3
from bs4 import BeautifulSoup
import json
from PIL import Image, ImageDraw, ImageFont
from replit import db
import datetime as dt
import pyowm
import xml.etree.ElementTree as ET
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import pickle
from gtts import gTTS
from zalgo_text import zalgo

kb = VkKeyboard(inline=True)

from keep_alive import keep_alive
try:
	tree = ET.parse("banned.xml")
	root = tree.getroot()
	xml_doc = ET.Element('root')
except:
	pass


#xml и всякое такое к нему относящееся
def linked():
	try:
		vk.method('messages.getInviteLink', {'peer_id': 2000000000 + group_ID})
	except:
		vk.method(
		    'messages.send', {
		        'chat_id': group_ID,
		        'message': 'Предоставьте доступ к ссылке на беседу',
		        'random_id': get_random_id(),
		        'attachment': 'video315625951_456239157'
		    })


def weather(city):
	try:
		owm = pyowm.OWM('4797f7598bd39b32d692b4de7c4ab1e0')
		mgr = owm.weather_manager()
		observation = mgr.weather_at_place(city)
		w = observation.weather
		temp = w.temperature('celsius')['temp']
		write_mes(group_ID,
		          f'Температура в {city}: ' + str(temp) + ', по цельсию')
	except:
		otvet = 'Что-то пошло не так...'
		vk.method(
		    'messages.send', {
		        'chat_id': group_ID,
		        'message': otvet,
		        'random_id': get_random_id(),
		        'attachment': 'video315625951_456239157'
		    })


def just_ban(user_id, reason=None):
	user_id = str(user_id)
	#id
	user = ET.SubElement(xml_doc, 'user', id=user_id)
	name = ET.SubElement(
	    user,
	    'name',
	    name=f'{vk.method("users.get", {"user_ids":j})[0]["first_name"]}')
	reas = ET.SubElement(user, 'reason', reason=reason)

	smb_var = str(ET.tostring(xml_doc))
	#decoration
	prettify(xml_doc)
	myfile = open("banned.xml", "w")
	myfile.write(smb_var)


def prettify(element, indent='  '):
	queue = [(0, element)]  # (level, element)
	while queue:
		level, element = queue.pop(0)
		children = [(level + 1, child) for child in list(element)]
		if children:
			element.text = '\n' + indent * (level + 1)  # for child open
		if queue:
			element.tail = '\n' + indent * queue[0][0]  # for sibling open
		else:
			element.tail = '\n' + indent * (level - 1)  # for parent close
		queue[0:0] = children  # prepend so children come before siblings


kb.add_callback_button(label='Да', color=VkKeyboardColor.PRIMARY)
#ВСЯКИЕ ПЕРЕМЕННЫЕ_________________________
ban_var = 0

#КУРС ДОЛЛАРА
D_R_s = 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&aqs=chrome..69i57j0l7.6903j1j7&sourceid=chrome&ie=UTF-8'

#КУРС ЕВРO
E_R_s = 'https://www.google.com/search?sxsrf=ALeKk00RD7v7meADu6V95rm3NMil9ShKyA%3A1601561454902&ei=buN1X9W5NsmJrwTu7Z7QDA&q=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIKCAAQsQMQRhCCAjICCAAyDQgAELEDEIMBEBQQhwIyAggAMgIIADICCAAyAggAMgIIADIHCAAQFBCHAjICCAA6BAgjECc6BAguECc6BAgAEEM6BQgAELEDOgUILhCxAzoICC4QsQMQgwE6BwgAELEDEEM6CggAELEDEBQQhwI6CggAELEDEIMBEENQqA1Y2xtgjR1oAHABeACAAWWIAYIIkgEDOS4zmAEAoAEBqgEHZ3dzLXdpesABAQ&sclient=psy-ab&ved=0ahUKEwjVqOusyZPsAhXJxIsKHe62B8oQ4dU  DCA0&uact=5'

#КУРС БИТКОИНА
Bt_R_s = 'https://www.google.com/search?sxsrf=ALeKk03Jq5STjuZDpxj0XxQJnLBB7rvHoA%3A1601561305355&ei=2eJ1X-aZFc-RrgSLrITwBg&q=%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzICCAAyBwgAEBQQhwIyAggAMgIIADIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjoECCMQJzoECAAQQzoFCAAQsQM6BwgAELEDEEM6CggAELEDEBQQhwI6CAgAELEDEIMBOggILhCxAxCDAToKCAAQsQMQgwEQQzoJCAAQQxBGEIICOg8IABCxAxAUEIcCEEYQggJKBQgmEgFuSgUIJxIBMVD3KFiBPmC8VGgCcAF4AIABnQGIAYUMkgEEMTAuNZgBAKABAaoBB2d3cy13aXrAAQE&sclient=psy-ab&ved=0ahUKEwim6sPlyJPsAhXPiIsKHQsWAW4Q4dUDCA0&uact=5'

# Нг
ng = 'https://calculator888.ru/skolko-dney-do-novogo-goda'
# 23 фев
feb23 = 'https://calculator888.ru/skolko-dney/do-dnya-zashchitnika-otechestva'
# 8 март
mar8 = 'https://calculator888.ru/skolko-dney/mezhdunarodny-zhenskiy-den'
# 9 мая
may9 = 'https://calculator888.ru/skolko-dney/do-prazdnik-vesny'
# Лето
leto = 'https://calculator888.ru/skolko-dney-do-leta'

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}


#__________________________________________________
def write_mes(group_ID, message, attachment=None):
	if attachment == None:
		vk.method('messages.send', {
		    'chat_id': group_ID,
		    'message': message,
		    'random_id': get_random_id()
		})
	else:
		vk.method(
		    'messages.send', {
		        'attachment': attachment,
		        'chat_id': group_ID,
		        'random_id': get_random_id(),
		        'message': message
		    })


def write_mes_online(group_ID, message):
	vk.method(
	    'messages.send', {
	        'chat_id': group_ID,
	        'message': message,
	        'random_id': get_random_id(),
	        'disable_mentions': 1
	    })


def write_mes_img(group_ID, message):
	vk.method(
	    'messages.send', {
	        'chat_id': group_ID,
	        'message': message,
	        'random_id': get_random_id(),
	        'attachment': ','.join(attachments)
	    })


try:
	vk = vk_api.VkApi(token=settings['token'])
	longpoll = VkBotLongPoll(vk, group_id=settings['group_id'])
	bot_id = 0 - settings['group_id']
	admin_chat = 9
except:
	vk = vk_api.VkApi(token=settings['token2'])
	longpoll = VkBotLongPoll(vk, group_id=settings['group_id2'])
	bot_id = 0 - settings['group_id2']
	admin_chat = 2
	write_mes(admin_chat, 'Бот сменился на FT2')


def get_user(who):
	return vk.method('users.get', {'user_ids': who})


def get_group(id):
	return vk.method('groups.getById', {'group_ids': id})[0]


def ban_check(id):
	banned_list = db.keys()
	aaa = []
	id = str(id)
	for aa in banned_list:
		aaa.append(aa)
	if id in aaa:
		return False
	else:
		try:
			if id == str(auto_var):
				return 'оп ахах'
			else:
				return True
		except:
			return True


def time_pret(utime):
	return (datetime.utcfromtimestamp(utime) +
	        timedelta(hours=3)).strftime('%Y/%m/%d %H:%M:%S')


def balance_get(user):
	return cursor.execute(
	    f"SELECT cash FROM users WHERE id = {user}").fetchone()[0]


def lvl_get(user, group):
	return cursor.execute( f"SELECT user_status FROM a{group} WHERE user_ids = {user}").fetchone()[0]


def mes_count_get(user, group):
	return cursor.execute(
	    f"SELECT user_messages_count FROM a{group} WHERE user_ids = {user}"
	).fetchone()[0]


def nick_get(user, group):
	return cursor.execute(
	    f"SELECT user_nick FROM a{group} WHERE user_ids = {user}").fetchone(
	    )[0]


def info_get(user, group):
	return cursor.execute(
	    f"SELECT user_info FROM a{group} WHERE user_ids = {user}").fetchone(
	    )[0]


def status_get(user, group):
	return cursor.execute(
	    f"SELECT user_status FROM a{group} WHERE user_ids = {user}").fetchone(
	    )[0]


def warn_get(user, group, type_w=None):
	if type_w == None:
		return cursor.execute(
		    f"SELECT warns from a{group} WHERE user_ids = {user}").fetchone(
		    )[0]
	elif type_w == '-':
		cursor.execute(
		    f"UPDATE a{group} SET warns = warns - 1 WHERE user_ids = {user}")
	elif type_w == '+':
		cursor.execute(
		    f"UPDATE a{group} SET warns = warns + 1 WHERE user_ids = {user}")


def get_user_id(mention):
	j = list(mention)
	jj = j.index('|')
	try:
		while True:
			j.pop(jj)
	except:
		j.remove('[')
		j.remove('i')
		j.remove('d')
		j = ''.join(j)
		return j


def rate_get(user):
	return cursor.execute(
	    f"SELECT rate FROM users WHERE id = {user}").fetchone()[0]


def job_get(user):
	return cursor.execute(
	    f"SELECT job_place FROM users WHERE id = {user}").fetchone()[0]


def dk_get(group, name):
	return cursor.execute(
	    f"SELECT {name} FROM dk WHERE group_id = {group}").fetchone()[0]

def bank_bal_get(who):
	return cursor.execute(f"SELECT cash FROM bank WHERE id = {who}").fetchone()[0]


def admin_bot_get(id_b):
	try:
		if vk.method('messages.getConversationsById', {
		    'peer_ids': 2000000000 + id_b,
		    'extended': 1
		})['count'] != 0:
			chat_data = vk.method('messages.getConversationsById', {
			    'peer_ids': 2000000000 + id_b,
			    'extended': 1
			})['items'][0]
			chat_settings = chat_data['chat_settings']
			admins = chat_settings['admin_ids']
			a = 1
			return True
		else:
			a = 0
	except:
		write_mes(group_ID, f'Не могу получить доступ к {id_b}')
		a = 0
		return False

	if a == 1:
		for kk in cursor.execute("SELECT * FROM non_admin").fetchall():
			for ll in chat_settings['admin_ids']:
				if ll in kk and ll == bot_id * -1:
					cursor.execute(
					    f"UPDATE non_admin DELETE id WHERE id = {id_b}")
			if id_b == kk[0]:
				write_mes(group_ID, 'Дайте боту права администратора')
				return False
		return True
	else:
		return False


#DK________________
kick = ['кик', 'kick', '!kick', '!кик']
warn = ['+варн', '!варн', '+пред', '!пред', 'варн', 'пред']
ava = ['+ава', 'ава', '!ава']
role = ['+роль', '+админ', '!повысить', '!понизить', 'понизить', 'роль']

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
	id INT,
	cash BIGINT,
	job_time INT,
	job_place INT,
	rate INT
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS banned_users(
  id BIGINT
  )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS non_admin(
  id INT
)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS dk(
	group_id INT,
	kick INT,
	роль INT,
	ава INT,
	варн INT
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS property(
	id INT, 
	house INT, 
	phone INT, 
	car INT
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS invest(
	id INT,
	count INT
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS bank(
							id INT,
							cash INT,
							time INT
						)""")
						
starter = 1
connection.commit()
today = dt.datetime.today()
#if today.strftime("%M") == 0 or today.strftime("%M") == 00:
'''else:
  day = today.strftime("%d")
  hour = today.strftime("%H")
  minut = today.strftime("%M")
  print(day + ' ' + hour + ' ' + minut)'''

admins_bot_GG = [
    315625951, 550391377, 248693132, 273667139, 506465307, 139193247
]

keep_alive()
dima_var = 0
upload = VkUpload(vk)
print('Connection succesfull')
obn_var = []
obn_var_var = 0
var_alive = []

#attachments
dima_clicker = 'doc315625951_572401165'

write_mes(admin_chat, 'Бот включен')

error = [
    'video315625951_456239164', 'video315625951_456239157',
    'video315625951_456239158'
]
last_mes = 0
anti_spam = 0
anti_spam_var = 0
c6poc = 0

def get_chat(peer):
	return vk.method('messages.getConversationsById', {'peer_ids':2000000000 + peer, 'group_id':settings['group_id']})

def bal_pret(l):
	num = list(str(l))
	num.reverse()
	a = 0
	for i in num:
		a += 1
	count = a // 3
	ii = 3
	while count > 0:

		num.insert(ii, '.')
		count -= 1
		ii += 4
	num.reverse()
	if a % 3 == 0:
		num.pop(0)
	return (''.join(num))


def car_get(user):
	return cursor.execute(
	    f"SELECT car FROM property WHERE id = {user}").fetchone()[0]


def car_text_get(number):
	if number == 0:
		return 'Ноги'
	elif number == 1:
		return 'Тележка из Ашана'
	elif number == 2:
		return 'Велик'
	elif number == 3:
		return 'Гнилая шаха'
	elif number == 4:
		return 'Хендай Солярис'
	elif number == 5:
		return 'Ниссан Скайлайн'
	elif number == 6:
		return 'Тойота Марк 2'
	elif number == 7:
		return 'Мерседес CLS 2020'
	elif number == 8:
		return 'Тойота Камри'
	elif number == 9:
		return 'Тесла Модель S'
	elif number == 9:
		return 'Мерседес Гелендваген'
	elif number == 10:
		return 'Ламборгини Урус'
	elif number == 11:
		return 'Ламборгини Авентадор'
	elif number == 12:
		return 'Роллс-Ройс Куллинан'
	elif number == 13:
		return 'МакЛарен П1'


def car_price_get(number):
	if number == 1:
		return '5000'
	elif number == 2:
		return '15000'
	elif number == 3:
		return '50000'
	elif number == 4:
		return '100000'
	elif number == 5:
		return '250000'
	elif number == 6:
		return '600000'
	elif number == 7:
		return '1000000'
	elif number == 8:
		return '2500000'
	elif number == 9:
		return '5000000'
	elif number == 9:
		return '10000000'
	elif number == 10:
		return '17750000'
	elif number == 11:
		return '30000000'
	elif number == 12:
		return '75000000'
	elif number == 13:
		return '150000000'


def phone_get(user):
	return cursor.execute(
	    f"SELECT phone FROM property WHERE id = {user}").fetchone()[0]


def phone_text_get(number):
	if number == 0:
		return 'Телефон из Детского Мира'
	elif number == 1:
		return 'Nokia 3310'
	elif number == 2:
		return 'LG K100'
	elif number == 3:
		return 'Xiaomi Redmi 4'
	elif number == 4:
		return 'Samsung A11'
	elif number == 5:
		return 'Iphone SE'
	elif number == 6:
		return 'Samsung A50'
	elif number == 7:
		return 'Honor 9X'
	elif number == 8:
		return 'Iphone 7'
	elif number == 9:
		return 'Samsung Note 8'
	elif number == 10:
		return 'Huawei P40'
	elif number == 11:
		return 'Asus ROG phone 3'


def phone_price_get(number):
	if number == 1:
		return '500'
	elif number == 2:
		return '7500'
	elif number == 3:
		return '12000'
	elif number == 4:
		return '31000'
	elif number == 5:
		return '50000'
	elif number == 6:
		return '75000'
	elif number == 7:
		return '100000'
	elif number == 8:
		return '235000'
	elif number == 9:
		return '500000'
	elif number == 10:
		return '750000'
	elif number == 11:
		return '1500000'


def house_get(user):
	return cursor.execute(
	    f"SELECT house FROM property WHERE id = {user}").fetchone()[0]


def house_text_get(number):
	if number == 0:
		return 'Коробка из-под холодильника'
	elif number == 1:
		return 'Сарай из фанеры'
	elif number == 2:
		return 'Старый домик в деревне'
	elif number == 3:
		return 'Коммуналка в Химках'
	elif number == 4:
		return 'Кирпичный дом'
	elif number == 5:
		return 'Квартира в Мытищах'
	elif number == 6:
		return 'Кирпичный дом'
	elif number == 7:
		return 'Двухэтажный коттедж'
	elif number == 8:
		return 'Большой замок'
	elif number == 9:
		return 'Личный небоскрёб'


def house_price_get(number):
	if number == 1:
		return '1000'
	elif number == 2:
		return '10000'
	elif number == 3:
		return '50000'
	elif number == 4:
		return '250000'
	elif number == 5:
		return '1000000'
	elif number == 6:
		return '50000000'
	elif number == 7:
		return '100000000'
	elif number == 8:
		return '500000000'
	elif number == 9:
		return '1000000000'

def business_text_get(number):
	if number == 0:
		return 'Бизнеса нет'
	elif number == 1:
		return 'Продажа бабушкиных закаток 1.000/час'
	elif number == 2:
		return 'Ларек с шаурмой на вокзале 12.000/час'
	elif number == 3:
		return 'Магазин в Чебоксарах 78.000/час'
	elif number == 4:
		return 'Парикмахерская 460.000/час'
	elif number == 5:
		return 'Супермаркет в Звенигороде 2.900.000/час'
	elif number == 6:
		return 'Компьютерный клуб 57.000.000/час'
	elif number == 7:
		return 'Интернет-магазин 132.000.000/час'
	elif number == 8:
		return 'Агентство недвижимости 440.000.000/час'
	elif number == 9:
		return 'Научные лаборатории 820.000.000/час'
	elif number == 10:
		return 'Продажа воздуха на Марсе 8.000.000.000/час'

def get_bus_d(number):
	if number == 1:
		return 1000
	elif number == 2:
		return 12000
	elif number == 3:
		return 78000
	elif number == 4:
		return 460000
	elif number == 5:
		return 2900000
	elif number == 6:
		return 57000000
	elif number == 7:
		return 132000000
	elif number == 8:
		return 440000000
	elif number == 9:
		return 820000000
	elif number == 10:
		return 8000000000

def business_price_get(number):
	if number == 1:
		return 25000
	elif number == 2:
		return 250000
	elif number == 3:
		return 1250000
	elif number == 4:
		return 7250000
	elif number == 5:
		return 25000000
	elif number == 6:
		return 1250000000
	elif number == 7:
		return 2500000000
	elif number == 8:
		return 12500000000
	elif number == 9:
		return 25000000000
	elif number == 10:
		return 125500000000

def get_bus(who):
	return cursor.execute(f"SELECT * FROM business WHERE id = {who}").fetchall()[0]

def coins_get(who):
	return cursor.execute(f"SELECT count FROM invest WHERE id = {who}").fetchone()[0]

memes = ['video315625951_456239201','video315625951_456239202']
shav = '&#127791;'
while True:
	for event in longpoll.listen():
		if event.type == VkBotEventType.MESSAGE_NEW:  # and event.from_chat and event.message.get('text') != '':
			mes_time_u = event.object.message['date']

			mes_time = (datetime.utcfromtimestamp(event.object.message['date'])
			            + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
			u_id = event.object.message['from_id']
			group_ID = event.chat_id
			mes_text_syntax = (event.message.get('text')).split()
			mes_text = (event.message.get('text')).lower().split()
			if last_mes == event.message.get('text') and last_mes != '':
				if anti_spam == 0:
					anti_spam_var = u_id
					anti_spam += 1
				elif anti_spam >= 1 and anti_spam_var == u_id:
					anti_spam += 1
					if anti_spam == 3:
						write_mes(group_ID, 'Не спамь')
					elif anti_spam == 5:

						anti_spam_var = 0
						anti_spam = 0
						write_mes(group_ID, 'Кик за спам')
						try:
							vk.method('messages.removeChatUser', {
							    'chat_id': group_ID,
							    'member_id': u_id
							})
						except:
							write_mes(group_ID,
							          'Не получается удалить пользователя')
			last_mes = event.message.get('text')
			if event.message.get('text') == '':
				mes_text = ['123123123123', '123123123123']

			if event.from_chat:
				# if mes_text[0] == 'спасибо':
				# 	try:
				# 		if mes_text[1] in ['на'] and mes_text[2] in ['хлеб']:
				# 			write_mes(group_ID, 'Спасибо теперь можно мазать на хлеб!')
				# 	except:
				# 		pass
				if 1 == 1 and u_id > 0:
					if admin_chat == 9 or group_ID in [1, 2, 9]:
						try:
							abh = vk.method(
							    'messages.getConversationMembers',
							    {'peer_id': 2000000000 + group_ID})['items']
							#запись даных в БД
							try:
								if cursor.execute(f"SELECT * FROM a{group_ID}"
								                  ).fetchall() == []:
									print(1 / 0)
							except:
								write_mes(group_ID,
								          'Идёт запись в базу данных...')
								print(1)
								cursor.execute(
								    f"""CREATE TABLE IF NOT EXISTS a{group_ID}(
                  user_ids INT,
                  user_status INT,
                  user_messages_count INT,
                  user_nick TEXT,
                  user_info TEXT
                )""")
								connection.commit()
								print(2)
								cursor.execute(
								    "INSERT INTO dk VALUES (?,?,?,?,?)",
								    (group_ID, 0, 0, 0, 0))
								print(3)
								connection.commit()
								a = []
								print('a')
								if cursor.execute(
								    f"SELECT user_ids FROM a{group_ID}"
								).fetchall() == []:
									for ids in cursor.execute(
									    f"SELECT user_ids FROM a{group_ID}"
									).fetchall():
										print(142)
										a.append(ids[0])
									abh = vk.method(
									    'messages.getConversationMembers',
									    {'peer_id': 2000000000 + group_ID
									     })['items']
									for user in abh:

										print(1552)
										user_var = user['member_id']
										if user_var not in a:
											if user_var > 0:
												namE = get_user(
												    user_var)[0]['first_name']
												cursor.execute(
												    f"INSERT INTO a{group_ID} VALUES (?, ?, ?, ?, ?)",
												    (user_var, 0, 0, namE,
												     'Пусто'))
												print(123)
												connection.commit()
									write_mes(group_ID, 'Готово!')
						except:
							break
					if admin_chat == 9 or group_ID in [1, 2, 9]:
						cursor.execute(
						    f"UPDATE a{group_ID} SET user_messages_count = user_messages_count + 1 WHERE user_ids = {u_id}"
						)
						connection.commit()

						if cursor.execute( f"SELECT user_status FROM a{group_ID} WHERE user_ids = {u_id}").fetchone() == None:
							cursor.execute(f"INSERT INTO a{group_ID} VALUES(?,?,?,?,?)", (u_id, 0, 0, 0, 0))

					if cursor.execute(f'SELECT * FROM users WHERE id = {u_id}'
					                  ).fetchone() is None and u_id != bot_id:
						print(2)
						cursor.execute(
						    f"INSERT INTO users VALUES (?, ?, ?, ?, ?)",
						    (u_id, 0, 0, 1, 0))
						connection.commit()
						print(3)

					if cursor.execute(
					    f'SELECT * FROM property WHERE id = {u_id}').fetchone(
					    ) is None and (admin_chat == 9 or
					                   group_ID in [1, 9]) and u_id != bot_id:
						print('Новый владелец имущества' + get_user(u_id))
						cursor.execute(
						    f"INSERT INTO property VALUES (?, ?, ?, ?)",
						    (u_id, 0, 0, 0))
						connection.commit()
					if cursor.execute(f"SELECT * FROM business WHERE id = {u_id}").fetchall() == []:
						cursor.execute(f"INSERT INTO business VALUES (?,?,?)", (u_id, 0, 0))
						connection.commit()
						print('новый владелец бизнесов')

					if cursor.execute(f"SELECT * FROM invest WHERE id = {u_id}").fetchall() == []:
						cursor.execute(f"INSERT INTO invest VALUES (?,?)", (u_id, 0))
						connection.commit()

					if cursor.execute(f"SELECT * FROM bank WHERE id = {u_id}").fetchall() == []:
						cursor.execute(f"INSERT INTO bank VALUES(?,?,?)", (u_id, 0, mes_time_u))

						print('новый инвестор')
					if event.object.message['attachments'] != []:
						print('1')
						try:
							if event.object.message['attachments'][0]['type'] == 'audio':
								write_mes(group_ID, 'Оудап качает', 'video315625951_456239200')
								print('2')
						except:
							continue

					if mes_text[0] == 'дима':
						if ban_check(u_id) == True:
							if group_ID in [1, 11]:
								n = random.randint(1, 12)
								img = 'images/дима/' + str(n) + '.jpg'
								attachments = []
								upload_img = upload.photo_messages(
								    photos=img)[0]
								attachments.append('photo{}_{}'.format(
								    upload_img['owner_id'], upload_img['id']))
								print(attachments)
								write_mes_img(group_ID, 'HTML для лохов)')
						elif ban_check(u_id) == False:
							write_mes(group_ID, 'Фейспалм чел ты в муте')
					elif mes_text[0] == 'очир' or 'бурятия' in mes_text:
						if ban_check(u_id) == True:
							if group_ID in [1, 11]:
								n = random.randint(1, 17)
								if n in range(13, 18):
									part1 = 'Yнгын дайдаар, хангай тайгаар нэмжыгшэ\nҮлзы Буряад — манай нангин үлгы.\nСэлмэг сарюун, сэнхир номин шарайшни\nСэдьхэлдэмнай хэзээдэшье зулгы'
									part2 = 'Эрхим хангал санзай шэнги агаарташ\nЭршэ хүсөөр элсүүлэнгүй яалайб!\nЭмтэй домтой мүнхын уһан аршаандаш\nЭльгэ зүрхөө хүртүүлэнгүй яалайб!'
									part3 = 'Холын замда эхын ёһоор юрөөжэ,\nХүмүүн зондо хэтын жаргал хүсөөш.\nСаяан хадын сэлгеэн амяар арюудхан,\nАршин далайн гэгээн долгёор сүршөөш.'
									part4 = 'Шэрүүн сагай ерээшье һаа дэлхэйдэ,\nШинии заяан замһаа хадуурхагүйл.\nЭбтэй дорюун бүлын ёһоор жаргыш даа,\nЭнхэ Буряад манай нангин үлгы.'
									part5 = 'Эхэ нютаг!'
									write_mes(
									    group_ID, f'{part1}\n\n' +
									    f'{part2}\n\n' + f'{part3}\n\n' +
									    f'{part4}\n\n' + f'{part5}')
								else:
									img = 'images/очир/' + str(n) + '.jpg'
									attachments = []
									upload_img = upload.photo_messages(
									    photos=img)[0]
									attachments.append('photo{}_{}'.format(
									    upload_img['owner_id'],
									    upload_img['id']))
									write_mes_img(
									    group_ID,
									    'Бурятия сила!&#128170;&#128170;&#128170;'
									)
						elif ban_check(u_id) == False:
							write_mes(group_ID, 'Фейспалм чел ты в муте')
						else:
							write_mes(
							    group_ID,
							    'Я должен тебе отвечать что-то умное, но мне еще это не добавили)'
							)
					elif mes_text[0] == 'вадик':
						if ban_check(u_id) == True:
							if group_ID in [1, 11]:
								n = random.randint(1, 10)
								img = 'images/вадик/' + str(n) + '.jpg'
								attachments = []
								upload_img = upload.photo_messages(
								    photos=img)[0]
								if random.randint(0, 1) == 0:
									attachments.append('photo{}_{}'.format(
									    upload_img['owner_id'],
									    upload_img['id']))
									vad_list = [
									    'Бахнув пельменей',
									    '- Это что?\n- Вам честно?\n- Да, конечно\n- Я сам не знаю...'
									]
									write_mes_img(
									    group_ID, vad_list[random.randint(
									        0, 1)])
									continue
								else:
									attachments.append(
									    'video208445918_456240131')
									vad_list = [
									    'Бахнув пельменей',
									    '- Это что?\n- Вам честно?\n- Да, конечно\n- Я сам не знаю...'
									]
									write_mes_img(
									    group_ID, vad_list[random.randint(
									        0, 1)])

						elif ban_check(u_id) == False:
							write_mes(group_ID, 'Фейспалм чел ты в муте')
						else:
							write_mes(
							    group_ID,
							    'Я должен тебе отвечать что-то умное, но мне еще это не добавили)'
							)

					elif mes_text[0] == 'мадина':
						if ban_check(u_id) == True:
							if group_ID in [1, 11]:
								n = random.randint(1, 10)
								img = 'images/мадина/' + str(n) + '.jpg'
								attachments = []
								upload_img = upload.photo_messages(
								    photos=img)[0]
								attachments.append('photo{}_{}'.format(
								    upload_img['owner_id'], upload_img['id']))
								write_mes_img(group_ID, '*кродется*')
						elif ban_check(u_id) == False:
							write_mes(group_ID, 'Фейспалм чел ты в муте')
					elif mes_text[0] in [
					    'артем', 'артём', 'тема', 'тёма', 'артемий'
					]:
						if ban_check(u_id) == True:
							if group_ID in [1, 11]:
								anek_list = {
								    1:
								    'Не могу представить себе событие в мире, после которого не упал бы курс рубля.',
								    2:
								    'Один городской тип купил поселок. Теперь это поселок городского типа.',
								    3:
								    'Группа умных альпинистов обошла Эверест.',
								    4:
								    'Тимуровцы-хулиганы переводят бабушек через дорогу в неположенном месте.',
								    5:
								    'Интересный факт: самый сильный футболист "Балтики" играет под девятым номером.',
								    6:
								    'На сочинском пляже дельфин спас человека, отговорив его покупать чебурек.',
								    7:
								    '83.3% британских учёных доказали, что «русская рулетка» совершенно безопасна. Остальные 16.7% исследователей, к сожалению, не смогли принять участие в итоговом обсуждении данного вопроса.',
								    8:
								    'Наркоман Олег, чтобы не спалиться, придя домой, сделал вид, что это не он.',
								    9:
								    'Новые батарейки "Дети прокуроров". "Дети прокуроров" никогда не сядут.',
								    10:
								    'В маршрутке, набитой чиновниками, деньги до водителя так и не дошли.',
								    11:
								    'Во всем можно найти плюсы. Например, доллар по 100 будет намного удобнее считать в уме!',
								    12:
								    'Петросян но не Евгений',
								    13:
								    'Петросян но не Евгений',
								    14:
								    'Петросян но не Евгений',
								    15:
								    'Петросян но не Евгений'
								}
								n = random.randint(1, 10)
								i = random.randint(1, 15)
								img = 'images/артем/' + str(n) + '.jpg'
								attachments = []
								upload_img = upload.photo_messages(
								    photos=img)[0]
								attachments.append('photo{}_{}'.format(
								    upload_img['owner_id'], upload_img['id']))
								write_mes_img(group_ID, anek_list[i])
						elif ban_check(u_id) == False:
							write_mes(group_ID, 'Фейспалм чел ты в муте')
						else:
							write_mes(
							    group_ID,
							    'Я должен тебе отвечать что-то умное, но мне еще это не добавили)'
							)

					if mes_text[0] in ['ку', 'привет', 'дарова', 'прив', 'hi']:
						hi_mes = ['Привет!', 'Пакет', 'Дарова че снилось']
						hi_var_mes = random.randint(0, 2)
						write_mes(group_ID, hi_mes[hi_var_mes])
						linked()
					elif mes_text[0] in ['пока']:
						write_mes(group_ID, 'Никто не будет по тебе скучать!')
						linked()

					elif mes_text[0] == '!тайм':
						prep_list = []
						vk.method('messages.setActivity', {
						    'type': 'typing',
						    'peer_id': 2000000000 + group_ID
						})
						ng_k = requests.get(ng, headers=headers)
						ng_soup = BeautifulSoup(ng_k.content, 'html.parser')
						ng_dn = ng_soup.find("span", {'id': 'den_dan'})
						ng_dn1 = ng_soup.find("span", {'id': 'dni_skl'})
						ng_ch = ng_soup.find("span", {'id': 'chs_dan'})
						ng_ch1 = ng_soup.find("span", {'id': 'chs_skl'})

						ng_mi = ng_soup.find("span", {'id': 'min_dan'})

						ng_mi1 = ng_soup.find("span", {'id': 'min_skl'})

						ng_sec = ng_soup.find("span", {'id': 'sec_dan'})

						ng_sec1 = ng_soup.find("span", {'id': 'sec_skl'})
						prep_list.append(
						    f'&#127876; До нг {ng_dn.text} {ng_dn1.text} {ng_ch.text} {ng_ch1.text} {ng_mi.text} {ng_mi1.text} {ng_sec.text} {ng_sec1.text}'
						)
						print('ng ready')

						feb23_k = requests.get(feb23, headers=headers)
						feb23_soup = BeautifulSoup(feb23_k.content,
						                           'html.parser')
						feb23_dn = feb23_soup.find("span", {'id': 'den_dan'})
						feb23_dn1 = feb23_soup.find("span", {'id': 'dni_skl'})
						feb23_ch = feb23_soup.find("span", {'id': 'chs_dan'})

						feb23_ch1 = feb23_soup.find("span", {'id': 'chs_skl'})

						feb23_mi = feb23_soup.find("span", {'id': 'min_dan'})

						feb23_mi1 = feb23_soup.find("span", {'id': 'min_skl'})

						feb23_sec = feb23_soup.find("span", {'id': 'sec_dan'})

						feb23_sec1 = feb23_soup.find("span", {'id': 'sec_skl'})
						prep_list.append(
						    f'&#127895; До 23 февраля {feb23_dn.text} {feb23_dn1.text} {feb23_ch.text} {feb23_ch1.text} {feb23_mi.text} {feb23_mi1.text} {feb23_sec.text} {feb23_sec1.text}'
						)
						print('feb23 ready')

						mar8_k = requests.get(mar8, headers=headers)
						mar8_soup = BeautifulSoup(mar8_k.content,
						                          'html.parser')
						mar8_dn = mar8_soup.find("span", {'id': 'den_dan'})
						mar8_dn1 = mar8_soup.find("span", {'id': 'dni_skl'})
						print(mar8_dn1)
						mar8_ch = mar8_soup.find("span", {'id': 'chs_dan'})
						print(mar8_ch)

						mar8_ch1 = mar8_soup.find("span", {'id': 'chs_skl'})
						print(mar8_ch1)

						mar8_mi = mar8_soup.find("span", {'id': 'min_dan'})
						print(mar8_mi)
						mar8_mi1 = mar8_soup.find("span", {'id': 'min_skl'})
						print(mar8_mi1)

						mar8_sec = mar8_soup.find("span", {'id': 'sec_dan'})
						print(mar8_sec)

						mar8_sec1 = mar8_soup.find("span", {'id': 'sec_skl'})

						print(mar8_sec1)
						prep_list.append(
						    f'&#128144; До 8 марта {mar8_dn.text} {mar8_dn1.text} {mar8_ch.text} {mar8_ch1.text} {mar8_mi.text} {mar8_mi1.text} {mar8_sec.text} {mar8_sec1.text}'
						)
						print('mar8 ready')

						may9_k = requests.get(may9, headers=headers)
						may9_soup = BeautifulSoup(may9_k.content,
						                          'html.parser')
						may9_dn = may9_soup.find("span", {'id': 'den_dan'})
						may9_dn1 = may9_soup.find("span", {'id': 'dni_skl'})
						may9_ch = may9_soup.find("span", {'id': 'chs_dan'})

						may9_ch1 = may9_soup.find("span", {'id': 'chs_skl'})

						may9_mi = may9_soup.find("span", {'id': 'min_dan'})

						may9_mi1 = may9_soup.find("span", {'id': 'min_skl'})

						may9_sec = may9_soup.find("span", {'id': 'sec_dan'})

						may9_sec1 = may9_soup.find("span", {'id': 'sec_skl'})
						prep_list.append(
						    f'&#127894; До 9 мая {str(int(may9_dn.text) + 8)} {may9_dn1.text} {may9_ch.text} {may9_ch1.text} {may9_mi.text} {may9_mi1.text} {may9_sec.text} {may9_sec1.text}'
						)
						print('may9 ready')

						leto_k = requests.get(leto, headers=headers)
						leto_soup = BeautifulSoup(leto_k.content,
						                          'html.parser')
						leto_dn = leto_soup.find("span", {'id': 'den_dan'})
						leto_dn1 = leto_soup.find("span", {'id': 'dni_skl'})
						leto_ch = leto_soup.find("span", {'id': 'chs_dan'})

						leto_ch1 = leto_soup.find("span", {'id': 'chs_skl'})

						leto_mi = leto_soup.find("span", {'id': 'min_dan'})

						leto_mi1 = leto_soup.find("span", {'id': 'min_skl'})

						leto_sec = leto_soup.find("span", {'id': 'sec_dan'})

						leto_sec1 = leto_soup.find("span", {'id': 'sec_skl'})
						prep_list.append(
						    f'&#128526; До лета {leto_dn.text} {leto_dn1.text} {leto_ch.text} {leto_ch1.text} {leto_mi.text} {leto_mi1.text} {leto_sec.text} {leto_sec1.text}'
						)
						print('leto ready')
						write_mes(group_ID, '\n\n'.join(prep_list))

					elif mes_text[0] == 'курс':
						linked()
						if ban_check(u_id) == True:
							try:
								if mes_text[1] == '1':
									vk.method(
									    'messages.send', {
									        'attachment':
									        'doc315625951_572401165',
									        'chat_id':
									        group_ID,
									        'random_id':
									        get_random_id()
									    })
									vk.method(
									    'messages.setActivity', {
									        'type': 'typing',
									        'peer_id': 2000000000 + group_ID
									    })
									full_page = requests.get(
									    D_R_s, headers=headers)
									soup = BeautifulSoup(
									    full_page.content, 'html.parser')
									convert = soup.findAll(
									    "span", {
									        "class": "DFlfde",
									        "class": "SwHCTb",
									        "data-precision": "2"
									    })
									dol_rub = (convert[0].text)
									write_mes(group_ID,
									          f'Курс доллара: {dol_rub}₽')
								elif mes_text[1] == '2':
									vk.method(
									    'messages.send', {
									        'attachment':
									        'doc315625951_572401165',
									        'chat_id':
									        group_ID,
									        'random_id':
									        get_random_id()
									    })
									vk.method(
									    'messages.setActivity', {
									        'type': 'typing',
									        'peer_id': 2000000000 + group_ID
									    })
									full_page = requests.get(
									    E_R_s, headers=headers)
									soup = BeautifulSoup(
									    full_page.content, 'html.parser')
									convert = soup.findAll(
									    "span", {
									        "class": "DFlfde",
									        "class": "SwHCTb",
									        "data-precision": "2"
									    })
									eur_rub = (convert[0].text)
									write_mes(group_ID,
									          f'Курс евро: {eur_rub}₽')
									ii = 3
								elif mes_text[1] == '3':
									vk.method(
									    'messages.send', {
									        'attachment':
									        'doc315625951_572401165',
									        'chat_id':
									        group_ID,
									        'random_id':
									        get_random_id()
									    })
									vk.method(
									    'messages.setActivity', {
									        'type': 'typing',
									        'peer_id': 2000000000 + group_ID
									    })
									full_page = requests.get(
									    Bt_R_s, headers=headers)
									soup = BeautifulSoup(
									    full_page.content, 'html.parser')
									convert = soup.findAll(
									    "span", {
									        "class": "DFlfde",
									        "class": "SwHCTb",
									        "data-precision": "2"
									    })
									btc_rub = (convert[0].text)
									write_mes(group_ID,
									          f'Курс биткоина: {btc_rub}₽')
									ii = 3
								else:
									write_mes(
									    group_ID,
									    'Выбран некорректный тип валюты. 1- Доллар, 2 - Евро, 3 -Биткоин.'
									)
							except IndexError:
								write_mes(
								    group_ID,
								    'Выберите тип валюты. 1 - Доллар, 2 - Евро, 3 - Биткоин.'
								)
						elif ban_check(u_id) == False:
							write_mes(group_ID, 'Фейспалм чел ты в муте')
						else:
							write_mes(
							    group_ID,
							    'Я должен тебе отвечать что-то умное, но мне еще это не добавили)'
							)

					elif mes_text[0] == 'читать' and mes_text[1] == 'науку':
						linked()
						if ban_check(u_id) == True:
							write_mes(
							    group_ID,
							    f'[id{event.object.message["from_id"]}|Пользователь] читает науку&#128214;'
							)
						elif ban_check(u_id) == False:
							write_mes(group_ID, 'Фейспалм чел ты в муте')
						else:
							write_mes(
							    group_ID,
							    'Я должен тебе отвечать что-то умное, но мне еще это не добавили)'
							)

					elif mes_text[0] == 'console_inf':
						linked()
						sender = (event.object.message['from_id'])
						if sender == 536969746 or sender == 315625951:
							print(event.object.message)
							write_mes(group_ID, event.object.message)
							write_mes(group_ID,
							          f'ID группы в боте: {group_ID}')
							print('****************************************')
							print('________________________________________')
						else:
							write_mes(group_ID, 'Вы не являетесь админом бота')

					elif mes_text[0] == 'инфа':
						linked()
						if ban_check(u_id) == True:
							try:
								mes_text.remove('инфа')
								if mes_text[1] == '' or mes_text[1] == ' ':
									1 / 0
								g = ' '.join(mes_text)
								rnd = random.randint(0, 100)
								write_mes(
								    group_ID,
								    'Я думаю, что вероятность того, что ' +
								    str(g) + ',равна ' + str(rnd) + '%')
							except:
								otvet = 'Что-то пошло не так...'
								vk.method(
								    'messages.send', {
								        'chat_id': group_ID,
								        'message': otvet,
								        'random_id': get_random_id(),
								        'attachment':
								        'video315625951_456239157'
								    })
						elif ban_check(u_id) == False:
							write_mes(group_ID, 'Фейспалм чел ты в муте')
						else:
							write_mes(
							    group_ID,
							    'Я должен тебе отвечать что-то умное, но мне еще это не добавили)'
							)

					elif mes_text[0] in ['+ава', '+аватарка']:
						linked()
						if ban_check(u_id) == True:
							members = vk.method(
							    'messages.getConversationMembers',
							    {'peer_id': 2000000000 + group_ID})
							for i in members["items"]:
								admin = i.get('is_admin', False)
								if i["member_id"] == event.object.message[
								    "from_id"]:
									if admin == True or u_id == 315625951 or status_get(
									    u_id, group_ID) >= 1:

										n = random.randint(1, 20)
										#	img = 'images/авки/' + str(n) + '.jpg'
										upload_rez = vk.method(
										    'photos.getChatUploadServer', {
										        'chat_id': group_ID,
										        'crop_x': 10000,
										        'crop_y': 10000,
										        'crop_width': 20000
										    })

										imagePath = 'images/авки/' + str(
										    n) + '.png'
										img = {
										    'file':
										    ('images/авки/' + str(n) + '.jpg',
										     open(imagePath, 'rb'))
										}

										photo_upload_response = requests.post(
										    upload_rez['upload_url'],
										    files=img)
										photo_upload_result = json.loads(
										    photo_upload_response.text)
										try:
											vk.method(
											    'messages.setChatPhoto', {
											        'file':
											        photo_upload_result[
											            'response']
											    })
										except:
											write_mes(
											    group_ID,
											    'Предоставьте доступ на изменение информации беседы'
											)
									else:
										gender = vk.method(
										    'users.get', {
										        'user_ids':
										        event.object.
										        message["from_id"],
										        'fields':
										        'sex'
										    })
										if gender[0]['sex'] == 1:
											write_mes(group_ID,
											          'Ты кто вообще такая?')
										elif gender[0]['sex'] == 2:
											write_mes(group_ID,
											          'Ты кто вообще такой?')
										else:
											write_mes(
											    group_ID,
											    'У тебя скрыт пол, поэтому я спрошу ТЫ ЧТО ВООБЩЕ ТАКОЕЕЕ???'
											)
						elif ban_check(u_id) == False:
							write_mes(group_ID, 'Фейспалм чел ты в муте')
						else:
							write_mes(
							    group_ID,
							    'Я должен тебе отвечать что-то умное, но мне еще это не добавили)'
							)

					elif mes_text[0] in ['!adm', '!admin', '!админ', '!адм']:
						linked()
						if ban_check(u_id) == True:
							members = vk.method(
							    'messages.getConversationMembers',
							    {'peer_id': 2000000000 + group_ID})
							for i in members["items"]:
								if i["member_id"] == event.object.message[
								    "from_id"]:
									img_t = 'images/admins/2.jpg'
									img_f = 'images/admins/1.jpg'
									admin = i.get('is_admin', False)
									attachments = []
									if admin == True or status_get(
									    u_id, group_ID) >= 1:
										upload_img = upload.photo_messages(
										    photos=img_t)[0]
										attachments.append('photo{}_{}'.format(
										    upload_img['owner_id'],
										    upload_img['id']))
										write_mes_img(
										    group_ID,
										    'Это батюшка, я всьо проверил')
									else:
										upload_img = upload.photo_messages(
										    photos=img_f)[0]
										attachments.append('photo{}_{}'.format(
										    upload_img['owner_id'],
										    upload_img['id']))
										write_mes_img(group_ID, 'Пишов вон')
						elif ban_check(u_id) == False:
							write_mes(group_ID, 'Фейспалм чел ты в муте')
						else:
							write_mes(
							    group_ID,
							    'Я должен тебе отвечать что-то умное, но мне еще это не добавили)'
							)
					elif mes_text[0] in ['!kick']:
						linked()
						if ban_check(u_id) == True:
							if admin_bot_get(group_ID):
								members = vk.method(
								    'messages.getConversationMembers',
								    {'peer_id': 2000000000 + group_ID})
								for i in members["items"]:
									admin = i.get('is_admin', False)
									if i["member_id"] == event.object.message[
									    "from_id"]:
										try:
											if admin == True or status_get(
											    u_id, group_ID) >= dk_get(
											        group_ID, 'kick'):
												p = event.message[
												    'text'].split()
												j = list(p[1])
												jj = j.index('|')
												try:
													while True:
														j.pop(jj)
												except:
													j.remove('[')
													j.remove('i')
													j.remove('d')
													j = ''.join(j)
													try:
														int(j)
														gg = 0
													except:
														gg = 1
												if int(
												    j
												) in admins_bot_GG and gg == 0:
													write_mes(
													    group_ID,
													    'Я не буду кикать этого хорошего человека!!!'
													)
												else:
													write_mes(
													    group_ID,
													    'Кикаю дауна...')
													try:
														vk.method(
														    'messages.removeChatUser',
														    {
														        'chat_id':
														        group_ID,
														        'member_id':
														        j
														    })
													except:
														otvet = 'Упс, что-то пошло не так'
														vk.method(
														    'messages.send', {
														        'chat_id':
														        group_ID,
														        'message':
														        otvet,
														        'random_id':
														        get_random_id(
														        ),
														        'attachment':
														        'video315625951_456239157'
														    })
														continue
											else:
												gender = vk.method(
												    'users.get', {
												        'user_ids':
												        event.object.
												        message["from_id"],
												        'fields':
												        'sex'
												    })
												if gender[0]['sex'] == 1:
													write_mes(
													    group_ID,
													    'Ты кто вообще такая?')
												elif gender[0]['sex'] == 2:
													write_mes(
													    group_ID,
													    'Ты кто вообще такой?')
												else:
													write_mes(
													    group_ID,
													    'У тебя скрыт пол, поэтому я спрошу ТЫ ЧТО ВООБЩЕ ТАКОЕЕЕ???'
													)
										except:
											vk.method(
											    'messages.send', {
											        'chat_id':
											        group_ID,
											        'message':
											        'Упс ахах',
											        'random_id':
											        get_random_id(),
											        'attachment':
											        'video315625951_456239157'
											    })
						elif ban_check(u_id) == False:
							write_mes(group_ID, 'Фейспалм чел ты в муте')
						else:
							write_mes(
							    group_ID,
							    'Я должен тебе отвечать что-то умное, но мне еще это не добавили)'
							)

					elif mes_text[0] in ['ping']:
						linked()
						if ban_check(u_id) == True:
							write_mes(group_ID, 'PONG')
						elif ban_check(u_id) == False:
							write_mes(group_ID, 'Фейспалм чел ты в муте')
						else:
							write_mes(
							    group_ID,
							    'Я должен тебе отвечать что-то умное, но мне еще это не добавили)'
							)

					elif mes_text[0] in ['цитата', 'цит']:
						linked()
						if ban_check(u_id) == True:
							try:
								rep_text = event.object.message[
								    'reply_message']['text']
								nnn = 0
								for literals in rep_text:
									nnn += 1
								if nnn >= 35:
									rep_text = list(rep_text)
									if nnn >= 65:
										a = 'Сообщение слишком длинное, попробуйте другое'
										vk.method(
										    'messages.send', {
										        'chat_id':
										        group_ID,
										        'message':
										        a,
										        'random_id':
										        get_random_id(),
										        'attachment':
										        'video315625951_456239157'
										    })

									else:
										rep_text.reverse()
										space = rep_text.index(' ')
										rep_text.remove(' ')
										rep_text.insert(space, '\n')
										rep_text.reverse()
										a = ''.join(rep_text)
								else:
									a = ''.join(rep_text)

								img = Image.open('images/pyllow.png')
								font = ImageFont.truetype('19847.otf', size=70)
								draw_text = ImageDraw.Draw(img)
								draw_text.text(
								    (120, 250),
								    a,
								    # Добавляем шрифт к изображению
								    font=font,
								    fill='#000000')
								img.save('fraza.jpg')
								attachments = []
								upload_img = upload.photo_messages(
								    photos='fraza.jpg')[0]
								attachments.append('photo{}_{}'.format(
								    upload_img['owner_id'], upload_img['id']))
								write_mes_img(group_ID, 'Ауф&#9757;')
							except:
								#sender = (event.object.message['from_id'])
								#if sender == 536969746 or sender == 315625951:
								mes_text_syntax.remove(mes_text_syntax[0])
								mes_text_syntax_1 = mes_text_syntax
								mes_text_syntax = ' '.join(mes_text_syntax)
								#try:

								nnn = 0
								for literals in mes_text_syntax:
									nnn += 1
								if nnn >= 35:
									mes_text = list(mes_text_syntax)
									if nnn >= 65:
										otvet = 'Сообщение слишком длинное, попробуйте другое'
										vk.method(
										    'messages.send', {
										        'chat_id':
										        group_ID,
										        'message':
										        otvet,
										        'random_id':
										        get_random_id(),
										        'attachment':
										        'video315625951_456239157'
										    })
									else:

										mes_text_syntax_1.reverse()
										space = mes_text_syntax_1.index(' ')
										mes_text_syntax_1.remove(' ')
										mes_text_syntax_1.insert(space, '\n')
										mes_text_syntax_1.reverse()
										a = ''.join(mes_text_syntax_1)
								else:
									a = ''.join(mes_text_syntax)

								img = Image.open('images/pyllow.png')
								font = ImageFont.truetype('19847.otf', size=70)
								draw_text = ImageDraw.Draw(img)
								draw_text.text(
								    (120, 250),
								    a,
								    # Добавляем шрифт к изображению
								    font=font,
								    fill='#000000')
								img.save('fraza.jpg')
								attachments = []
								upload_img = upload.photo_messages(
								    photos='fraza.jpg')[0]
								attachments.append('photo{}_{}'.format(
								    upload_img['owner_id'], upload_img['id']))
								write_mes_img(group_ID, 'Ауф&#9757;')
						elif ban_check(u_id) == False:
							write_mes(group_ID, 'Фейспалм чел ты в муте')
						else:
							write_mes(
							    group_ID,
							    'Я должен тебе отвечать что-то умное, но мне еще это не добавили)'
							)

					elif mes_text[0] in ['онлайн', 'online']:
						linked()
						if ban_check(u_id) == True:
							user_inf = vk.method(
							    'messages.getConversationMembers', {
							        'peer_id': 2000000000 + group_ID,
							        'group_id': group_ID
							    })
							users_online_list = []
							n = 0
							a = 0
							for user in user_inf['profiles']:
								if user_inf['profiles'][n]['online_info'][
								    'visible'] == False:
									a += 1
								else:
									if user_inf['profiles'][n]['online_info'][
									    'is_online'] == True:
										if user_inf['profiles'][n][
										    'online_info'][
										        'is_mobile'] == True:
											users_online_list.append(
											    f'&#128241; [id{user_inf["profiles"][n]["id"]}|{user_inf["profiles"][n]["first_name"]}]'
											)
										else:
											users_online_list.append(
											    f'&#128421; [id{user_inf["profiles"][n]["id"]}|{user_inf["profiles"][n]["first_name"]}]'
											)
								n += 1
							result_online = '\n'.join(users_online_list)
							if a == 0:
								write_mes_online(
								    group_ID,
								    f'Список пользователей онлайн:\n{result_online}'
								)
							elif a == 1:
								write_mes_online(
								    group_ID,
								    f'Список пользователей онлайн:\n{result_online}\nИ еще 1 пользователь скрывает онлайн'
								)
							elif a % 10 in [2, 3, 4] and a not in range(
							    10, 21):
								write_mes_online(
								    group_ID,
								    f'Список пользователей онлайн:\n{result_online}\nИ еще {a} пользователя скрываю онлайн'
								)
							else:
								write_mes_online(
								    group_ID,
								    f'Список пользователей онлайн:\n{result_online}\nИ еще {a} пользователей скрывают онлайн'
								)

						elif ban_check(u_id) == False:
							write_mes(group_ID, 'Фейспалм чел ты в муте')
						else:
							write_mes(
							    group_ID,
							    'Я должен тебе отвечать что-то умное, но мне еще это не добавили)'
							)

					elif mes_text[0] in ['!botban']:
						linked()
						if event.object.message['from_id'] in admins_bot_GG:
							try:
								j = list(mes_text[1])
								jj = j.index('|')
								try:
									mes_text.append['слово_в_конце_ахах']
									reas_var = ' '.join(mes_text[2:-1])
								except:
									reas_var = 'причина не указана'
								try:
									while True:
										j.pop(jj)
								except:
									j.remove('[')
									j.remove('i')
									j.remove('d')
									j = ''.join(j)
								try:
									if mes_text[2:-1] == []:
										1 / 0
									else:
										reas_var = ' '.join(mes_text[2:-1])
								except:
									reas_var = 'причина не указана'
								vk.method(
								    'messages.send', {
								        'chat_id': group_ID,
								        'message': 'Вы уверены?',
								        'random_id': get_random_id(),
								        'keyboard': kb.get_keyboard()
								    })
								# just_ban(j, reas_var)
								ban_var = 1
							except:
								vk.method(
								    'messages.send', {
								        'chat_id': group_ID,
								        'message': 'Вася кого банить?',
								        'random_id': get_random_id(),
								        'attachment':
								        ['doc315625951_569339590']
								    })
						else:
							write_mes(group_ID, 'Вы не являетесь админом бота')

					elif mes_text[0] in [
					    '[club199139848|@ft_ghoul]',
					    '[club199447647|@ft_ghoul2]'
					]:
						linked()
						if event.object.message['from_id'] in admins_bot_GG:
							if ban_var == 1:
								db[j] = vk.method(
								    'users.get',
								    {'user_ids': j})[0]['first_name']
								cursor.execute(
								    f"INSERT INTO banned_users VALUES ({j})")
								write_mes(group_ID, 'Готово!\n\n███████╗ \n██╔════╝ \n█████╗ \n██╔══╝ \n██║\n╚═╝')
								connection.commit()
								ban_var = 0
							elif dima_var == 12:
								vk.method('messages.removeChatUser', {
								    'chat_id': group_ID,
								    'member_id': 273667139
								})
						else:
							ban_var = 1

					elif mes_text[0] in ['!botunban']:
						linked()
						if event.object.message['from_id'] in admins_bot_GG:
							try:
								j = list(mes_text[1])
								jj = j.index('|')
								try:
									while True:
										j.pop(jj)
								except:
									j.remove('[')
									j.remove('i')
									j.remove('d')
									j = ''.join(j)
								try:
									del db[j]
									write_mes(
									    group_ID,
									    'Удаляю юзера из списка забанненых в боте'
									)
								except:
									write_mes(
									    group_ID,
									    'Пользователя нет в черном списке бота'
									)
								banned_list = db.keys()
							except:
								vk.method(
								    'messages.send', {
								        'chat_id': group_ID,
								        'message': 'Вася кого разбанить?',
								        'attachment':
								        ['doc315625951_569339590'],
								        'random_id': get_random_id()
								    })
								vk.method(
								    'messages.send', {
								        'chat_id': group_ID,
								        'attachment':
								        ['doc315625951_569339590'],
								        'random_id': get_random_id()
								    })
						else:
							write_mes(group_ID, 'Вы не являетесь админом бота')

					elif mes_text[0] in ['!botbanlist']:
						linked()
						banned_list = db.keys()
						black_list = []
						for loh in banned_list:
							e = db[loh]
							ee = f'[id{loh}|{e}]'
							black_list.append(ee)
						try:
							black_list[0]
							black_list_str = ', '.join(black_list)
							write_mes(
							    group_ID,
							    f'Список забаненных пользователей:\n{black_list_str}'
							)
						except:
							write_mes(
							    group_ID,
							    'Список забаненных юзеров пока что пустует')
						#except:
					elif mes_text[0] in ['/автобот']:
						cursor.execute("""CREATE TABLE IF NOT EXISTS autobot(
							id INT
						)""")
						if event.object.message['from_id'] in [
						    315625951, 273667139
						]:
							try:
								print(1)
								j = get_user_id(mes_text[1])
							except:
								try:
									j = event.object.message['reply_message'][
									    'from_id']
								except:
									write_mes(group_ID, 'И чё и кого')
									j = 0
								if j != 0:
									cursor.execute("INSERT INTO autobot VALUES ?", (j))
									auto_var = int(j)
									write_mes(
									    group_ID,
									    f'███████╗\n██╔════╝\n█████╗\n██╔══╝\n██║\n╚═╝'
									)

					elif mes_text[0] == '/автостоп':
						linked()
						if event.object.message['from_id'] in [
						    315625951, 273667139
						]:
							try:
								if auto_var != 0:
									cursor.execute("DELETE FROM autobot WHERE id =", (u_id))
									write_mes(
									    group_ID,
									    f'Больше не веду диалог с [id{auto_var}|Пользователем]'
									)
									auto_var = 0
							except:
								write_mes(group_ID,
								          'Да я вроде и не болтал особо :/')

					elif mes_text[0] == 'погода':
						linked()
						if ban_check(u_id) == True:
							try:
								weather(mes_text[1])
							except:
								weather('Одинцово')
						elif ban_check(u_id) == False:
							write_mes(group_ID, 'Фейспалм чел ты в муте')
						else:
							write_mes(
							    group_ID,
							    'Я должен тебе отвечать что-то умное, но мне еще это не добавили)'
							)

					elif mes_text[0] in ['дуэль', 'поединок', 'бой']:
						linked()
						if ban_check(u_id) == True:

							def battle():
								i = random.randint(0, 2)
								if i == 0:
									write_mes(
									    group_ID,
									    'Менты накрыли обоих, все отменяется')
								elif i == 1:
									write_mes_online(
									    group_ID,
									    f'[id{opponent1}|{opp1_name}] победил')
								elif i == 2:
									write_mes_online(
									    group_ID,
									    f'[id{opponent2}|{vk.method("users.get", {"user_ids":opponent2})[0]["first_name"]}] победил'
									)

							try:
								if event.object.message['reply_message']:
									opponent1 = event.object.message['from_id']
									opp1_name = vk.method(
									    'users.get', {'user_ids': opponent1
									                  })[0]['first_name']
									opponent2 = event.object.message[
									    'reply_message']['from_id']
									opp2_name = vk.method(
									    'users.get', {
									        'user_ids': opponent2,
									        'name_case': 'acc'
									    })[0]['first_name']
									if opponent1 == int(opponent2):
										write_mes_online(
										    group_ID,
										    'Ну молодец, снес себе жбан')
									else:
										write_mes_online(
										    group_ID,
										    f'[id{opponent1}|{opp1_name}] вызвал на поединок [id{opponent2}|{opp2_name}]'
										)
										battle()
							except:
								try:
									if event.object.message['fwd_messages']:
										opponent1 = event.object.message[
										    'from_id']
										opp1_name = vk.method(
										    'users.get',
										    {'user_ids': opponent1
										     })[0]['first_name']
										opponent2 = event.object.message[
										    'fwd_messages'][0]['from_id']
										opp2_name = vk.method(
										    'users.get', {
										        'user_ids': opponent2,
										        'name_case': 'gen'
										    })[0]['first_name']
										if opponent1 == int(opponent2):
											write_mes_online(
											    group_ID,
											    'Ну молодец, снес себе жбан')
										else:
											write_mes_online(
											    group_ID,
											    f'[id{opponent1}|{opp1_name}] вызвал на поединок [id{opponent2}|{opp2_name}]'
											)
											battle()
									else:
										print(1 / 0)
								except:
									try:
										if mes_text[1]:
											j = list(mes_text[1])
											jj = j.index('|')
											try:
												while True:
													j.pop(jj)
											except:
												j.remove('[')
												j.remove('i')
												j.remove('d')
												j = ''.join(j)
											opponent1 = event.object.message[
											    'from_id']
											opp1_name = vk.method(
											    'users.get',
											    {'user_ids': opponent1
											     })[0]['first_name']
											opponent2 = j
											opp2_name = vk.method(
											    'users.get', {
											        'user_ids': opponent2,
											        'name_case': 'acc'
											    })[0]['first_name']
											if opponent1 == int(opponent2):
												write_mes(
												    group_ID,
												    'Ну молодец, снес себе жбан'
												)
											else:
												write_mes_online(
												    group_ID,
												    f'[id{opponent1}|{opp1_name}] вызвал на поединок [id{opponent2}|{opp2_name}]'
												)
												battle()
									except:
										try:
											if list(
											    str(event.object.
											        message['reply_message']
											        ['from_id']))[0] == '-':
												ran = random.randint(0, 1)
												if ran == 0:
													write_mes(
													    group_ID,
													    'Дурак, зачем бота гасить, совсем конченый что ли'
													)
												else:
													vk.method(
													    'messages.send', {
													        'sticker_id':
													        12714,
													        'chat_id':
													        group_ID,
													        'random_id':
													        get_random_id()
													    })
										except:
											write_mes(
											    group_ID,
											    'Вы устроили мордобой с воздухом и проиграли'
											)
											try:
												vk.method(
														'messages.send', {
																'chat_id': group_ID,
																'sticker_id': 4282,
																'random_id':
																get_random_id()
														})
											except:
												continue
						elif ban_check(u_id) == False:
							write_mes(group_ID, 'Фейспалм чел ты в муте')
						else:
							write_mes(
							    group_ID,
							    'Я должен тебе отвечать что-то умное, но мне еще это не добавили)'
							)

					elif mes_text[0] in ['пошел', 'иди', 'пошел', 'пошол']:
						linked()
						try:
							if event.object.message['reply_message'][
							    'from_id'] in [-199447647, -199139848
							                   ] and mes_text[1] in ['нахуй']:
								db[event.object.
								   message['from_id']] = vk.method(
								       'users.get', {
								           'user_ids':
								           event.object.message['from_id']
								       })[0]['first_name']
								write_mes(
								    group_ID,
								    'Вы были забанены по причине несанкциоионированного посыла нахуй'
								)
						except:
							pass
					elif mes_text[0] in [
					    '!помощь', 'help', 'help', 'помощь', 'справка',
					    '!справка'
					]:
						write_mes(
						    group_ID,
						    'Вся доступная информация про бота тут:\nvk.com/@ft_ghoul-base\n\nЕсли после прочтения статьи у  вопросы, можете задать их [x3ron|Админу], или написать в лс [ft_ghoul|Боту].'
						)
						#print(vk.method('messages.getConversationMembers', {'peer_id': 2000000000 + group_ID}))

					elif mes_text[0] == '!getuser':
						if group_ID == admin_chat:
							try:
								p = event.message['text'].split()
								j = list(p[1])
								jj = j.index('|')
								try:
									while True:
										j.pop(jj)
								except:
									j.remove('[')
									j.remove('i')
									j.remove('d')
									j = ''.join(j)
								es = 1
							except:
								write_mes(admin_chat,
								          'Укажите айди пользователя')
								es = 0

							if es == 1:
								g_i = 1
								prepair = []
								user_inf = get_user(j)[0]
								fio = user_inf['first_name'] + ' ' + user_inf[
								    'last_name']
								try:
									write_mes(group_ID, 'Ща все будет',
									          dima_clicker)
									vk.method(
									    'messages.setActivity', {
									        'type': 'typing',
									        'peer_id': 2000000000 + group_ID
									    })
									while True:
										chat_name = vk.method(
										    'messages.getConversationsById', {
										        'peer_ids': 2000000000 + g_i,
										        'extended': 1
										    })
										if chat_name['count'] != 0:
											for user_id in vk.method(
											    'messages.getConversationMembers',
											    {'peer_id': 2000000000 + g_i
											     })['profiles']:
												if int(j) == int(
												    user_id['id']):
													prepair.append(
													    '&#9898; ' +
													    chat_name['items'][0]
													    ['chat_settings']
													    ['title'])
										g_i += 1

								except:
									print('ку')

								if prepair != []:
									prepair_ready = '\n'.join(prepair)
									ready_mes = f'&#128308; Пользователь [id{j}|{fio}] состоит в беседах:\n\n\n{prepair_ready}'
								else:
									ready_mes = f'&#128308; Пользователь [id{j}|{fio}] не состоит в беседах, где есть бот'

								write_mes(group_ID, ready_mes)

					elif mes_text[0] == '!получить':
						if group_ID == admin_chat:
							try:
								if int(mes_text[1]) in range(0, 100):
									es = 1
								else:
									es = 0
									write_mes(admin_chat,
									          'Укажите айди беседы')

							except:
								write_mes(admin_chat, 'Укажите айди беседы')
								es = 0
							if es == 1:
								if admin_bot_get(int(mes_text[1])):
									chat_data = vk.method(
									    'messages.getConversationsById', {
									        'peer_ids':
									        2000000000 + int(mes_text[1]),
									        'extended':
									        1
									    })['items'][0]
									chat_settings = chat_data['chat_settings']
									owner_id = chat_settings['owner_id']
									owner = f'&#128081; Создатель беседы: [id{owner_id}|{get_user(owner_id)[0]["first_name"]} {get_user(owner_id)[0]["last_name"]}]'

									chat_title = f"&#128214; Название беседы: {chat_settings['title']}"
									extended_list = chat_settings['acl']
									can_list = []
									can_not_list = []
									for elem in extended_list:
										if extended_list[elem] == True:
											can_list.append(elem)
										else:
											can_not_list.append(elem)
									can_info = '&#9989; Я могу: ' + ', '.join(
									    can_list)
									can_not_info = '&#128683; Я не могу: ' + ', '.join(
									    can_not_list)
									members_count = f"&#9898; Всего участников в беседе: {chat_settings['members_count']}"
									admin_ids_list = chat_settings['admin_ids']
									adm_info_bots = []
									admin_list = []
									admin_list.append(
									    f'[id{owner_id}|{get_user(owner_id)[0]["first_name"]} {get_user(owner_id)[0]["last_name"]}]'
									)
									for elem in admin_ids_list:
										if elem < 0:
											elem_p = elem * -1
											adm_info_bots.append(
											    f"[club{elem_p}|{get_group(elem_p)['name']}]"
											)
										else:
											admin_list.append(
											    f'[id{elem}|{get_user(elem)[0]["first_name"]} {get_user(elem)[0]["last_name"]}]'
											)
									var_bot_adm = '\n '.join(adm_info_bots)
									adm_bots = f"&#129302; Боты в беседе, с правами администратора: {var_bot_adm}"
									var_ad_users = '\n '.join(admin_list)
									admin_users = f"&#128308; Администраторы в беседе: {var_ad_users}"
									online_users_list = []
									user_inf = vk.method(
									    'messages.getConversationMembers', {
									        'peer_id':
									        2000000000 + int(mes_text[1])
									    })
									users_online_list = []
									n = 0
									a = 0
									user_inf = vk.method(
									    'messages.getConversationMembers', {
									        'peer_id':
									        2000000000 + int(mes_text[1]),
									        'group_id':
									        int(mes_text[1])
									    })
									for user in user_inf['profiles']:
										if user_inf['profiles'][n][
										    'online_info']['visible'] == False:
											a += 1
										else:
											if user_inf['profiles'][n][
											    'online_info'][
											        'is_online'] == True:
												if user_inf['profiles'][n][
												    'online_info'][
												        'is_mobile'] == True:
													users_online_list.append(
													    f'&#128241; [id{user_inf["profiles"][n]["id"]}|{user_inf["profiles"][n]["first_name"]}]'
													)
												else:
													users_online_list.append(
													    f'&#128421; [id{user_inf["profiles"][n]["id"]}|{user_inf["profiles"][n]["first_name"]}]'
													)
										n += 1
									result_online = '\n'.join(
									    users_online_list)
									online_mes = f'&#127759; Пользователи онлайн:\n{result_online}'
									invisible_online = f'&#128100; Количество пользователей, скрываюищх онлайн: {a}'
									'''for elem in chat_settings['active_ids']:
                    if elem < 0:
                      pass
                    else:
                      online_users_list.append(f'[id{elem}|{get_user(elem)[0]["first_name"]} {get_user(elem)[0]["last_name"]}]')
                  online_users = f'Пользователи онлайн: {", ".join(online_users_list)}'
                  '''
									ready_mes = f'{owner}\n{chat_title}\n\n{can_info}\n\n{can_not_info}\n\n{members_count}\n\n{adm_bots}\n\n{admin_users}\n\n{online_mes}\n\n{invisible_online}'
									write_mes_online(admin_chat, ready_mes)

					elif mes_text[0] == '!гдея':
						write_mes(group_ID, group_ID)

					elif mes_text[0] == '/беседы':
						if group_ID == admin_chat:
							gg = 0
							o = 0
							oq = 0
							mas = []
							er_mas = []
							while True:
									o += 1
									try:
										d = get_chat(o)
									except:
										ready = '\n'.join(mas)
										err = ', '.join(er_mas)
										write_mes(group_ID, f'Всего найдено {oq}:\n\n{ready}\n\nНе найдено {gg}: {err}')
										break
									if d['count'] != 0:
										mas.append(f"{o}. {d['items'][0]['chat_settings']['title']}")
										oq += 1
									else:
										gg += 1
										er_mas.append(str(o))

					elif mes_text[0] == '!обновить':
						if ban_check(u_id) == True:
							if admin_bot_get(group_ID):
								members = vk.method(
								    'messages.getConversationMembers',
								    {'peer_id': 2000000000 + group_ID})
								for i in members["items"]:
									admin = i.get('is_admin', False)
									if i["member_id"] == event.object.message[
									    "from_id"]:
										if admin == True or u_id == 315625951:
											if obn_var == []:
												obn_var_var += 1
												obn_var.append(obn_var_var)
												r_u_id = u_id
												obn_var.append(r_u_id)
											else:
												if r_u_id == u_id:
													if obn_var == 1:
														obn_var.pop(0)
														obn_var_var += 1
														write_mes(
														    group_ID,
														    'Не отправляйте эту команду много раз.'
														)
														obn_var.incert(
														    0, obn_var_var)
													elif obn_var == 2:
														obn_var.pop(0)
														obn_var_var += 1
														obn_var.incert(
														    0, obn_var_var)
														write_mes(
														    group_ID,
														    'Последнее предупреждение. Не спамьте.'
														)
													else:
														write_mes(
														    group_ID,
														    'Добавляю пользователя в список забаненных в боте...'
														)
														db[u_id] = vk.method(
														    'users.get', {
														        'user_ids':
														        u_id
														    })[0]['first_name']
														write_mes(
														    group_ID,
														    'Готово!')
												else:
													obn_var.clear()

											try:
												link_name = vk.method(
												    'messages.getInviteLink', {
												        'peer_id':
												        2000000000 + group_ID
												    })
											except:
												write_mes(
												    group_ID,
												    'Предоставьте разрешение на получение ссылки'
												)
												link_name = 'Не удалось получить ссылку'
											group_name = vk.method(
											    'messages.getConversationsById',
											    {
											        'peer_ids':
											        2000000000 + group_ID
											    })['items'][0][
											        'chat_settings']['title']

											owner_id = vk.method(
											    'messages.getConversationsById',
											    {
											        'peer_ids':
											        2000000000 + group_ID
											    }
											)['items'][0]['chat_settings'][
											    'owner_id']

											users_count = vk.method(
											    'messages.getConversationsById',
											    {
											        'peer_ids':
											        2000000000 + group_ID
											    }
											)['items'][0]['chat_settings'][
											    'members_count']

											users_list = []

											local_group_id = vk.method(
											    'messages.getConversationsById',
											    {
											        'peer_ids':
											        2000000000 + group_ID
											    }
											)['items'][0]['peer']['local_id']

											admins_list = vk.method(
											    'messages.getConversationsById',
											    {
											        'peer_ids':
											        2000000000 + group_ID
											    }
											)['items'][0]['chat_settings'][
											    'admin_ids']
											admins_mentions = []
											for user in admins_list:
												if user < 0:
													group = vk.method(
													    'groups.getById',
													    {'group_ids': user})
													user = user * -1
													user = f'[public{user}|БОТ]'
													admins_mentions.append(
													    user)
												else:
													user_name = vk.method(
													    'users.get',
													    {'user_ids': user})

													user = f'[id{user}|{user_name[0]["first_name"]} {user_name[0]["last_name"]}]'
													admins_mentions.append(
													    user)
											admins_mentions = ', '.join(
											    admins_mentions)
											try:
												if link_name[1] == 0:
													link_name_pr = link_name[0]
												else:
													link_name_pr = link_name
											except:
												link_name_pr = link_name
											write_mes({
											    admin_chat
											}, f'Новая группа!!!\n\n&#128220; Ссылка на вступление: {str(link_name_pr["link"])}\n\n&#128206; Название беседы: {group_name}\n\n&#128081; Создатель беседы: @id{str(owner_id)}\n&#128308; Администраторы беседы: {str(admins_mentions)}\n\n&#128101; Всего участников: {str(users_count)}\n\n&#127380; Уникальный идентификационный номер: {str(local_group_id)}\n\n&#128344; Время отправки запроса на обновление: {mes_time}'
											          )

										else:
											gender = vk.method(
											    'users.get', {
											        'user_ids':
											        event.object.
											        message["from_id"],
											        'fields':
											        'sex'
											    })
											if gender[0]['sex'] == 1:
												write_mes(
												    group_ID,
												    'Ты кто вообще такая?')
											elif gender[0]['sex'] == 2:
												write_mes(
												    group_ID,
												    'Ты кто вообще такой?')
											else:
												write_mes(
												    group_ID,
												    'У тебя скрыт пол, поэтому я спрошу ТЫ ЧТО ВООБЩЕ ТАКОЕЕЕ???'
												)
							else:
								write_mes(group_ID, 'Дайте админку...')
						elif ban_check(u_id) == False:
							write_mes(group_ID, 'Фейспалм чел ты в муте')

					elif mes_text[0] == '!гдз':
						try:
							if mes_text[1] == 'русский':
								write_mes(
								    group_ID,
								    'https://gdz.ru/class-9/russkii_yazik/trostnecova-9/'
								)
							elif mes_text[1] == 'алгебра':
								write_mes(
								    group_ID,
								    'https://gdz.math-helper.ru/reshebniki-dlya-shkolnikov/gdz-k-uchebniku-merzljak-algebra-9-klass-uglublennoe-izuchenie'
								)
							elif mes_text[1] == 'геометрия':
								write_mes(
								    group_ID,
								    'https://gdz.ru/class-7/geometria/atanasyan-7-9/'
								)
							elif mes_text[1] == 'история':
								write_mes(
								    group_ID,
								    'https://www.euroki.org/gdz/ru/istoriya/9_klass/istoriya-rossii-9-klass-arsentev-danilov-158'
								)
							elif mes_text[1] == 'англ':
								try:
									if mes_text[2] in ['уч', 'учебник']:
										write_mes(group_ID,'https://vk.cc/bWmXFW')
									elif mes_text[2] == 'рт':
										write_mes(group_ID, 'https://vk.cc/8rKrfH')
									else:
										write_mes(group_ID, 'Укажи рт или учебник')
								except:
									write_mes(group_ID, 'Укажи рт или учебник')
									

						except:
							write_mes(group_ID, 'Укажите предмет')

					elif mes_text[0] == '!работать':
						linked()
						if ban_check(u_id) == True:
							if admin_chat == 9 or group_ID in [1, 2, 9]:
								if cursor.execute(
								    f"SELECT job_time FROM users WHERE id = {u_id}"
								).fetchone()[0] < mes_time_u:
									cursor.execute(
									    f"UPDATE users SET job_time = {mes_time_u} + 14400 WHERE id = {u_id}"
									)
									connection.commit()
									if job_get(u_id) == 1:
										cursor.execute(
										    f"UPDATE users SET cash = cash + 1000 WHERE id = {u_id}"
										)
									elif job_get(u_id) == 2:
										cursor.execute(
										    f"UPDATE users SET cash = cash + 2500 WHERE id = {u_id}"
										)
									elif job_get(u_id) == 3:
										cursor.execute(
										    f"UPDATE users SET cash = cash + 6000 WHERE id = {u_id}"
										)
									elif job_get(u_id) == 4:
										cursor.execute(
										    f"UPDATE users SET cash = cash + 10000 WHERE id = {u_id}"
										)
									elif job_get(u_id) == 5:
										cursor.execute(
										    f"UPDATE users SET cash = cash + 25000 WHERE id = {u_id}"
										)
									elif job_get(u_id) == 6:
										cursor.execute(
										    f"UPDATE users SET cash = cash + 50000 WHERE id = {u_id}"
										)
									connection.commit()
									print('cash ready')
									num = list(str(balance_get(u_id)))
									num.reverse()
									a = 0
									for i in num:
										a += 1
									count = a // 3
									ii = 3
									while count > 0:

										num.insert(ii, '.')
										count -= 1
										ii += 4
									num.reverse()
									if a % 3 == 0:
										num.pop(0)
									num = ''.join(num)
									write_mes_online(
									    group_ID,
									    f'[id{u_id}|{nick_get(u_id, group_ID)}], Отлично поработал!\n\nТвой баланс: {num}&#127791;'
									)
								else:
									job_time = cursor.execute(
									    f"SELECT job_time FROM users WHERE id = {u_id}"
									).fetchone()[0]
									write_mes(
									    group_ID,
									    f'Вы сможете работать в {time_pret(job_time)}'
									)
							else:
								write_mes(
								    group_ID,
								    'Работа с базой данных не предусмотрена для работы со вторым ботом'
								)

					elif mes_text[0] == '3а21' and u_id == 315625951:
						cursor.execute("""CREATE TABLE IF NOT EXISTS dk(
							group_id INT,
							kick INT,
							роль INT,
							ава INT,
							варн INT
						)""")
					elif mes_text[0] == '!drop':
						cursor.execute("DROP TABLE prom")
						connection.commit()

					elif mes_text[0] == 'test1' and u_id == 315625951:
						datas = {'q': 'def'}

						ttt = input('вв ')

						datas['user_request'] = ttt
						url = 'http://p-bot.ru'

						s = requests.Session()
						hh = {
						    'User-Agent':
						    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
						}

						otp = s.post(
						    url, data=datas, cookies=s.cookies.get_dict())

						print(otp.text)

					elif mes_text[0] == 'test2' and u_id == 315625951:
						while True:
							write_mes(25, '@all')
					elif mes_text[0] in ['+варн', '!варн', '+пред', '!пред']:
						if admin_chat == 9 or group_ID in [1, 2, 9]:
							members = vk.method(
							    'messages.getConversationMembers',
							    {'peer_id': 2000000000 + group_ID})['items']
							n = 1
							for i in members:
								if u_id == i['member_id']:
									try:
										i['is_admin']
										g = 1
										break
									except:
										g = 0
										break
								n += 1
							if g == 1:
								try:
									rep_id = event.object.message[
									    'reply_message']['from_id']
									warn_get(rep_id, group_ID, '+')
									warn_count = warn_get(rep_id, group_ID)
									u2_inf = vk.method('users.get', {
									    'user_ids': rep_id,
									    'name_case': 'gen'
									})[0]
									u2_name = u2_inf['first_name']
									if warn_count == 5:
										write_mes_online(
										    group_ID,
										    f'У [id{rep_id}|{u2_name}] максимальное количество предупреждений (5/5)\nКикаю...'
										)
										vk.method(
										    'messages.removeChatUser', {
										        'chat_id': group_ID,
										        'member_id': rep_id
										    })
									else:
										write_mes_online(
										    group_ID,
										    f'У [id{rep_id}|{u2_name}] {warn_count}/5 предупреждений'
										)
								except:
									try:
										u2_id = get_user_id(mes_text[1])
										u2_inf = vk.method(
										    'users.get', {
										        'user_ids': u2_id,
										        'name_case': 'gen'
										    })[0]
										u2_name = u2_inf['first_name']
										warn_get(u2_id, group_ID, '+')
										warn_count = warn_get(u2_id, group_ID)
										if warn_count == 5:
											write_mes_online(
											    group_ID,
											    f'У [id{u_id}|{u2_name}] максимальное количество предупреждений (5/5)\nКикаю...'
											)
											vk.method(
											    'messages.removeChatUser', {
											        'chat_id': group_ID,
											        'member_id': u2_id
											    })
										else:
											write_mes_online(
											    group_ID,
											    f'У [id{u2_id}|{u2_name}] {warn_count}/5 предупреждений'
											)
									except:
										write_mes(group_ID, 'Ичё и каво')
							else:
								write_mes(group_ID, 'Ты не админ слыш')

					elif mes_text[0] in [
					    '-варн', '!снятьварн', '-пред', '!снятьпред'
					]:
						if admin_chat == 9 or group_ID in [1, 2, 9]:
							members = vk.method(
							    'messages.getConversationMembers',
							    {'peer_id': 2000000000 + group_ID})['items']
							n = 1
							for i in members:
								if u_id == i['member_id']:
									try:
										i['is_admin']
										g = 1
										break
									except:
										g = 0
										break
								n += 1
							if g == 1:
								try:
									rep_id = event.object.message[
									    'reply_message']['from_id']
									warn_get(rep_id, group_ID, '-')
									warn_count = warn_get(rep_id, group_ID)
									u2_inf = vk.method('users.get', {
									    'user_ids': rep_id,
									    'name_case': 'gen'
									})[0]
									u2_name = u2_inf['first_name']
									if warn_count == -1:
										write_mes_online(
										    group_ID,
										    f'У [id{rep_id}|{u2_name}] минимально возможное количество предупреждений (0/5)'
										)
										warn_get(rep_id, group_ID, '+')
									else:
										write_mes_online(
										    group_ID,
										    f'У [id{rep_id}|{u2_name}] {warn_count}/5 предупреждений'
										)
								except:
									try:
										u2_id = get_user_id(mes_text[1])
										u2_inf = vk.method(
										    'users.get', {
										        'user_ids': u2_id,
										        'name_case': 'gen'
										    })[0]
										u2_name = u2_inf['first_name']
										warn_get(u2_id, group_ID, '-')
										warn_count = warn_get(u2_id, group_ID)
										if warn_count == -1:
											write_mes_online(
											    group_ID,
											    f'У [id{rep_id}|{u2_name}] минимально возможное количество предупреждений (0/5)'
											)
											warn_get(rep_id, group_ID, '+')
										else:
											write_mes_online(
											    group_ID,
											    f'У [id{rep_id}|{u2_name}] {warn_count}/5 предупреждений'
											)
									except:
										write_mes(group_ID, 'Ичё и каво')
							else:
								write_mes(group_ID, 'Ты не админ слыш ')

					elif mes_text[0] == '!снять' and u_id == 315625951:
						try:
							j = event.object.message['reply_message'][
							    'from_id']
							e = 1
							sel = 2
						except:
							try:
								j = get_user_id(mes_text[2])
								sel = 3
								e = 1
							except:
								e = 0

						if e == 1:
							print(j)
							try:
								if mes_text[1] in ['рейтинг', 'рейт']:
									g = 1
								else:
									g = 0
							except:
								g = 0

							if g == 1:
								try:
									mins = int(mes_text[sel])
									if mins >= 1:
										hh = 1
									else:
										hh = 0
										write_mes(group_ID,
										          'Укажи натуральное число')
								except:
									try:
										if mes_text[sel] in ['всё', 'все']:
											mins = rate_get(int(j))
											hh = 1
									except:
										hh = 0

							if hh == 1 and mins <= rate_get(j):
								cursor.execute(
								    f"UPDATE users SET rate = rate - {mins} WHERE id = {j}"
								)
								connection.commit()
								write_mes(group_ID, 'Готово, мой повелитель')
							else:
								write_mes(
								    group_ID,
								    'У пользователя нет столько рейтинга')

					elif mes_text[0] in ['!все', '!всё']:
						try:
							if mes_text[1] == 'или':
								if mes_text[2] == 'ничегo':
									if u_id == 315625951:
										write_mes(
										    group_ID,
										    'Вы выиграли во "Всё или ничего", ваш баланс увеличен в 400 раз!'
										)
										cursor.execute(
										    f"UPDATE users SET cash = cash * 400 WHERE id = {u_id}"
										)
										connection.commit()
								elif mes_text[2] == 'ничего':
									Bce_uJlu_Hu4ero = random.randint(0, 100)
									stavka = balance_get(u_id)
									if Bce_uJlu_Hu4ero in range(97, 101):
										write_mes(
										    group_ID,
										    'Вы выиграли во "Всё или ничего", ваш баланс увеличен в 400 раз!'
										)
										cursor.execute(
										    f"UPDATE users SET cash = cash * 400 WHERE id = {u_id}"
										)
										connection.commit()
									else:
										write_mes(
										    group_ID,
										    'Вы проиграли :(\nВаш баланс аннулирован'
										)
										cursor.execute(
										    f"UPDATE users SET cash = 0 WHERE id = {u_id}"
										)
										connection.commit()
						except:
							pass

					elif mes_text[0] == '!топ':
						linked()
						if ban_check(u_id) == True:

							if admin_chat == 9 or group_ID in [1, 2, 9]:
								prep_list = []
								for user in cursor.execute(
								    f"SELECT user_messages_count, user_ids FROM a{group_ID}"
								):
									if user not in prep_list:
										prep_list.append(user)

								prep_list.sort()
								prep_list.reverse()
								prep1_list = []
								o = 0
								for i in prep_list:
									o += 1
									print(o)
									prep1_list.append(
									    f'{str(o)}) [id{i[1]}|{nick_get(i[1], group_ID)}] - {str(i[0])} сообщений'
									)
								ready_mes = '\n'.join(prep1_list)
								write_mes_online(
								    group_ID,
								    f'Топ пользователей по количеству сообщений:\n\n{ready_mes}'
								)

							else:
								write_mes(
								    group_ID,
								    'Работа с базой данных не предусмотрена для работы со вторым ботом'
								)

					elif mes_text[0] in ['+роль', '+админ', '!повысить']:
						if admin_chat == 9 or group_ID in [1, 2, 9]:
							linked()
							if ban_check(u_id) == True:
								members = vk.method(
								    'messages.getConversationMembers',
								    {'peer_id': 2000000000 + group_ID})
								for i in members["items"]:
									if i["member_id"] == event.object.message[
									    "from_id"]:
										admin = i.get('is_admin', False)
										if admin == True or status_get(
										    u_id, group_ID) == 3:
											p = event.message['text'].split()
											try:
												j = list(p[1])
												jj = j.index('|')
												try:
													while True:
														j.pop(jj)
												except:
													j.remove('[')
													j.remove('i')
													j.remove('d')
													j = ''.join(j)
												if cursor.execute(
												    f"SELECT user_status FROM a{group_ID} WHERE user_ids = {u_id}"
												).fetchone()[0] <= 3:
													cursor.execute(
													    f"UPDATE a{group_ID} SET user_status = user_status + 1 WHERE user_ids = {j}"
													)
													connection.commit()
													write_mes(
													    group_ID,
													    'Статус обновлён!')
												else:
													write_mes(
													    group_ID,
													    'У пользователя максимальо допустимый уровень!'
													)
											except:
												write_mes(group_ID, 'И кого?')

										else:
											gender = vk.method(
											    'users.get', {
											        'user_ids':
											        event.object.
											        message["from_id"],
											        'fields':
											        'sex'
											    })
											if gender[0]['sex'] == 1:
												write_mes(
												    group_ID,
												    'Ты кто вообще такая?')
											elif gender[0]['sex'] == 2:
												write_mes(
												    group_ID,
												    'Ты кто вообще такой?')
											else:
												write_mes(
												    group_ID,
												    'У тебя скрыт пол, поэтому я спрошу ТЫ ЧТО ВООБЩЕ ТАКОЕЕЕ???'
												)
						else:
							write_mes(
							    group_ID,
							    'Работа с базой данных не предусмотрена для работы со вторым ботом'
							)

					elif mes_text[0] == '-роль':
						if admin_chat == 9 or group_ID in [1, 2, 9]:
							linked()
							if ban_check(u_id) == True:
								members = vk.method(
								    'messages.getConversationMembers',
								    {'peer_id': 2000000000 + group_ID})
								for i in members["items"]:
									if i["member_id"] == event.object.message[
									    "from_id"]:
										admin = i.get('is_admin', False)
										if admin == True or status_get(
										    u_id, group_ID) == 3:
											p = event.message['text'].split()
											try:
												j = list(p[1])
												jj = j.index('|')
												try:
													while True:
														j.pop(jj)
												except:
													j.remove('[')
													j.remove('i')
													j.remove('d')
													j = ''.join(j)
												if cursor.execute(
												    f"SELECT user_status FROM a{group_ID} WHERE user_ids = {u_id}"
												).fetchone()[0] > -1:
													cursor.execute(
													    f"UPDATE a{group_ID} SET user_status = user_status - 1 WHERE user_ids = {j}"
													)
													connection.commit()
													write_mes(
													    group_ID,
													    'Статус обновлён!')
												else:
													write_mes(
													    group_ID,
													    'У пользователя минимально допустимый уровень!'
													)
											except:
												write_mes(group_ID, 'И кого?')
										else:
											gender = vk.method(
											    'users.get', {
											        'user_ids':
											        event.object.
											        message["from_id"],
											        'fields':
											        'sex'
											    })
											if gender[0]['sex'] == 1:
												write_mes(
												    group_ID,
												    'Ты кто вообще такая?')
											elif gender[0]['sex'] == 2:
												write_mes(
												    group_ID,
												    'Ты кто вообще такой?')
											else:
												write_mes(
												    group_ID,
												    'У тебя скрыт пол, поэтому я спрошу ТЫ ЧТО ВООБЩЕ ТАКОЕЕЕ???'
												)
						else:
							write_mes(
							    group_ID,
							    'Работа с базой данных не предусмотрена для работы со вторым ботом'
							)

					elif mes_text[0] == '+ник':
						linked()
						if ban_check(u_id) == True and (admin_chat == 9
						                                or group_ID in [1, 9]):
							try:
								mes_text_syntax.pop(0)
								var = 0
								gh = list(' '.join(mes_text_syntax))
								for i in gh:
									var += 1
								if var >= 21 or var < 3:
									gg = 0
								else:
									gg = 1
								text = ' '.join(mes_text_syntax)
								text = text.replace('<br>', '')
								print(gg)
							except ValueError:
								gg = 0
							if gg == 1:
								cursor.execute(
								    f"UPDATE a{group_ID} SET user_nick = ? WHERE user_ids = ?",
								    (str(text), u_id))
								connection.commit()
								write_mes(
								    group_ID,
								    f'Ник заменён на {nick_get(u_id, group_ID)}'
								)
							else:
								if group_ID in [1, 9]:
									write_mes(
									    group_ID,
									    'Укажи ник нормально (от 3 до 21 символа)',
									    'video315625951_456239158')
								else:
									write_mes(
									    group_ID,
									    'Укажите ник (от 3 до 21 символа)')

					elif mes_text[0] == '+описание':

						linked()
						if ban_check(u_id) == True and (admin_chat == 9
						                                or group_ID in [1, 9]):
							g = 0
							for lit in list(mes_text_syntax):
								g += 1
							if g <= 256:
								try:
									mes_text_syntax[1]
									mes_text_syntax.pop(0)
									gg = 1
									text = ' '.join(mes_text_syntax)
								except:
									gg = 0
								if gg == 1:
									cursor.execute(
									    f"UPDATE a{group_ID} SET user_info = ? WHERE user_ids = ?",
									    (text, u_id))
									connection.commit()
									write_mes(group_ID, 'Описание обновлено')
								else:
									write_mes(group_ID, 'Укажите описание')
							else:
								write_mes(
								    group_ID,
								    'Слишком длинное описание. Уложитесь в 256 символов'
								)

					elif mes_text[0] == '!казино':
						try:
							podkr = mes_text[2]
						except:
							podkr = 0

						linked()
						if ban_check(u_id) == True:
							try:
								if mes_text[1] in ['все', 'всё', 'all']:
									p = 1
									minus_a = balance_get(u_id)
								elif int(mes_text[1]) >= 100:
									p = 1
									minus_a = mes_text[1]
								else:
									p = 0
							except:
								p = 0

							if p == 1:
								if balance_get(u_id) >= int(minus_a):
									cursor.execute(
									    f"UPDATE users SET cash = cash - {int(minus_a)} WHERE id = {u_id}"
									)
									connection.commit()
									bb_cash = random.randint(0, 100)
									'''
									if u_id == 518399067:
										if random.randint(0,1) == 1:
										bb_cash == 1
									'''
									if u_id == 315625951 and podkr != False:
										bb_cash = 100
									if bb_cash == 100:
										bb_cash_x = 50
									elif bb_cash in range(90, 100):
										bb_cash_x = 4
									elif bb_cash in range(75, 90):
										bb_cash_x = 2
									elif bb_cash in range(50, 75):
										bb_cash_x = 1
									elif bb_cash in range(40, 50):
										bb_cash_x = 0.75
									elif bb_cash in range(30, 40):
										bb_cash_x = 0.5
									elif bb_cash in range(20, 30):
										bb_cash_x = 0.25
									else:
										bb_cash_x = 0
									bb_cash_ready = bb_cash_x * int(minus_a)
									if bb_cash_x >= 2:
										win_mes = f', вы выиграли {str(bb_cash_ready - (int(minus_a)))}&#127791;'
									elif bb_cash_x == 1:
										win_mes = f', вы ничего не выиграли, но и не проиграли!'
									else:
										win_mes = f', вы проиграли {str(int(minus_a) - bb_cash_ready)}&#127791;'
									cursor.execute(
									    f"UPDATE users SET cash = cash + {bb_cash_ready} WHERE id = {u_id}"
									)
									connection.commit()
									write_mes_online(
									    group_ID,
									    f'[id{u_id}|{nick_get(u_id, group_ID)}]{win_mes}'
									)
								else:
									write_mes(group_ID,
									          'Ты в себя поверил? Иди копи!')

							else:
								write_mes(
								    group_ID,
								    'Укажите сумму ставки от 100&#127791;')

					elif mes_text[0] == '!del' and u_id == 315625951:
						if admin_chat == 9 or group_ID in [1, 2, 9]:
							try:
								mes_text[1]
								g = 1
							except:
								write_mes(group_ID, 'Аче удалять то будем?')
								g = 0

							if g == 1:
								p = event.message['text'].split()
								try:
									j = list(p[2])
									h = 1
								except:
									h = 0
								if h == 1:
									jj = j.index('|')
									try:
										while True:
											j.pop(jj)
									except:
										j.remove('[')
										j.remove('i')
										j.remove('d')
										j = ''.join(j)
									if mes_text[1] == 'ник':
										cursor.execute(
										    f"UPDATE a{group_ID} SET user_nick = '<Удалено модератором>' WHERE user_ids = {j}"
										)
										connection.commit()
									elif mes_text[1] == 'описание':
										cursor.execute(
										    f"UPDATE a{group_ID} SET user_info = '<Удалено модератором>' WHERE user_ids = {j}"
										)
										connection.commit()

								else:
									write_mes(group_ID, 'Ичё и кого')
						else:
							write_mes(
							    group_ID,
							    'Работа с базой данных не работает со вторым ботом'
							)

					elif mes_text[0] == '-деньги' and u_id == 315625951:
						try:
							rep_text = event.object.message['reply_message'][
							    'text']
							rep_id = event.object.message['reply_message'][
							    'from_id']
							cursor.execute(
							    f"UPDATE users SET cash = 0 WHERE id = {rep_id}"
							)
							connection.commit()
							write_mes(group_ID, 'Готово, мой повелитель!')
						except:
							try:
								mes_text[1]
								gg = 1
							except:
								gg = 0

							if gg == 1:
								p = event.message['text'].split()
								j = list(p[1])
								jj = j.index('|')
								try:
									while True:
										j.pop(jj)
								except:
									j.remove('[')
									j.remove('i')
									j.remove('d')
									j = ''.join(j)
								cursor.execute(
								    f"UPDATE users SET cash = 0 WHERE id = {j}"
								)
								connection.commit()
								write_mes(group_ID, 'Готово, мой повелитель!')
							else:
								write_mes(group_ID, 'Кому?')

					elif mes_text[0] in ['!профиль', '!я']:
						linked()
						if ban_check(u_id) == True:
							if admin_chat == 9 or group_ID in [1, 2, 9]:
								print(lvl_get(u_id, group_ID))
								if lvl_get(u_id, group_ID) == 0:
									lvl_mes = 'Просто человек'
								elif lvl_get(u_id, group_ID) == 1:
									lvl_mes = 'Мелкий чиновник'
								elif lvl_get(u_id, group_ID) == 2:
									lvl_mes = 'Админ'
								elif lvl_get(u_id, group_ID) == 3:
									lvl_mes = 'Князь'
								
								write_mes(
								    group_ID,
								    f'&#128100; Это {nick_get(u_id, group_ID)}\n\n&#128176; Ваш баланс: {bal_pret(round(balance_get(u_id)))}&#127791;\n\n&#128273; Имущество:\n\n&#128664; Машина: {car_text_get(car_get(u_id))}\n\n&#128241; Телефон: {phone_text_get(phone_get(u_id))}\n\n&#127969; Недвижимость: {house_text_get(house_get(u_id))}\n\n&#127970; Ваш бизнес: {business_text_get(get_bus(u_id)[1])}\n\n&#128511; Ваш рейтинг: {rate_get(u_id)}\n\n&#128081; Ваше положение в обществе: {lvl_mes}\n\n&#9993; Количество сообщений общества: {mes_count_get(u_id, group_ID)}\n\n&#128214; Описание пользователя:\n{info_get(u_id, group_ID)}'
								)
								
							else:
								write_mes(
								    group_ID,
								    'Работа с базой данных не предусмотрена для работы со вторым ботом'
								)

					elif mes_text[0] == '!чек':
						try:
							rep_text = event.object.message['reply_message'][
							    'text']
							j = event.object.message['reply_message'][
							    'from_id']
							gender = vk.method('users.get', {
							    'user_ids': j,
							    'fields': 'sex'
							})
							if gender[0]['sex'] == 1:
								eee = 'Её'
							else:
								eee = 'Его'
							if j not in [-199139848, -199447647]:
								write_mes(
								    group_ID,
								    f'&#128100; Это {nick_get(j, group_ID)}\n\n&#128176; {eee} баланс: {str(round(balance_get(j)))}&#127791;\n\n&#128511; {eee} рейтинг: {rate_get(j)}\n\n&#128081; {eee} положение в обществе: {lvl_get(j, group_ID)}\n\n&#9993; Количество сообщений общества: {mes_count_get(j, group_ID)}\n\n&#128214; Описание пользователя:\n{info_get(j, group_ID)}'
								)
							else:
								write_mes(
								    group_ID,
								    '&#128100; Это самый забаганный бот\n\n&#128176; Его баланс очень велик, примерно 500 рубликов\n\n&#9993; Количество сообщений: боже он единственный кто вам отвечает, да он дохрена наспамил)))\n\n&#128214; Описание пользователя:\nДима лох)'
								)
						except:
							try:
								p = event.message['text'].split()
								j = list(p[1])
								jj = j.index('|')
								try:
									while True:
										j.pop(jj)
								except:
									try:
										j.remove('[')
										j.remove('i')
										j.remove('d')
										j = int(''.join(j))
									except:
										j.remove('c')
										j.remove('l')
										j.remove('u')
										j.remove('b')
										j = int(''.join(j))
										j = j * -1
								if j not in [-199139848, -199447647]:
									gender = vk.method('users.get', {
									    'user_ids': j,
									    'fields': 'sex'
									})
									if gender[0]['sex'] == 1:
										eee = 'Её'
									else:
										eee = 'Его'
									write_mes(
									    group_ID,
									    f'&#128100; Это {nick_get(j, group_ID)}\n\n&#128176; {eee} баланс: {str(balance_get(j))}\n\n&#128511; {eee} рейтинг: {rate_get(j)}\n\n&#127791;\n\n&#128081; {eee} положение в обществе: {lvl_get(j, group_ID)}\n\n&#9993; Количество сообщений общества: {mes_count_get(j, group_ID)}\n\n&#128214; Описание пользователя:\n{info_get(j, group_ID)}'
									)
								else:
									write_mes(
									    group_ID,
									    '&#128100; Это самый забаганный бот\n\n&#128176; Его баланс очень велик, примерно 500 рубликов\n\n&#9993; Количество сообщений: боже он единственный кто вам отвечает, да он дохрена наспамил)))\n\n&#128214; Описание пользователя:\nДима лох)'
									)
							except:
								write_mes(group_ID, 'Ичё и кого')

					elif mes_text[0] == '!передать':
						if 'reply_message' not in event.object.message:
							try:
								mes_text[1]
								count = int(mes_text[2])
								gg = 1
							except:
								write_mes_online(
								    group_ID,
								    'Укажите кому и сколько денег передать. пример: !передать @x3ron 1000'
								)
								gg = 0

							if gg == 1:
								if count >= 1:
									if count <= balance_get(u_id):
										u2_id = get_user_id(mes_text[1])
										if u2_id != u_id:
											u2_inf = vk.method(
											    'users.get', {
											        'user_ids': u2_id,
											        'name_case': 'gen'
											    })
											cursor.execute(
											    f"UPDATE users SET cash = cash - {count} WHERE id = {u_id}"
											)
											connection.commit()
											cursor.execute(
											    f"UPDATE users SET cash = cash + {count} WHERE id = {u2_id}"
											)
											connection.commit()
											write_mes_online(
											    group_ID,
											    f'[id{u_id}|{get_user(u_id)[0]["first_name"]}] передал {count}&#127791; [id{u2_id}|{u2_inf[0]["first_name"]}]'
											)
										else:
											write_mes(
											    group_ID,
											    'Нельзя передать деньги самому себе '
											)
									else:
										write_mes(group_ID,
										          'У вас нет столько денег')
								else:
									write_mes(group_ID,
									          'Укажите натуральное число')
						else:
							try:
								count = int(mes_text[1])
								gg = 1
							except:
								write_mes_online(
								    group_ID,
								    'Укажите кому и сколько денег передать. пример: !передать @x3ron 1000'
								)
								gg = 0

							if gg == 1:
								if count in range(1, 10000000):
									u2_id = event.object.message[
									    'reply_message']['from_id']
									if u2_id != u_id:
										u2_inf = vk.method(
										    'users.get', {
										        'user_ids': u2_id,
										        'name_case': 'dat'
										    })
										cursor.execute(
										    f"UPDATE users SET cash = cash - {count} WHERE id = {u_id}"
										)
										connection.commit()
										cursor.execute(
										    f"UPDATE users SET cash = cash + {count} WHERE id = {u2_id}"
										)
										write_mes_online(
										    group_ID,
										    f'[id{u_id}|{get_user(u_id)[0]["first_name"]}] передал {count}&#127791; [id{u2_id}|{u2_inf[0]["first_name"]}]'
										)
										connection.commit()
									else:
										write_mes(
										    group_ID,
										    'Нельзя передать деньги самому себе '
										)
								else:
									write_mes(
									    group_ID,
									    'Укажите натуральное число в переделах 10000000'
									)
					elif mes_text[0] in ['!дом', '!дома']:
						try:
							if int(mes_text[1]) in range(1, 10):
								g = 1
							else:
								g == 0
						except:
							g = 0
							prep_list = []
							for i in range(1, 10):
								prep_list.append(
								    f"{str(i)}. {house_text_get(i)} - {bal_pret(house_price_get(i))}&#127791;"
								)
							ready_mes = '\n'.join(prep_list)
							write_mes(
							    group_ID,
							    f'&#127969; Список домов доступных для покупки:\n\n{ready_mes}'
							)

						if g == 1:
							if balance_get(u_id) >= int(
							    house_price_get(int(mes_text[1]))):
								cursor.execute(
								    f"UPDATE users SET cash = cash - {int(phone_price_get(int(mes_text[1])))} WHERE id = {u_id}"
								)
								cursor.execute(
								    f"UPDATE property SET house = {int(mes_text[1])} WHERE id = {u_id}"
								)
								write_mes(group_ID, 'Готово!')

					elif mes_text[0] in ['!телефон', '!телефоны']:
						try:
							if int(mes_text[1]) in range(1, 12):
								g = 1
							else:
								g == 0
						except:
							g = 0
							prep_list = []
							for i in range(1, 12):
								prep_list.append(
								    f"{str(i)}. {phone_text_get(i)} - {bal_pret(phone_price_get(i))}&#127791;"
								)
							ready_mes = '\n'.join(prep_list)
							write_mes(
							    group_ID,
							    f'&#128241; Список телефонов доступных для покупки:\n\n{ready_mes}'
							)

						if g == 1:
							if balance_get(u_id) >= int(
							    phone_price_get(int(mes_text[1]))):
								cursor.execute(
								    f"UPDATE users SET cash = cash - {int(phone_price_get(int(mes_text[1])))} WHERE id = {u_id}"
								)
								cursor.execute(
								    f"UPDATE property SET phone = {int(mes_text[1])} WHERE id = {u_id}"
								)
								write_mes(group_ID, 'Готово!')

					elif mes_text[0] in ['!машина', '!машины']:
						try:
							if int(mes_text[1]) in range(1, 14):
								g = 1
							else:
								g == 0
						except:
							g = 0
							prep_list = []
							for i in range(1, 14):
								prep_list.append(
								    f"{str(i)}. {car_text_get(i)} - {bal_pret(car_price_get(i))}&#127791;"
								)
							ready_mes = '\n'.join(prep_list)
							write_mes(
							    group_ID,
							    f'&#128664; Список машин доступных для покупки:\n\n{ready_mes}'
							)

						if g == 1:
							if balance_get(u_id) >= int(
							    car_price_get(int(mes_text[1]))):
								cursor.execute(
								    f"UPDATE users SET cash = cash - {int(car_price_get(int(mes_text[1])))} WHERE id = {u_id}"
								)
								cursor.execute(
								    f"UPDATE property SET car = {int(mes_text[1])} WHERE id = {u_id}"
								)
								write_mes(group_ID, 'Готово!')

					elif mes_text[0] == '!купить':
						try:
							if mes_text[1] in ['рейтинг', 'рейт']:
								g = 1

							else:
								g = 0
						except:
							g = 0

						try:
							if mes_text[2] in ['all', 'всё', 'все']:
								gg = balance_get(u_id) // 15000000
								print(gg)
								print(balance_get(u_id))
							elif int(mes_text[2]) >= 1:
								gg = int(mes_text[2])
							else:
								write_mes(group_ID,
								          'Число должно быть натуральным')
								gg = 0
						except:

							gg = 1

						if g == 1:

							n = 15000000 * gg
							if n <= balance_get(u_id):
								cursor.execute(
								    f"UPDATE users SET cash = cash - {n} WHERE id = {u_id}"
								)
								connection.commit()
								cursor.execute(
								    f"UPDATE users SET rate = rate + {gg} WHERE id = {u_id}"
								)
								connection.commit()
								print('aaa2')
								write_mes(group_ID, 'Готово!')
							else:
								write_mes(group_ID, 'Иди копи!')

					elif mes_text[0] == '!продать':
						try:
							if mes_text[1] in ['рейтинг', 'рейт']:
								g = 1
							else:
								g = 0
						except:
							g = 0

						try:
							if mes_text[2] in ['all', 'все', 'всё']:
								gg = rate_get(u_id)

							elif int(mes_text[2]) >= 1:
								gg = int(mes_text[2])
							else:
								write_mes(group_ID,
								          'Число должно быть натуральным')
								gg = 1
						except:
							gg = 1

						if g == 1:
							n = 10000000 * gg
							if gg <= rate_get(u_id):
								cursor.execute(
								    f"UPDATE users SET cash = cash + {n} WHERE id = {u_id}"
								)
								connection.commit()
								cursor.execute(
								    f"UPDATE users SET rate = rate - {gg} WHERE id = {u_id}"
								)
								connection.commit()
								write_mes(group_ID, 'Готово!')
							else:
								write_mes(group_ID, 'У тебя столько нету')

					elif mes_text[0] == '+деньги' and u_id in [
					    315625951, 550391377
					]:
						linked()
						if ban_check(u_id) == True:
							try:
								rep_text = event.object.message[
								    'reply_message']['text']
								rep_id = event.object.message['reply_message'][
								    'from_id']
								cursor.execute(
								    f"UPDATE users SET cash = cash + {mes_text[1]} WHERE id = {rep_id}"
								)
								connection.commit()
								write_mes(group_ID, 'Готово, мой повелитель!')
							except:
								try:
									mes_text[1]
									gg = 1
								except:
									gg = 0

								if gg == 1:
									try:
										mes_text[2]
										hh = 1
									except:
										hh = 0
								else:
									write_mes(group_ID,
									          '+деньги <кому> <сколько>')
								if hh == 1:
									p = event.message['text'].split()
									j = list(p[1])
									jj = j.index('|')
									try:
										while True:
											j.pop(jj)
									except:
										j.remove('[')
										j.remove('i')
										j.remove('d')
										j = ''.join(j)
									cursor.execute(
									    f"UPDATE users SET cash = cash + {mes_text[2]} WHERE id = {j}"
									)
									connection.commit()
									write_mes(group_ID,
									          'Готово, мой повелитель!')

					elif mes_text[0] in [
					    'извини', 'прости', 'сорян', 'сорри', 'сори'
					]:
						linked()
						if ban_check(u_id) == False:
							i = random.randint(0, 1)
							sor_ans = [
							    'Извини в карман не положишь :/',
							    'Ты просишь, но делаешь это без уважения',
							    'Нет'
							]
							otvet = sor_ans[i]
							vk.method(
							    'messages.send', {
							        'chat_id': group_ID,
							        'message': otvet,
							        'random_id': get_random_id(),
							        'attachment': 'video315625951_456239157'
							    })
						else:
							pass

					elif mes_text[0] == '!рейтинг':
						rating = []
						rating_list = []
						i = 0
						for t in cursor.execute(
						    f"SELECT * FROM users WHERE rate > 0"):
							t = tuple(reversed(t))
							print(t)
							print('______________________')
							if i <= 20 and t[4] > 0:
								i += 1
								rating_list.append(t)
							else:
								break
						rating_list.reverse()
						rating_list.sort()
						rating_list.reverse()
						print(rating_list)
						e = 1
						for t in rating_list:
							if e <= 10:
								rating.append(
								    f"{e}.[id{t[4]}|{get_user(t[4])[0]['first_name']} {get_user(t[4])[0]['last_name']}] {t[0]}&#128511;"
								)
								e += 1
							else:
								break
						rating_read = '\n'.join(rating)
						write_mes_online(
						    group_ID,
						    f'Топ пользователей бота:\n{rating_read}')

					elif mes_text[0] == '!работы':
						try:
							j = int(mes_text[1])
							if j in range(1, 7):
								ee = 1
							else:
								j = 0
								ee = 0
						except:
							ee = 0
							j = 0

						if ee == 1:
							if j == 1:
								if job_get(u_id) != 1:
									if rate_get(u_id) >= 0:
										cursor.execute(
										    f"UPDATE users SET job_place = 1 WHERE id = {u_id}"
										)
										write_mes(group_ID, 'Готово!')
										connection.commit()
									else:
										write_mes(
										    group_ID,
										    'У вас не хватает рейтинга!')
								else:
									write_mes(group_ID,
									          'Вы и так на этой работе')
							elif j == 2:
								print(j)
								if job_get(u_id) != 2:
									if rate_get(u_id) >= 1:
										cursor.execute(
										    f"UPDATE users SET rate = rate - 1 WHERE id = {u_id}"
										)
										connection.commit()
										cursor.execute(
										    f"UPDATE users SET job_place = 2 WHERE id = {u_id}"
										)
										connection.commit()
										write_mes(group_ID, 'Готово!')
									else:
										write_mes(
										    group_ID,
										    'У вас не хватает рейтинга!')
								else:
									write_mes(group_ID,
									          'Вы и так на этой работе')
							elif j == 3:
								if job_get(u_id) != 3:
									if rate_get(u_id) >= 5:
										cursor.execute(
										    f"UPDATE users SET rate = rate - 5 WHERE id = {u_id}"
										)
										connection.commit()
										cursor.execute(
										    f"UPDATE users SET job_place = 3 WHERE id = {u_id}"
										)
										connection.commit()
										write_mes(group_ID, 'Готово!')
									else:
										write_mes(
										    group_ID,
										    'У вас не хватает рейтинга!')
								else:
									write_mes(group_ID,
									          'Вы и так на этой работе')
							elif j == 4:
								if job_get(u_id) != 4:
									if rate_get(u_id) >= 15:
										cursor.execute(
										    f"UPDATE users SET rate = rate - 15 WHERE id = {u_id}"
										)
										connection.commit()
										cursor.execute(
										    f"UPDATE users SET job_place = 4 WHERE id = {u_id}"
										)
										connection.commit()
										write_mes(group_ID, 'Готово!')
									else:
										write_mes(
										    group_ID,
										    'У вас не хватает рейтинга!')
								else:
									write_mes(group_ID,
									          'Вы и так на этой работе')
							elif j == 5:
								if job_get(u_id) != 5:
									if rate_get(u_id) >= 50:
										cursor.execute(
										    f"UPDATE users SET rate = rate - 50 WHERE id = {u_id}"
										)
										connection.commit()
										cursor.execute(
										    f"UPDATE users SET job_place = 5 WHERE id = {u_id}"
										)
										connection.commit()
										write_mes(group_ID, 'Готово!')
									else:
										write_mes(
										    group_ID,
										    'У вас не хватает рейтинга!')
								else:
									write_mes(group_ID,
									          'Вы и так на этой работе')
							elif j == 6:
								if job_get(u_id) != 6:
									if rate_get(u_id) >= 100:
										cursor.execute(
										    f"UPDATE users SET rate = rate - 100 WHERE id = {u_id}"
										)
										connection.commit()
										cursor.execute(
										    f"UPDATE users SET job_place = 6 WHERE id = {u_id}"
										)
										connection.commit()
										write_mes(group_ID, 'Готово!')
									else:
										write_mes(
										    group_ID,
										    'У вас не хватает рейтинга!')
								else:
									write_mes(group_ID,
									          'Вы и так на этой работе')

						if j == 0:
							write_mes(
							    group_ID,
							    'Доступные работы:\n\n1. Дворник \nЗ/П: 1.000&#127791;\nНеобходимый рейтинг: 0&#128511;\n\n2. Учитель физры \nЗ/П: 2.500&#127791;\nНеобходимый рейтинг: 1&#128511;\n\n3. Программист \nЗ/П: 6.000&#127791;\nНеобходимый рейтинг: 5&#128511;\n\n4. Ведущий геолог \nЗ/П: 10.000&#127791;\nНеобходимый рейтинг: 10&#128511;\n\n5. Директор нефтяного завода \nЗ/П: 25.000&#127791;\nНеобходимый рейтинг: 50&#128511;\n\n6. Нефтяной монополист \nЗ/П: 50.000&#127791;\nНеобходимый рейтинг: 100&#128511;'
							)
					elif mes_text[0] == '+сброс' and u_id == 315625951:
						c6poc = 1
						write_mes(group_ID, 'Сброс времени разрешен!')

					elif mes_text[0] == '-сброс' and u_id == 315625951:
						c6poc = 0
						write_mes(group_ID, 'Сброс времени запрещён!')

					elif mes_text[0] == '!сбросить' and c6poc == 1:
						try:
							if mes_text[1] == 'время':
								cursor.execute(
								    f"UPDATE users SET job_time = 0 WHERE id = {u_id}"
								)
								connection.commit()
							else:
								write_mes(group_ID, 'А чё сбрасывать?')
						except:
							pass
					elif mes_text[0] in ['!рандом', '!ран']:
						try:
							first_int = int(mes_text[1])
						except:
							first_int = 0
						try:
							second_int = int(mes_text[2])
						except:
							second_int = 100

						if first_int < second_int:
							write_mes(group_ID, random.randint(first_int, second_int))
						else:
							write_mes(
							    group_ID,
							    'Первое число должно быть меньше второго')

					elif mes_text[0] in [
					    '!калькулятор', '!каль', '!calc', '!реши'
					]:
						try:
							resh = eval(mes_text[1])
							write_mes(
							    group_ID,
							    f'&#128126; Решение математической задачи:\n{resh}'
							)
						except:
							write_mes(group_ID, 'Укажите пример')

					elif mes_text[0] in ['!дк', '!доступ']:
						foo = 0
						if admin_chat == 9 or group_ID in [1, 2, 9]:
							try:
								command = mes_text[1]
								rank = int(mes_text[2])
								foo = 1
							except:
								write_mes(group_ID, '!дк <комманда> <ранг>')
							if foo == 1 and rank in range(0, 4):
								if command in role:
									cursor.execute(
									    f"UPDATE dk SET роль = '{rank}' WHERE group_id = {group_ID}"
									)
									connection.commit()
									write_mes(
									    group_ID,
									    f'Доступ к командам ролей теперь имеют пользователи с {str(rank)} ролью'
									)
								elif command in warn:
									cursor.execute(
									    f"UPDATE dk SET варн = '{rank}' WHERE group_id = {group_ID}"
									)
									connection.commit()
									write_mes(
									    group_ID,
									    f'Доступ к командам предупреждений теперь имеют пользователи с {str(rank)} ролью'
									)
								elif command in kick:
									cursor.execute(
									    f"UPDATE dk SET kick = {rank} WHERE group_id = {group_ID}"
									)
									connection.commit()
									write_mes(
									    group_ID,
									    f'Доступ к командам кика теперь имеют пользователи с {str(rank)} ролью'
									)
								elif command in ava:
									cursor.execute(
									    f"UPDATE dk SET ава = {rank} WHERE group_id = {group_ID}"
									)
									connection.commit()
									write_mes(
									    group_ID,
									    f'Доступ к командам аватарки теперь имеют пользователи с {str(rank)} ролью'
									)
								else:
									write_mes(
									    group_ID,
									    'Перед использованием посмотрите статью:\nvk.com/@ft_ghoul-base'
									)
							else:
								write_mes(
								    group_ID,
								    'Перед использованием посмотрите статью:\nvk.com/@ft_ghoul-base'
								)
					elif mes_text[0] == '!баланс':
						write_mes(group_ID, f"Ваш баланс: {bal_pret(balance_get(u_id))} {shav}")

					elif mes_text[0] == '!поставить':
						try:
							count = int(mes_text[1])

						except:
							count = 0
							write_mes(group_ID, 'Укажите натуральное число')
						if count <= balance_get(u_id):
							if count in range(1,
							                  10000000000000000000000000000):
								cursor.execute(
								    f"""CREATE TABLE IF NOT EXISTS m{group_ID}(
									id INT,
									stav BIGINT
								)""")
								if cursor.execute(
								    f"SELECT * FROM m{group_ID} WHERE id = {u_id}"
								).fetchone() == None:
									cursor.execute(
									    f"UPDATE users SET cash = cash - {count} WHERE id = {u_id}"
									)
									cursor.execute(
									    f"INSERT INTO m{group_ID} VALUES ({u_id}, {count})"
									)
									connection.commit()
								else:
									cursor.execute(
									    f"UPDATE users SET cash = cash - {count} WHERE id = {u_id}"
									)
									cursor.execute(
									    f"UPDATE m{group_ID} SET stav = stav + {count} WHERE id = {u_id}"
									)
								all_sum = 0
								for item in cursor.execute(
								    f"SELECT stav FROM m{group_ID}"):
									all_sum += item[0]
								print(all_sum)
								summ = cursor.execute(
								    f"SELECT stav FROM m{group_ID} WHERE id = {u_id}"
								).fetchone()[0]
								write_mes(
								    group_ID,
								    f'{nick_get(u_id, group_ID)}, твоя сумма ставки {summ}&#127791;, шанс на победу {round((summ/all_sum)*100, 3)}%\n\nОбщий размер ставки = {all_sum}&#127791;'
								)
						else:
							write_mes(group_ID, 'У тебя нет столько &#127791;')

					elif mes_text[0] == '!начать':
						b = 0
						try:
							for aa in cursor.execute(
							    f"SELECT * FROM m{group_ID}").fetchall():
								b += 1
						except:
							b = 0
						if b != 0:
							REZ = {}
							used = []
							all_sum = 0
							try:
								for item in cursor.execute(
								    f"SELECT stav FROM m{group_ID}"):
									all_sum += item[0]
								ab = 1
							except:
								ab = 0

							if ab == 1:
								for i in cursor.execute(
								    f"SELECT id FROM m{group_ID}").fetchall():
									REZ[i[0]] = []
									summ = cursor.execute(
									    f"SELECT stav FROM m{group_ID} WHERE id = {i[0]}"
									).fetchone()[0]
									per = round((summ / all_sum) * 100)
									per1000 = per * 1000
									if per < 1:
										REZ[i[0]] = [0]
									else:
										for a in range(1, 100):
											if a not in used and a not in REZ[
											    i[0]]:
												REZ[i[0]].append(a)
												used.append(a)
								results = random.randint(1, 100)
								for lists in REZ.values():
									for item1 in lists:
										if results == item1:
											for key in REZ.keys():
												if REZ[key] == lists:
													summ = cursor.execute(
													    f"SELECT stav FROM m{group_ID} WHERE id = {key}"
													).fetchone()[0]
													write_mes(
													    group_ID,
													    f'Победил [id{key}|{nick_get(key, group_ID)}]\nОн выиграл {all_sum} &#127791; с шансом {round((summ/all_sum)*100)}%'
													)
													cursor.execute(
													    f"UPDATE users SET cash = cash + {all_sum} WHERE id = {key}"
													)
													break
										else:
											continue
								cursor.execute(f"DROP TABLE m{group_ID}")
								print('READY')
					elif mes_text[0] == 'ладно':
						write_mes(group_ID, 'Прохладно')
					elif 'урыл' in mes_text:
						write_mes(group_ID, 'Закопал')

					elif mes_text[0] in ['слит', 'слита']:
						try:
							if mes_text[1] == False:
								i = 1
							else:
								i = 0
						except:
							i = 1
						if i == 1:
							write_mes(group_ID, 'Мать твоя слита уёбище')
						else:
							print('123')
					elif mes_text[0] in ['!бизнес', '!бизнесы']:
						cursor.execute("""CREATE TABLE IF NOT EXISTS business(
							id INT,
							bus INT,
							time INT
						)""")
						print(cursor.execute(f"SELECT * FROM business WHERE id = {u_id}").fetchall())
						if cursor.execute(f"SELECT * FROM business WHERE id = {u_id}").fetchall() == []:
							cursor.execute("INSERT INTO business VALUES (?,?,?)", (u_id, 0, 0))
							connection.commit()
						us_b = get_bus(u_id)
						try:
							if mes_text[1] in ['забрать', 'получить']:
								if get_bus(u_id)[1] != 0:
									raz = int(mes_time_u) - int(get_bus(u_id)[2])
									raz = raz//3600
									print(raz)
									if raz > 5:
										raz = 5


									cursor.execute(f"UPDATE users SET cash = cash + {raz * get_bus_d(us_b[1])} WHERE id = {u_id}")
									cursor.execute(f"UPDATE business SET time = {mes_time_u} WHERE id = {u_id}")
									write_mes(group_ID, f'На вас счет зачислено {bal_pret(raz * get_bus_d(us_b[1]))}')
								else:
									write_mes(group_ID, 'У вас еще не куплен бизнес')
							elif mes_text[1] in ['купить']:
								# try:
									if int(mes_text[2]) in range(1,11):
										if balance_get(u_id) >= business_price_get(int(mes_text[2])):
											cursor.execute(f"UPDATE users SET cash = cash - {business_price_get(int(mes_text[2]))} WHERE id = {u_id}")
											cursor.execute(f"UPDATE business SET bus = {int(mes_text[2])}  WHERE id = {u_id}")
											write_mes(group_ID, 'Успешно!')
										else:
											write_mes(group_ID, 'Иди копи!')
									else:
										write_mes(group_ID, 'Такого нет :/')
								
								# except:
								# 	write_mes(group_ID, 'А что покупать?')
							elif mes_text[1] == 'продать':
								if get_bus(u_id)[1] == 0:
									write_mes(group_ID, 'Чтобы продать что-нибудь ненужное, надо сначала купить что-нибудь ненужное')
								else:
									cursor.execute(f"UPDATE users SET cash = cash + {business_price_get(get_bus(u_id)[1])} WHERE id = {u_id}")
									cursor.execute(f"UPDATE business SET bus = 0 WHERE id = {u_id}")
									write_mes(group_ID, 'Успешно!')
							else:
								write_mes(group_ID, 'Такого действия нет')
						except:
							prep = []
							for i in range(1,11):
								prep.append(f'{i}. {business_text_get(i)}\nЦена: {bal_pret(business_price_get(i))}')
							ready = '\n\n'.join(prep)
							write_mes(group_ID, f'Список бизнесов, доступных для покупки:\n\n{ready}')

							
					
					elif mes_text[0] == '!скачать':
						try:
							if event.object.message['attachments'][0]['type']  == 'video':
								owner_id = event.object.message['attachments'][0]['video']['owner_id']
								v_id = event.object.message['attachments'][0]['video']['id']
								write_mes(group_ID, f'Вот ссылка на скачивание:\nsavevk.com/video{owner_id}_{v_id}')
						except:
							write_mes(group_ID, 'Иче качать?')



					elif mes_text[0] == '!сократить':
						try:
							vkcc = vk.method('utils.getShortLink', {'url' : mes_text[1]})
						except:
							vkcc = 'Не указана ссылка'
						print(vkcc)
						write_mes(group_ID, f'Вот, держи:\n{vkcc["short_url"]}')

					elif mes_text[0] in ['!инвестиции', '!инв']:
						write_mes(group_ID, 'Начинаю...')
						r = requests.get('https://www.google.com/search?q=%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D0%B2+%D0%B3%D0%B2%D0%B8%D0%BD%D0%B5%D0%B9%D1%81%D0%BA%D0%B8%D0%B9+%D1%84%D1%80%D0%B0%D0%BD%D0%BA&oq=%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D0%B2+%D0%B3%D0%B2%D0%B8%D0%BD%D0%B5%D0%B9%D1%81%D0%BA%D0%B8%D0%B9+%D1%84%D1%80%D0%B0%D0%BD%D0%BA&aqs=chrome..69i57j33i160l2.5183j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
						soup = BeautifulSoup(r.content, 'html.parser')
						convert = soup.findAll(
								"span", {
										"class": "DFlfde",
										"data-precision": "2"
								})
						print(convert)
						kurs = (convert[0].text)
						kurs = int(float(kurs.replace(',', '')))
						try:
							if mes_text[1] == 'купить':
								try:
									count = int(mes_text[2])
									if balance_get(u_id) >= kurs*count:
										cursor.execute(f"UPDATE users SET cash = cash - {count*kurs} WHERE id = {u_id}")
										cursor.execute(f"UPDATE invest SET count = count + {count} WHERE id = {u_id}")
										connection.commit
										write_mes(group_ID, f'На ваш счёт лачкоинов пополнен на {count}')
									else:
										write_mes(group_ID, 'Иди копи!')
								except:
									write_mes(group_ID, 'А че покупать то...')
						except:


							write_mes(group_ID, f'&#128200; Действующий курс лачкоина: \n{bal_pret(kurs)} &#127791;\nВаш счёт лачкоинов составляет {bal_pret(coins_get(u_id))}')



					elif mes_text[0] == '/время':
						
						vk.method('messages.setActivity', {'type': 'typing','peer_id':2000000000 + group_ID})
						try:
							if mes_text[1] != '':
								mes_text.pop(0)
								gg = ' '.join(mes_text)
								h = 1
							else:
								h = 0
						except:
							h = 0
						
						if h != 0:
					
							f = requests.get(f'https://www.google.com/search?q=время+{gg}', headers=headers)
							soup = BeautifulSoup(f.content, 'html.parser')
							convert = soup.findAll(
									"div", {
											"class": "gsrt vk_bk dDoNo XcVN5d"
									})
							try:
								ready = (convert[0].text)
							except IndexError:
								ready = 'Не удалось определить время'
							write_mes(group_ID, ready)

						else:
							write_mes(group_ID, 'А где?')

					elif mes_text[0] == '/переведи':
						try:
							lan = mes_text[1]
							f = 1
						except:
							write_mes(group_ID, '/переведи <на какой язык(напишите помощь если не знаете что указывать)> <текст>')
							f = 0
						
						if f == 1:
							if lan == 'помощь':
								write_mes(group_ID, '1 - английский\n2 - японский\n3 - немецкий.\nНиже приведён пример перевода слова ШАУРМА на английский')
								lan = 'en'
							if lan == '1':
								lan = 'en'
							elif lan == '2':
								lan = 'ja'
							elif lan == '3':
								lan = 'de'

							try:
								text = mes_text[2]
							except:
								text = 'Шаурма'
							
							r = requests.get(f'https://translate.google.com/?sl=auto&tl={lan}&text={text}&op=translate', headers=headers)
							soup = BeautifulSoup(r.content, 'html.parser')
							print(soup)
							convert = soup.findAll(
								"span", {"jsname":"W297wb"} 
							)
							print(convert)
							try:
								ready = (convert[0].text)
							except:
								ready = 'Не удалось перевести :('
							
							write_mes(group_ID, ready)


					elif mes_text[0] == '!ред':
						try:
							vk.method('messages.removeChatUser', {'chat_id':group_ID, 'member_id':u_id})
						except:
							write_mes(group_ID, 'ясно клоун')
							pass

					elif mes_text[0] == '+пром' and u_id == 315625951:
						print(1)
						
						var = 0
						cursor.execute("""CREATE TABLE IF NOT EXISTS prom(
							id INT,
							name TEXT,
							count INT,
							tries INT,
							used BLOB
						)""")
					
						try:
							title = mes_text_syntax[1]
							print(2)
							try:
								if cursor.execute(f"SELECT * FROM prom WHERE name = '{title}'").fetchall() != []:
									write_mes(group_ID, 'Имя уже занято')
									var = 0
								else:
									kakak = 1 / 0
							except:
								try:
									if cursor.execute(f"SELECT * FROM prom WHERE name = ?", (title, )).fetchall() == []:
										print(3)
										count = int(mes_text[2])
										print(4)
										tries = int(mes_text[3])
										var = 1
									else:
										write_mes(group_ID, 'Имя уже занято')
								except sqlite3.OperationalError:
									print(3)
									count = int(mes_text[2])
									print(4)
									tries = int(mes_text[3])
									var = 1

						except IndexError:
							write_mes(group_ID, '+пром <имя> <награда> <попытки>')
							var = 0
						if var == 1:
							while True:
								r = random.randint(1, 100000)
								if cursor.execute(f"SELECT * FROM prom WHERE id = {r}").fetchall() == []:
									cursor.execute(f"INSERT INTO prom VALUES (?,?,?,?,?)", (r, title, count, tries, pickle.dumps([])))
									connection.commit()
									write_mes(group_ID, f'Создан промокод {title}. При использовании начисляется {count} {shav}. Количество использований {tries}. ID промокода {str(r)}')
									break
					elif mes_text[0] == 'промы' and u_id == 315625951:
						print(cursor.execute(f"SELECT * FROM prom").fetchall())


					elif mes_text[0] == 'пром':
						try:
							title = mes_text_syntax[1]
						except IndexError:
							title = False
							write_mes(group_ID, 'Укажите какой промокод активировать')
						if title:
							if cursor.execute(f"SELECT * FROM prom WHERE name = '{title}'").fetchall() == []:
								write_mes(group_ID, 'Такого промокода нет')
							else:
								if cursor.execute(f"SELECT tries FROM prom WHERE name = '{title}'").fetchone()[0] > 0:
									b_used = cursor.execute(f"SELECT used FROM prom WHERE name = '{title}'").fetchone()[0]
									used = pickle.loads(b_used)
									if u_id in used:
										write_mes(group_ID, 'Вы уже использовали данный промокод')
									else:
										used.append(u_id)
										print(pickle.dumps(used))
										cursor.execute(f"UPDATE prom SET used =(?) WHERE name = '{title}'", (pickle.dumps(used), ))
										connection.commit()
										print('Внесено')
										cash = cursor.execute(f"SELECT count FROM prom WHERE name = '{title}'").fetchone()[0]

										cursor.execute(f"UPDATE prom SET tries = tries - 1 WHERE name = '{title}'")

										cursor.execute(f"UPDATE users SET cash = cash + {cash} WHERE id = {u_id}")

										tr = cursor.execute(f"SELECT tries FROM prom WHERE name = '{title}'").fetchone()[0]

										write_mes(group_ID, f'Вы активировали промокод {title}. На ваш счет зачисленно {cash} {shav}. Осталось активаций {tr}')
										
								else:
									write_mes(group_ID, 'Промокод недействителен')

					elif mes_text[0] == '/гиф' and u_id == 315625951:
						i = 1
						while i != 0:
							t = vk.method('docs.search', {'q':mes_text[1], 'count' : 1, 'offset' : random.randint(1,123)})
							if t['items'][0]['ext'] == 'gif':
								write_mes(group_ID, f'Нашёл всего {t["count"]}', f"doc{t['items'][0]['owner_id']}_{t['items'][0]['id']}")
								break

					elif mes_text[0] == '!гс' and u_id == 315625951:
						try:
							mes_text[2]
							ii = 1
							try:
								la = mes_text[1]
							except:
								la = 'ru'
						except:
							sr = vk.method('docs.getMessagesUploadServer', {'type':'audio_message', 'peer_id':group_ID+2000000000 })
							r = requests.post(sr['upload_url'], files={'file':open('music/1.ogg', 'rb')}).json()
							print(r)
							c = vk.method("docs.save", {'file':r['file']})['audio_message']
							print(c)
							d = 'doc{}_{}'.format(c['owner_id'], c['id'])
							write_mes(group_ID, None, d)
							ii = 0
						if ii == 1:
							mes_text.pop(0)
							mes_text.pop(0)

							speech = gTTS(text = ' '.join(mes_text), lang = la, slow = False)

							speech.save('music/2.ogg')

							sr = vk.method('docs.getMessagesUploadServer', {'type':'audio_message', 'peer_id':group_ID+2000000000 })
							r = requests.post(sr['upload_url'], files={'file':open('music/2.ogg', 'rb')}).json()
							print(r)
							c = vk.method("docs.save", {'file':r['file']})['audio_message']
							print(c)
							d = 'doc{}_{}'.format(c['owner_id'], c['id'])
							write_mes(group_ID, None, d)

					elif mes_text[0] == '!зальго' and u_id == 315625951:
						aa = 1
						try:
							mes_text[1]
						except:
							aa = 0
						if aa == 1:
							mes_text_syntax.pop(0)

							text = ' '.join(mes_text_syntax)
							ready = zalgo.zalgo().zalgofy(text)
							write_mes(group_ID, ready)
						else:
							write_mes(group_ID, 'А кого')
					
					elif mes_text[0] == '!банк':
						print(1)
						cursor.execute("""CREATE TABLE IF NOT EXISTS bank(
							id INT,
							cash INT,
							time INT
						)""")
						try:
							cmd = mes_text[1]
							print(2)
						except:
							cmd = False
							print(3)

						if cmd != False:
							try:
								print(4)
								c = int(mes_text[2])
							except:
								try:
									print(5)
									c = mes_text[2]
								except:
									print(6)
									c = False


							if c != False:
								print(7)
								
								if cmd in ["вложить", "положить"]:
									try:
										cc = int(mes_text[2])
									except:
										write_mes(group_ID, 'Укажите число')
										cc = False
									if cc != False and cc >= 1000:
										cursor.execute(f"UPDATE bank SET cash = cash + {cc} WHERE id = {u_id}")
										write_mes(group_ID, f'Вы вложили {bal_pret(cc)} {shav}. Теперь банковский счёт составляет {bal_pret(bank_bal_get(u_id))}')
									else:
										write_mes(group_ID, f'Минимальная сумма вклада - 1000 {shav}')
							else:
								if cmd == 'посмотреть':
									write_mes(group_ID, f'Ваш банковский счёт: {bal_pret(bank_bal_get(u_id))}')
								elif cmd in ["забрать", "получить"]:
									rz = mes_time_u - cursor.execute(f"SELECT time FROM bank WHERE id = {u_id}").fetchone()[0]
									cc = int((rz//14400)*(bank_bal_get(u_id)/100*3))
									cursor.execute(f"UPDATE users SET cash = cash + {cc + bank_bal_get(u_id)} WHERE id = {u_id}")
									cursor.execute(f"UPDATE bank SET cash = 0 WHERE id = {u_id}")
									connection.commit()
									write_mes(group_ID, f'На ваш баланс зачисленно {bal_pret(cc + bank_bal_get(u_id))} {shav}\nТеперь он составляет {bal_pret(balance_get(u_id))} {shav}.')
								else:
									write_mes(group_ID, 'Такой команды нет')


								
										
						else:
							write_mes(group_ID, f'В банк вы можете вложить деньги и получать каждые 4 часа 3% от вложенных {shav}\nИспользуйте команды:"Забрать", "получить" чтобы забрать деньги со счёта\n"Вложить", "положить" чтобы вложить деньги\n"Посмотреть" чтобы посмотреть баланс вклада')


					elif mes_text[0] == '!эвелина' and group_ID == 1:
						try:
							if mes_text[1] == 'передать' and u_id in [
							    296293821, 315625951
							]:
								try:
									cursor.execute(
									    f"UPDATE a1 SET evelinacoin = evelinacoin + {mes_text[3]} WHERE user_ids = {get_user_id(mes_text[2])}"
									)
									connection.commit()
									write_mes(group_ID, 'Готово!')
								except:
									try:
										cursor.execute(
										    f"UPDATE a1 SET evelinacoin = evelinacoin + {mes_text[2]} WHERE user_ids = {event.object.message['reply_message']['from_id']}"
										)
										connection.commit()
										write_mes(group_ID, 'Готово!')
									except:
										write_mes(
										    group_ID,
										    '!эвелина передать <упоминание> <количество деняг> или !эвелина передать <количество> <в ответ на сообщение>'
										)

						except:
							ev_bal = cursor.execute(
							    f"SELECT evelinacoin FROM a1 WHERE user_ids = {u_id}"
							).fetchone()[0]
							write_mes(
							    group_ID,
							    f'У вас на руках {ev_bal} эвелинакоинов')

					elif 1 == 1:
						try:
							if auto_var == event.object.message['from_id']:
								prep_mes = "".join(mes_text_syntax)
								url = 'https://xu.su/api/send'

								dt = {'bot': 'pbot', 'text': prep_mes}
								hd = {
								    'user_agent':
								    'Mozilla/5.0 (Linux; U; Android 10; ru-ru; Redmi Note 7 Build/QKQ1.190910.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/12.7.4-gn'
								}
								news = requests.post(
								    url, data=dt, headers=hd).json()
								write_mes(group_ID, news['text'])

						except:
							continue
					'''elif event.object.message['from_id'] == 273667139 or mes_text[0] == 'тест':
            if dima_var <= 10:
              dima_otv = ['video315625951_456239154', 'video315625951_456239153']
              ll = random.randint(0,1)
              vk.method('messages.send', {'chat_id' : group_ID, 'message' : 'Ого! Сайты делаешь?\nНаучи взламывать тесты и менять цвет пжпжпжпж', 'random_id': get_random_id(), 'attachment' : dima_otv[ll]})
              dima_var += 1
            elif dima_var == 11:
              write_mes(group_ID, 'Задолбал писать...')
              dima_var += 1
            elif dima_var == 12:
              vk.method('messages.send', {'chat_id' : group_ID, 'message' : 'Мб кикнуть его?...', 'random_id' : get_random_id(), 'keyboard' : kb.get_keyboard()})
              dima_var = 0'''

			else:
				if 'action' in event.raw['object']['message']:
					linked()
					if 'chat_invite_user' == event.raw['object']['message'][
					    'action']['type']:
						if event.raw['object']['message']['action'][
						    'member_id'] in [-199447647, -199139848]:
							print('БОТА ДОБАВИЛИ')
							if event.raw['object']['message']['action'][
							    'member_id'] == bot_id:
								write_mes(
								    group_ID,
								    'Ура, меня добавили!\n«А это батько мой @x3ron»\n\nИнструкция по пользованию: https://vk.com/@ft_ghoul-base'
								)
								cursor.execute(
								    f"INSERT INTO non_admin VALUES ({group_ID})"
								)
								connection.commit()
								write_mes(group_ID,
								          'Дайте права администратора ')
							else:
								write_mes(group_ID, 'Отлично! Мой брат тут!')
						else:
							write_mes(event.chat_id,
							          'Ку, добро пожаловать на помойку.')
							if cursor.execute(
							    f"SELECT * FROM a{group_ID} WHERE user_ids = {u_id}"
							) == None and (admin_chat == 9 or group_ID == 1):
								namE = get_user(user_var)[0]['first_name']
								cursor.execute(
								    f"INSERT INTO a{group_ID} VALUES (?, ?, ?, ?, ?)",
								    (user_var, 0, 0, namE, 'Пусто'))
								print(123)
								connection.commit()

					elif 'chat_kick_user' == event.raw['object']['message'][
					    'action']['type']:
						linked()
						bye_mes = [
						    'Дал дал ушёл', 'Никто не будет по тебе скучать'
						]
						haha = random.randint(0, 1)
						write_mes(group_ID, bye_mes[haha])
					elif 'chat_invite_user_by_link' == event.raw['object'][
					    'message']['action']['type']:
						linked()
						write_mes(group_ID, 'Пф, ссылочники')
