import requests
from bs4 import BeautifulSoup

class gachaPaidPlayer():
	def __init__(self, codeGacha):
		self.codeGacha = codeGacha
		self.file = 'akun.txt' # name of accounts file
		self.Username = []
		self.Password = []
		with open(self.file) as f:
			alist = [line.rstrip() for line in f]
			totalAkun = str(len(alist)) # get total accounts
			for line in alist:
				line = line[23:57]
				line = line.split(" ")
				self.Username.append(line[1]) # push into array 
				self.Password.append(line[2]) # push into array

	def login(self):
		# initiate headers
		headers = {
		'User-Agent': "Mozilla/5.0 (Linux; Android 7.0; PLUS Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36"
		}

		# Create Requests
		r = requests.session()
		r.headers = headers

		# GET CSRF TOKEN
		URL = "https://dauth.user.ameba.jp/login/ameba"
		req = r.get(URL)
		soup = BeautifulSoup(req.text, 'html.parser')
		csrf_token = soup.find("input", {"name": "csrf_token"}).get("value")

		# Login Process
		URL = "https://dauth.user.ameba.jp/accounts/login"
		for u, p in zip(self.Username, self.Password):
			payload = {
			'accountId':u,
			'csrf_token':csrf_token,
			'password':p
			}
			try:
				req = r.post(URL, data=payload)
				print("Logging in...")
			except Exception as e:
				print("Login failed...")
				print(str("reason is {0}".format(e)))
			
			# Get Pigg ID
			URL = "https://pigg.ameba.jp/"
			req =r.get(URL)
			roomID = req.url.split("/")[-1]

			# Get Nick Name
			URL = "https://spsns-api.pigg.ameba.jp/api/room/owner/" + roomID + "/json?accessType=2"
			req = r.get(URL).json()
			Nickname = req['datas']['nickName']
			print("\nLogin Success !\n")
			print("Nickname : {0}".format(Nickname))



gachaPaidPlayer(None).login()
