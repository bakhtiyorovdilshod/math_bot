from telebot.types import ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
import telebot
import random
from apps.question.models.second import Second
from apps.question.models.four import FourChoice

def numb_of_choice():
	key = ReplyKeyboardMarkup(True, False)
	button1 = KeyboardButton("2")
	button2 = KeyboardButton("4")
	key.add(button1, button2)
	return key


def main_start():
	key = ReplyKeyboardMarkup(True, False)
	button1 = KeyboardButton('Boshlash')
	button2 = KeyboardButton('Tekshirish')
	key.add(button1, button2)
	return key

def start_buttons():
    key = ReplyKeyboardMarkup(True,False)
    button1 = KeyboardButton('Savol yaratish')
    key.add(button1)
    return key

def empy_fun():
	button_empty = ReplyKeyboardRemove()
	return button_empty

def move_end():
	key = ReplyKeyboardMarkup(True,False)
	back = KeyboardButton('orqaga')
	key.add(back)
	return key

def approve():
	key = ReplyKeyboardMarkup(True,False)
	yes = KeyboardButton("Ha")
	no = KeyboardButton("Yo\'q")
	key.add(yes, no)
	return key

def option_two_markup(info_id):
	choice = random.randint(0, 2)
	qs = Second.objects.get(message_id=info_id)
	opt1 = qs.option1
	opt2 = qs.answer
	markup = InlineKeyboardMarkup()
	markup.row_width = 2
	true = InlineKeyboardButton(opt1, callback_data="5opt1:{}".format(info_id))
	false = InlineKeyboardButton(opt2, callback_data="5ans2:{}".format(info_id))
	if choice==1:
		markup.add(true, false)
	else:
		markup.add(false, true)
	return markup


def option_four_markup(data_id):
	choice = random.randint(0, 4)
	qs = FourChoice.objects.get(message_id=data_id)
	opt1 = qs.option1
	opt2 = qs.option2
	opt3 = qs.option3
	ans = qs.answer
	markup = InlineKeyboardMarkup()
	markup.row_width = 2
	option1 = InlineKeyboardButton(opt1, callback_data="4opt1:{}".format(data_id))
	option2 = InlineKeyboardButton(opt2, callback_data="4opt2:{}".format(data_id))
	option3 = InlineKeyboardButton(opt3, callback_data="4opt3:{}".format(data_id))
	answer = InlineKeyboardButton(ans, callback_data="4ans4:{}".format(data_id))
	if choice==1:
		markup.add(option1, answer)
		markup.add(option3, option2)
	elif choice==2:
		markup.add(answer, option2)
		markup.add(option1, option3)
	elif choice==3:
		markup.add(option3, answer)
		markup.add(option1, option2)
	else:
		markup.add(answer, option2)
		markup.add(option1, option3)
	return markup