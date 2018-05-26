from multiprocessing import Process, Pool
from Traffic_generation.ddos import ddos
from Traffic_generation.SYNflood import synFlood


def f():
    while True:
        print('sb')

if __name__ == "__main__":
	p = Pool(2)
	print(2)
	for i in range(2):
		p.apply_async(synFlood)
	p.close()
	p.join()
