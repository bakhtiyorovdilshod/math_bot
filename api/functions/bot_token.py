import telebot

def get_token(token):
	bot = telebot.TeleBot(token)
	return bot