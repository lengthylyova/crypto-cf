import json
import requests
from datetime import datetime
from app.settings import api_url


def get_avg_price(symbol):
	params = {'symbol': symbol}
	url = api_url + 'avgPrice'
	try:
		r = requests.get(url, params=params)
	except:
		return 'Something wrong...' 
	price = r.json()['price']
	current_time = datetime.now().isoformat(sep=' ', timespec='seconds')

	return f'{current_time}' + f'{symbol: ^20}' + f'price: {price}'
