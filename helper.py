import finviz
def news(ticker, limit):
  news = list(finviz.get_news(ticker))
  response = ''
  for idx, part_news in enumerate(news):
    if(idx < limit):
      response += f'{idx+1})\n'
      for j in part_news:
        response += f"{j}\n"
  return response

def expert_analytics(ticker):
  info = finviz.get_analyst_price_targets(ticker)
  response =''
  response = 'This is not meant to represent financial advice. Any investments you make using the algorithm, strategy, ideas or given data below is at your own risk \n'
  for idx, item in enumerate(info):
    response += f'{idx+1})\n'
    for key, val in item.items():
      response += f'{key} - {val}\n'
  return response
