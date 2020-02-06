from rest_framework.views import APIView
from django.db.utils import IntegrityError
from rest_framework.response import Response
from api.functions.button import (
	numb_of_choice,
	start_buttons,
	empy_fun,
	move_end,
	approve,
	option_two_markup,
	option_four_markup,
)
from apps.question.models.second import Second
from apps.user.models.user import User
from apps.user.models.answered import Answer
from apps.question.models.four import FourChoice
from api.functions.bot_token import get_token
from api.functions.rank import find_rank

import telebot
bot = telebot.TeleBot('861845521:AAGOh5OtNoLPc1P_QkObcl363nTuWhmEXMo')

qs = {
	
}

class UpdateBot(APIView):
	def post(self,request):
		json_string = request.body.decode('UTF-8')
		update = telebot.types.Update.de_json(json_string)
		bot.process_new_updates([update])
		return Response({'code':200})


@bot.message_handler(commands=['start'])
def start(message):
	hello = "MathLink botiga xushkelibsiz!!!"
	sent = bot.send_message(message.chat.id, hello, reply_markup=start_buttons())


@bot.message_handler(content_types='text')
def send_Message(message):
	if message.text == 'Savol yaratish':
		sent = bot.send_message(message.chat.id, "Javoblar sonni tanlang!", reply_markup=numb_of_choice())
	elif message.text == "2":
		sent = bot.send_message(message.chat.id, "Savolni kiriting", reply_markup=move_end())
		bot.register_next_step_handler(sent, text2_question)
	elif message.text == "4":
		sent = bot.send_message(message.chat.id, "Savolni kiriting", reply_markup=move_end())
		bot.register_next_step_handler(sent, text4_question)
	else:
		bot.send_message(message.chat.id, 'Siz xato so\'zni yubording\'iz qaytadan boshlang!', reply_markup=start_buttons())


def text2_question(message):
	chat_id = message.chat.id
	que_text = message.text
	new_qs = Second.objects.create(text=que_text)
	new_qs.save()
	qs[chat_id] = new_qs.id
	sent = bot.send_message(chat_id, "Savolning to\'g\'ri javobini kiriting!")
	bot.register_next_step_handler(sent, answer2)


def answer2(message):
	chat_id = message.chat.id
	que_answer = message.text
	new_qs = Second.objects.get(pk=qs[chat_id])
	new_qs.answer = que_answer
	new_qs.save()
	pro_message = "To\'g\'ri javobni tushuntiradigan izoh kiriting!"
	sent = bot.send_message(chat_id, pro_message)
	bot.register_next_step_handler(sent, description2)

def description2(message):
	chat_id = message.chat.id
	que_answer = message.text
	new_qs = Second.objects.get(pk=qs[chat_id])
	new_qs.description = que_answer
	new_qs.save()
	pro_message = "Keyingi tugma javobini kiriting!"
	sent = bot.send_message(chat_id, pro_message)
	bot.register_next_step_handler(sent, two_option2)


def two_option2(message):
	chat_id = message.chat.id
	que_answer = message.text
	new_qs = Second.objects.get(pk=qs[chat_id])
	new_qs.option1 = que_answer
	new_qs.save()
	pro_message = "Savolning rasmini yuboring!"
	sent = bot.send_message(chat_id, pro_message)
	bot.register_next_step_handler(sent, two_photo2)


@bot.message_handler(content_types=['photo'])
def two_photo2(message):
	chat_id = message.chat.id
	message_id = message.message_id
	que_photo = message.photo
	try:
		fileId = message.photo[-1].file_id
	except TypeError:
		new_photo = Second.objects.get(pk=qs[chat_id])
		new_photo.delete()
		bot.send_message(chat_id, 'Siz rasm yubormadingiz qaytadan boshlang', reply_markup=start_buttons())
	new_photo = Second.objects.get(pk=qs[chat_id])
	new_photo.image = fileId
	new_photo.message_id = message_id
	new_photo.save()
	savol = new_photo.text
	bot.send_photo(chat_id, fileId, " {} ".format(savol),
		reply_markup=option_two_markup(message_id))
	sent =  bot.send_message(chat_id, 'Savolni ko\'zdan kechiring.Agar sizga ma\'qul bo\'lsa Ha ni tanlang!', reply_markup=approve())
	bot.register_next_step_handler(sent, two_send_image2)



