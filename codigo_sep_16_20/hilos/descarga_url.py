"""
Codigo de ejemplo para descargar una URL
"""

import urllib.request as urllib2
from threading import Thread


class Download(Thread):

	def __init__(self, ini, fin):
		Thread.__init__(self)
		self.ini = ini
		self.fin = fin

	def run(self):
		for i in range(self.ini, self.fin):
			url = f"http://localhost:8000/fich{i}.txt"
			print(url)
			numero = self.__descargaURL(url)
			print(numero)

	def __descargaURL(self, url):
		f = None
		numero = None
		
		try:
			f = urllib2.urlopen(url)                
			numero = int(f.read())
			return numero
				
		except Exception as e:
			print("ERROR: ", e)
			
		finally:
			if f != None: f.close()
			

if __name__=='__main__':
	num_hilos = 5
	num_ficheros = 100
	num_fich_hilo = num_ficheros // num_hilos

	hilos = []
	L = [(i*num_fich_hilo, i*num_fich_hilo+num_fich_hilo) for i in range(num_hilos)]
	
	for pos, i in enumerate(range(num_hilos)):
		d = Download(*L[i])
		d.start()
		hilos.append(d)

	for h in hilos:
		h.join()


	
