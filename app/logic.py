from time import sleep
from datetime import datetime
from app.reqs import get_avg_price as gap
from app.settings import primary_symbol as primary, secondary_symbol as secondary
from app.settings import period as time, freq
import os

n = time*60 // freq


def data_append(primary, secondary):
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
	p = open('app/data/primary.txt', 'r').read().splitlines()
	s = open('app/data/secondary.txt', 'r').read().splitlines()

	for i in range(n):
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

	while True:
		data_clear()

		for i in range(n):
			data_append(primary, secondary)
			sleep(freq)

		c = correlation_analysis()

		if c > 0.5 or c < -0.5:
			print(f'correlation analys not good ({c})...')
		else:
			print(f'correlation analys is good ({c})!')
			if is_more_percent:
				print(f"1% CHANGE! {datetime.now()}")