def two_send_image2(message):
	chat_id = message.chat.id
	if message.text=="Ha":
		new_photo = Second.objects.get(pk=qs[chat_id])
		fileId = new_photo.image
		savol = new_photo.text
		message_id = new_photo.message_id
		bot.send_photo('@mathtest_23', fileId, " {} ".format(savol),
		reply_markup=option_two_markup(message_id))
		bot.send_message(chat_id, "Kanalga tashlandi!", reply_markup=start_buttons())
	if message.text =="Yo\'q":
		query = Second.objects.get(pk=qs[chat_id])
		query.delete()
		bot.send_message(chat_id, "Boshidan boshlang!", reply_markup=start_buttons())




def text4_question(message):
	chat_id = message.chat.id
	que_text = message.text
	new_qs = FourChoice.objects.create(text=que_text)
	new_qs.save()
	qs[chat_id] = new_qs.id
	sent = bot.send_message(chat_id, "Savolning to\'g\'ri javobini kiriting")
	bot.register_next_step_handler(sent, answer4)

def answer4(message):
	chat_id = message.chat.id
	que_answer = message.text
	new_qs = FourChoice.objects.get(pk=qs[chat_id])
	new_qs.answer = que_answer
	new_qs.save()
	pro_message = "To\'g\'ri javobni tushuntiradigan izoh kiriting!"
	sent = bot.send_message(chat_id, pro_message)
	bot.register_next_step_handler(sent, description4)

def description4(message):
	chat_id = message.chat.id
	que_answer = message.text
	new_qs = FourChoice.objects.get(pk=qs[chat_id])
	new_qs.description = que_answer
	new_qs.save()
	pro_message = "Birinchi javob optionni kiriting!"
	sent = bot.send_message(chat_id, pro_message)
	bot.register_next_step_handler(sent, option1)

def option1(message):
	chat_id = message.chat.id
	que_answer = message.text
	new_qs = FourChoice.objects.get(pk=qs[chat_id])
	new_qs.option1 = que_answer
	new_qs.save()
	pro_message = "Ikkinchi javob optionni kiriting!"
	sent = bot.send_message(chat_id, pro_message)
	bot.register_next_step_handler(sent, option2)

def option2(message):
	chat_id = message.chat.id
	que_answer = message.text
	new_qs = FourChoice.objects.get(pk=qs[chat_id])
	new_qs.option2 = que_answer
	new_qs.save()
	pro_message = "Uchunchi javob optionni kiriting!"
	sent = bot.send_message(chat_id, pro_message)
	bot.register_next_step_handler(sent, option3)

def option3(message):
	chat_id = message.chat.id
	que_answer = message.text
	new_qs = FourChoice.objects.get(pk=qs[chat_id])
	new_qs.option3 = que_answer
	new_qs.save()
	pro_message = "Savolning rasmini yuboring!"
	sent = bot.send_message(chat_id, pro_message)
	bot.register_next_step_handler(sent, photo4)


@bot.message_handler(content_types=['photo'])
def photo4(message):
	chat_id = message.chat.id
	message_id = message.message_id
	que_photo = message.photo
	try:
		fileId = message.photo[-1].file_id
	except TypeError :
		new_photo = FourChoice.objects.get(pk=qs[chat_id])
		new_photo.delete()
		bot.send_message(chat_id, 'Siz rasm yubormadingiz qaytadan boshlang!', reply_markup=start_buttons())
	new_photo = FourChoice.objects.get(pk=qs[chat_id])
	new_photo.image = fileId
	new_photo.message_id = message_id
	new_photo.save()
	savol = new_photo.text
	bot.send_photo(chat_id, fileId, " {} ".format(savol),
		reply_markup=option_four_markup(message_id))
	sent =  bot.send_message(chat_id, 'Savolni ko\'zdan kechiring.Agar sizga ma\'qul bo\'lsa Ha ni tanlang!', reply_markup=approve())
	bot.register_next_step_handler(sent, send_image4)


