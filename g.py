import requests
from bs4 import BeautifulSoup

class gachaPaidPlayer():

	def __init__(self, codeGacha):
		self.codeGacha = codeGacha
		self.file = 'akun.txt'
		self.Username = []
		self.Password = []
		with open(self.file) as f:
			alist = [line.rstrip() for line in f]
			totalAkun = str(len(alist))
			for line in alist:
				line = line[23:57]
				line = line.split(" ")
				self.Username.append(line[1]) 
				self.Password.append(line[2]) 

	def call(self):
		for u in self.Username:
			print(u)

gachaPaidPlayer(None).call()
