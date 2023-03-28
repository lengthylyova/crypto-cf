from time import sleep
import threading
from datetime import datetime
from app.reqs import get_avg_price as gap
from app.settings import primary_symbol as primary, secondary_symbol as secondary
from app.settings import period as time, freq
import os

n = time*60 // freq


def data_append(primary, secondary):
	timer = threading.Timer(freq, data_append, args=(primary, secondary))
	timer.start()

	p_data = open('app/data/primary.txt', 'a')
	s_data = open('app/data/secondary.txt', 'a')

	p_data.write(f'{gap(primary)}\n')
	s_data.write(f'{gap(secondary)}\n')

	p_data.close()
	s_data.close()

	return True


def data_clear():
	open('app/data/primary.txt', 'w').close()
	open('app/data/secondary.txt', 'w').close()
	return True


def correlation_analysis():
	timer = threading.Timer(time*60, correlation_analysis)
	timer.start()

	p = list(open('app/data/primary.txt', 'r').read().splitlines())
	s = list(open('app/data/secondary.txt', 'r').read().splitlines())

	data_clear()

	for i in range(len(p)):
		p[i] = float(p[i].split(' ')[-1])
		s[i] = float(s[i].split(' ')[-1])

	p_avg = round(sum(p) / n, 8)
	s_avg = round(sum(s) / n, 8)

	# (x[i] - x[avg])^2
	p_pavg = []
	s_savg = []

	# (x[i] - x[avg])(y[i] - y[avg])
	ps_psavg = []

	for i in range(n):
		p_pavg.append((p[i] - p_avg)**2)
		s_savg.append((s[i] - s_avg)**2)
		ps_psavg.append((p[i] - p_avg)*(s[i] - s_avg))

	result = sum(ps_psavg) / (sum(p_pavg)*sum(s_savg))**0.5

	if result < 0.5 and result > 0.5:
		print(f'Correlation coef is GOOD: {result}')
		if max(p[0], p[-1]) / min(p[0],p[-1]) >= 1.01:
			print(f'PRICE CHANGE MORE THAN 1%')

	return result


def is_more_percent():
	p_data = open('app/data/primary.txt', 'r')
	first = p_data.readlines()[0]
	last = p_data.readlines()[-1]
	if (max(first, last) / min(first, last)) > 1.01:
		return True
	return False



def app():
	print('\nStarting the process...', end='\n\n')
	print(f'Period: {time} *minutes*')
	print(f'Freq: {freq} *seconds*')
	print(f'Primary Symbol: {primary}')
	print(f'Secondary Symbol: {secondary}')
	print(f'Start time: {datetime.now().isoformat(sep=" ", timespec="seconds")}\n\n')

	data_clear()

	t1 = threading.Thread(target=data_append, args=(primary, secondary))
	t1.start()
	print(f'Thread1 (target=data_append) started...')

	timer = threading.Timer(time*60, correlation_analysis)
	timer.start()
	
	print(f'Thread2 (target=correlation_analysis) started...')
