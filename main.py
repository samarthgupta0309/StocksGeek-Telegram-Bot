import config
API = config.API_KEY
import telebot
import yfinance as yf
import helper

bot = telebot.TeleBot(API)

# start : welcome message
@bot.message_handler(commands = ['start'])
def start_bot(message):
  '''Welcome '''
  bot.send_message(message.chat.id, ''' StocksGeek welcomes you\nTo use the bot:\n-To get price of a stock : price ticker_name\n
  -To get news related to the stock : news ticker_name limit(how many recent headlines you need)\n
  -To get advice from expert : expert ticker_name\n
  This is not meant to represent financial advice. Any investments you make using the algorithm, strategy, ideas or given data below is at your own risk \n''')
  bot.send_photo(message.chat.id, 'https://imgur.com/a/7nE9QF9')

# price <ticker_name> : give the recent price of <ticker>
def price_req_func(message):
  '''User asking for the price of the ticker'''
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "price":
    return False
  else:
    return True

@bot.message_handler(func=price_req_func)
def send_price(message):
  '''Send price to the user'''
  request = message.text.split()[1]
  data = yf.download(tickers=request, period='5m', interval='1m')
  if data.size > 0:
    data = data.reset_index()
    data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
    data.set_index('format_date', inplace=True)
    bot.send_message(message.chat.id, data['Close'].to_string(header=False))
  else:
    bot.send_message(message.chat.id, "No data!?")

# news <ticker> : give news of ticker
def news_req_func(message):
  '''User asking for the latest news of the ticker'''
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "news":
    return False
  else:
    return True
@bot.message_handler(func=news_req_func)
def send_news(message):
  '''Send news to the user'''
  request = message.text.split()
  if len(request) <=2:
    bot.send_message(message.chat.id, 'incomplete command\n')
  else:
    ticker = request[1]
    limit = request[2]
  try:
    res = helper.news(ticker, int(limit))
    bot.send_message(message.chat.id, res)
  except:
    bot.send_message(message.chat.id, "Please check the ticker or the server is down.\nTry after some time")

# expert <ticker> : give expert advice
def expert_req_func(message):
  '''User asking for the latest advice of the ticker'''
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "expert":
    return False
  else:
    return True
@bot.message_handler(func=expert_req_func)
def expert_advice(message):
  '''Send expert advice to the user'''
  request = message.text.split()

  ticker = request[1]
  try:
    res = helper.expert_analytics(ticker)
    bot.send_message(message.chat.id, res)
  except:
    bot.send_message(message.chat.id, "Please check the ticker or check the limit or the server is down.\nTry after some time")

# init bot convern : Hi|Yo|Hello|Namaste....
def greet_funct(message):
  '''Start when someone greets the bot'''
  request = message.text.split()
  cmds = ['hi', 'yo', 'hello', 'namaste']
  if request[0].lower() in cmds:
    return True
  else:
    bot.send_message(message.chat.id, '''I am still learing\n Here is the fast tutorial\n
    -To get price of a stock : price ticker_name\n
  -To get news related to the stock : news ticker_name limit(how many recent headlines you need)\n
  -To get advice from expert : expert ticker_name\n
  This is not meant to represent financial advice. Any investments you make using the algorithm, strategy, ideas or given data below is at your own risk \n ''')
    return False

@bot.message_handler(func = greet_funct)
def greet(message):
  '''Greeting message to the user'''
  bot.send_message(message.chat.id, ''' StocksGeek welcomes you\nTo use the bot:\n-To get price of a stock : price ticker_name\n
  -To get news related to the stock : news ticker_name limit(how many recent headlines you need)\n
  -To get advice from expert : expert ticker_name\n
  This is not meant to represent financial advice. Any investments you make using the algorithm, strategy, ideas or given data below is at your own risk \n''')
  bot.send_photo(message.chat.id, 'https://imgur.com/a/7nE9QF9')

bot.polling()
