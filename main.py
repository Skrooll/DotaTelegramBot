from settings import token
from dotaBuffParser import Parser
import telebot
from telebot import types

bot = telebot.TeleBot(token, parse_mode=None)
parser = Parser()

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing? Type /help for help.")
    
@bot.message_handler(commands=['help'])
def send_help(message):
	bot.reply_to(message, "/herodata if you want to know statistics for specific hero\n/counter if you need to counter enemy heroes\n/profile if you want profile data")
    
@bot.message_handler(commands=['herodata'])
def send_herodata(message):
    msg = bot.reply_to(message, "What hero do you want to pick?")
    bot.register_next_step_handler(msg, process_hero)

def process_hero(message):
    try:
        chat_id = message.chat.id
        name = message.text
        msg = bot.reply_to(message, parser.getHeroData(name))
    except Exception as e:
        bot.reply_to(message, e)
    
@bot.message_handler(commands=['counter'])
def send_pickhelper(message):
    msg = bot.reply_to(message, "What heros do your enemies have?")
    bot.register_next_step_handler(msg, process_emenies)

def process_emenies(message):
    chat_id = message.chat.id
    text = message.text
    suggested =  parser.getCounterPick(text.split(', '))
    msg = bot.reply_to(message, "We suggest you to pick {0}, {1}, {2}, {3} or {4}".format(*suggested))

@bot.message_handler(commands=['profile'])
def send_herodata(message):
    msg = bot.reply_to(message, "Tell me SteamID32 of that profile")
    bot.register_next_step_handler(msg, process_id)

def process_id(message):
    try:
        chat_id = message.chat.id
        name = message.text
        msg = bot.reply_to(message, parser.getProfileData(name))
    except Exception as e:
        bot.reply_to(message, e)

bot.polling()