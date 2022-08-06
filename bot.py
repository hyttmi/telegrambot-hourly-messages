import os
import threading
import telebot
import schedule
import redis
import time

counter = 0

token = os.getenv("TELEGRAM_TOKEN")

bot = telebot.TeleBot(token, parse_mode=None)

r = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

@bot.message_handler(commands=['addmsg'])
def addMsg(message):
  sent = bot.reply_to(message, 'Send the message to me now, it will be added to the scheduled messages.')
  bot.register_next_step_handler(sent, addMsgDB)

@bot.message_handler(commands=['showmsg'])
def showMsg(message):
    keys = r.keys("*")
    if len(keys) > 0:
        for key in keys:
            res = ("ID: " + key + "\nValue: " + r.get(key))
            bot.reply_to(message, res)
    else:
        bot.reply_to(message, "No messages found in database!")
        
@bot.message_handler(commands=['delmsg'])
def delMsg(message):
    sent = bot.reply_to(message, 'Okay, send me the ID of the message!')
    bot.register_next_step_handler(sent, delMsgDB)

@bot.message_handler(commands=['start'])
def startTimer(message):
    keys = r.keys("*")
    if len(keys) > 0:
        args = message.text.split()
        if len(args) > 1 and args[1].isdigit():
            min = int(args[1])
            schedule.every(min).minutes.do(sendMsg, message.chat.id).tag(message.chat.id)
            bot.reply_to(message, "Timer started!")
            running = True
        else:
            bot.reply_to(message, "Usage: /start <minutes>")
    else:
        bot.reply_to(message, "There's no messages added to the database, can't start the bot!")

    return running

@bot.message_handler(commands=['stop'])
def stopTimer(message):
    schedule.clear(message.chat.id)
    bot.reply_to(message, "Timer stopped!")

def addMsgDB(message):
    r.set(message.date, message.text)
    bot.reply_to(message,"Message added to database!")

def delMsgDB(message):
    id = message.text
    keys = r.keys(id)
    if keys:
        r.delete(id)
        bot.reply_to(message, "ID " + id + " deleted!")
    else:
        bot.reply_to(message,"ID not found!")

def sendMsg(chat_id):
    global counter
    keys = r.keys("*")
    if len(keys) == 0:
        schedule.clear()
        bot.send_message(chat_id, "No messages in database, timer stopped!")
        return
    try:
        res = r.get(keys[counter])
        idx = len(keys)
        print(idx)
        if counter < idx:
            bot.send_message(chat_id, res)
            counter += 1
        else:
            counter = 0
            bot.send_message(chat_id, res)
    except IndexError:
        counter = 0
        res = r.get(keys[counter])
        idx = len(keys)
        bot.send_message(chat_id, res)


if __name__ == "__main__":
    threading.Thread(target=bot.infinity_polling, name="bot_infinity_polling", daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)