def send_image4(message):
	chat_id = message.chat.id
	if message.text=="Ha":
		new_photo = FourChoice.objects.get(pk=qs[chat_id])
		fileId = new_photo.image
		savol = new_photo.text
		message_id = new_photo.message_id
		bot.send_photo('@mathtest_23', fileId, " {} ".format(savol),
		reply_markup=option_four_markup(message_id))
		bot.send_message(chat_id, "Tashlandi!", reply_markup=start_buttons())
	if message.text =="Yo\'q":
		query = FourChoice.objects.get(pk=qs[chat_id])
		query.delete()
		bot.send_message(chat_id, "Boshidan boshlang!", reply_markup=start_buttons())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	if call.data[:1] =="5":
		first_name = call.from_user.first_name
		last_name = call.from_user.last_name
		username = call.from_user.username
		user_id = call.from_user.id 
		check_user = User.objects.filter(user_id=user_id)
		if not check_user:
			new_user = User.objects.create(first_name=first_name,last_name=last_name,username=username,user_id=user_id)
		qs = Second.objects.get(message_id=call.data[6:])
		get_user_id = User.objects.filter(user_id=user_id)[0]
		filter_user = Answer.objects.filter(message_id=call.data[6:], user_id=get_user_id)
		user = Answer.objects.filter(user=get_user_id, bool_answer=True)
		get_user_rank = find_rank(user_id)
		if not filter_user:
			if call.data[:5]== "5opt1":
				qs.ans_false+=1
				login_qs = Answer.objects.create(message_id=call.data[6:], user=get_user_id)
				login_qs.number+=1
				login_qs.choose_answer = "5opt1"
				login_qs.save()
				qs.save()
				all_ans = qs.ans_false  + qs.ans_true 
				change = round((qs.ans_false)/(all_ans),2)*100
				bot.answer_callback_query(call.id, "❌ Noto\'g\'ri!\n\n🎗️ {} \n\nSizdek javob berishdi: {} foydalanuvchi: ({}%) \n\n💯 Sizning jami to\'g\'ri javoblaringiz: {} \n\n🏆 Sizning o\'rningiz: {} ".format(qs.description, qs.ans_false, change, len(user), get_user_rank), True)
			elif call.data[:5] == "5ans2":
				qs.ans_true+=1
				login_qs = Answer.objects.create(message_id=call.data[6:], user=get_user_id)
				login_qs.number +=2
				login_qs.choose_answer = "5ans2"
				login_qs.bool_answer=True
				get_user_id.numb_of_true_answer+=1
				get_user_id.save()
				login_qs.save()
				qs.save()
				change = round((qs.ans_true)/(qs.ans_true+qs.ans_false),2)*100
				new_len = len(user) + 1
				bot.answer_callback_query(call.id, "✅ To\'g\'ri!\n\n🎗️ {} \n\n🧑 Sizdek javob berishdi: {} foydalanuvchi ({}%) \n\n💯 Sizning jami to\'g\'ri javoblaringiz: {} \n\n🏆 Sizning o\'rningiz: {} ".format(qs.description, qs.ans_true, change, new_len, get_user_rank), True)
        
		else:
			k = Answer.objects.filter(message_id=call.data[6:], user=get_user_id)
			user = Answer.objects.filter(user=get_user_id, bool_answer=True)
			all_ans = qs.ans_false  + qs.ans_true
			if k[0].choose_answer == call.data[:5]:
				if k[0].number == 1:
					change = round((qs.ans_false)/(all_ans),2)*100
					bot.answer_callback_query(call.id, "❌ Noto\'g\'ri!\n\n🎗️ {} \n\n🧑 Sizdek javob berishdi: {} foydalanuvchi ({}%) \n\n💯 Sizning jami to\'g\'ri javoblaringiz: {} \n\n🏆 Sizning o\'rningiz: {} ".format(qs.description, qs.ans_false, change, len(user), get_user_rank), True)
				elif k[0].number == 2:
					change = round((qs.ans_true)/(qs.ans_true+qs.ans_false),2)*100

					bot.answer_callback_query(call.id, "✅ To\'g\'ri!\n\n🎗️ {} \n\n🧑 Sizdek javob berishdi: {} foydalanuvchi ({}%) \n\n💯 Sizning jami to\'g\'ri javoblaringiz: {} \n\n🏆 Sizning o\'rningiz: {} ".format(qs.description, qs.ans_true, change, len(user), get_user_rank), True)
			else:
				if k[0].number == 1:
					bot.answer_callback_query(call.id, "⚠️ Siz allaqachon {} javobni tanlagansiz! ".format(qs.option1))
				elif k[0].number == 2:
					bot.answer_callback_query(call.id, "⚠️ Siz allaqachon {} javobni tanlagansiz! ".format(qs.answer))
	elif call.data[:1] =="4":
		first_name = call.from_user.first_name
		last_name = call.from_user.last_name
		username = call.from_user.username
		user_id = call.from_user.id 
		check_user = User.objects.filter(user_id=user_id)
		if not check_user:
			new_user = User.objects.create(first_name=first_name,last_name=last_name,username=username,user_id=user_id)
		qs = FourChoice.objects.get(message_id=call.data[6:])
		get_user_id = User.objects.filter(user_id=user_id)[0]
		user = Answer.objects.filter(user=get_user_id, bool_answer=True)
		filter_user = Answer.objects.filter(message_id=call.data[6:], user=get_user_id)
		get_user_rank = find_rank(user_id)
		if not filter_user:	
			if call.data[:5]== "4opt1":
				qs.numb_of_option1+=1
				login_qs = Answer.objects.create(message_id=call.data[6:], user=get_user_id)
				login_qs.number+=1
				login_qs.choose_answer = "4opt1"
				login_qs.save()
				qs.save()
				all_ans = qs.numb_of_option1 + qs.numb_of_option2 + qs.numb_of_option3 + qs.true_answer
				change = round((qs.numb_of_option1)/(all_ans),2)*100
				bot.answer_callback_query(call.id, "❌ Noto\'g\'ri! \n\n 🎗️ {} \n\n🧑 Sizdek javob berishdi: {} foydalanuvchi ({}%) \n\n💯 Sizning jami to\'g\'ri javoblaringiz: {}  \n\n🏆 Sizning o\'rningiz: {}".format(qs.description, qs.numb_of_option1, change, len(user), get_user_rank), True)
			elif call.data[:5]== "4opt2":
				qs.numb_of_option2+=1
				login_qs = Answer.objects.create(message_id=call.data[6:], user=get_user_id)
				login_qs.number+=2
				login_qs.choose_answer = "4opt2"
				login_qs.save()
				qs.save()
				all_ans = qs.numb_of_option1 + qs.numb_of_option2 + qs.numb_of_option3 + qs.true_answer
				change = round((qs.numb_of_option2)/(all_ans),2)*100
				bot.answer_callback_query(call.id, "❌ Noto\'g\'ri! \n\n 🎗️ {} \n\n🧑 Sizdek javob berishdi: {} foydalanuvchi ({}%) \n\n💯 Sizning jami to\'g\'ri javoblaringiz: {}  \n\n🏆 Sizning o\'rningiz: {}".format(qs.description, qs.numb_of_option2, change, len(user), get_user_rank), True)
			elif call.data[:5]== "4opt3":
				qs.numb_of_option3+=1
				login_qs = Answer.objects.create(message_id=call.data[6:], user=get_user_id)
				login_qs.number+=3
				login_qs.choose_answer = "4opt3"
				login_qs.save()
				qs.save()
				all_ans = qs.numb_of_option1 + qs.numb_of_option2 + qs.numb_of_option3 + qs.true_answer
				change =round((qs.numb_of_option3)/(all_ans),2)*100
				bot.answer_callback_query(call.id, "❌ Noto\'g\'ri! \n\n 🎗️ {} \n\n🧑 Sizdek javob berishdi: {} foydalanuvchi ({}%) \n\n💯 Sizning jami to\'g\'ri javoblaringiz: {}  \n\n🏆 Sizning o\'rningiz: {}".format(qs.description, qs.numb_of_option3, change, len(user), get_user_rank), True)
			elif call.data[:5]== "4ans4":
				qs.true_answer+=1
				login_qs = Answer.objects.create(message_id=call.data[6:], user=get_user_id)
				login_qs.number+=4
				login_qs.choose_answer = "4ans4"
				login_qs.bool_answer=True
				get_user_id.numb_of_true_answer+=1
				get_user_id.save()
				login_qs.save()
				qs.save()
				all_ans = qs.numb_of_option1 + qs.numb_of_option2 + qs.numb_of_option3 + qs.true_answer
				change = round((qs.true_answer)/(all_ans),2)*100
				new_len = len(user) + 1
				bot.answer_callback_query(call.id, " ✅ To\'g\'ri! \n\n 🎗️ {} \n\n🧑 Sizdek javob berishdi: {} foydalanuvchi ({}%) \n\n💯 Sizning jami to\'g\'ri javoblaringiz :{}  \n\n🏆 Sizning o\'rningiz: {}".format(qs.description, qs.true_answer, change, new_len, get_user_rank), True)
		else:
			k = Answer.objects.filter(message_id=call.data[6:], user=get_user_id)
			all_ans = qs.numb_of_option1 + qs.numb_of_option2 + qs.numb_of_option3 + qs.true_answer
			user = Answer.objects.filter(user=get_user_id, bool_answer=True)
			get_user_rank = find_rank(user_id)
			if k[0].choose_answer == call.data[:5]:
				if k[0].number == 1:
					change = round((qs.numb_of_option1)/(all_ans),2)*100
					bot.answer_callback_query(call.id, "❌ Noto\'g\'ri! \n\n 🎗️ {} \n\n🧑 Sizdek javob berishdi: {} foydalanuvchi ({}%) \n\n Sizning jami to\'g\'ri javoblaringiz: {}  \n\n🏆 Sizning o\'rningiz: {}".format(qs.description, qs.numb_of_option1, change, len(user), get_user_rank), True)
				elif k[0].number == 2:
					change = round((qs.numb_of_option2)/(all_ans),2)*100
					bot.answer_callback_query(call.id, " ❌ Noto\'g\'ri! \n\n 🎗️ {} \n\n🧑 Sizdek javob berishdi: {} foydalanuvchi ({}%) \n\n💯 Sizning jami to\'g\'ri javoblaringiz: {}  \n\n🏆 Sizning o\'rningiz: {}".format(qs.description, qs.numb_of_option2, change, len(user), get_user_rank), True)
				elif k[0].number == 3:
					change = round((qs.numb_of_option3)/(all_ans),2)*100
					bot.answer_callback_query(call.id, " ❌ Noto\'g\'ri! \n\n 🎗️ {} \n\n🧑 Sizdek javob berishdi: {} foydalanuvchi ({}%) \n\n💯 Sizning jami to\'g\'ri javoblaringiz: {}  \n\n🏆 Sizning o\'rningiz: {}".format(qs.description, qs.numb_of_option3, change, len(user), get_user_rank), True)
				elif k[0].number == 4:
					change = round((qs.true_answer)/(all_ans),2)*100
					bot.answer_callback_query(call.id, "✅ To\'g\'ri! \n\n 🎗️ {} \n\n🧑 Sizdek javob berishdi: {} foydalanuvchi ({}%) \n\n💯Sizning jami to\'g\'ri javoblaringiz: {} \n\n🏆 Sizning o\'rningiz: {} ".format(qs.description, qs.true_answer, change, len(user), get_user_rank), True)
			else:
				if k[0].number == 1:
					bot.answer_callback_query(call.id, "⚠️ Siz allaqachon {} javobni tanlagansiz! ".format(qs.option1))
				elif k[0].number == 2:
					bot.answer_callback_query(call.id, "⚠️ Siz allaqachon {} javobni tanlagansiz! ".format(qs.option2))
				elif k[0].number == 3:
					bot.answer_callback_query(call.id, "⚠️ Siz allaqachon {} javobni tanlagansiz! ".format(qs.option3))
				elif k[0].number == 4:
					bot.answer_callback_query(call.id, "⚠️ Siz allaqachon {} javobni tanlagansiz!".format(qs.answer))