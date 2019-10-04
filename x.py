import requests, sys
from bs4 import BeautifulSoup
codeGacha = "smartphone_" + input(str("Code Gacha : "))
fileName = "akun.txt"
# Get List Account

with open(fileName) as f:
	alist = [line.rstrip() for line in f]
	totalAkun = str(len(alist))
	print('Total Accounts : ' + totalAkun)
	for line in alist:
		line = line[23:60]
		line = line.split(" ")
		Username = line[1]
		Password = line[2]

		print("ID : " + Username)
		print("PW : " + Password)

		# Create Headers
		headers = {
		'User-Agent': "Mozilla/5.0 (Linux; Android 7.0; PLUS Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36"
		}

		r = requests.session()
		r.headers = headers
		print("Gacha Custom Spinner")

		# Get CSRF
		URL = "https://dauth.user.ameba.jp/login/ameba"
		try:
			req = r.get(URL)
			print("\nGetting CSRF...")
		except Exception as e:
			print(str(e))
		soup = BeautifulSoup(req.text, 'html.parser')
		csrf_token = soup.find("input", {"name": "csrf_token"}).get("value")

		# Try Login
		URL = "https://dauth.user.ameba.jp/accounts/login"
		payload = {
		'accountId':Username,
		'csrf_token':csrf_token,
		'password':Password
		}
		print("\nLogin...")
		try:
			req = r.post(URL, data=payload)
		except Exception as e:
			print("\nLogin Failed")
			print(str(e))
		# Get Pigg ID
		print("\nLogin Success\n")
		URL = "https://pigg.ameba.jp/"
		try:
			req = r.get(URL)
			roomID = req.url.split("/")[-1]
		except Exception as e:
			print(str(e))
			
		# Gacha 
		URL = 'https://s.pigg.ameba.jp/gacha/detail?code=' + str(codeGacha)
		print("Checking Gacha...")
		try:
			req = r.get(URL).json()
			token = req['token']
		except Exception as e:
			print(str(e))

		URL = "https://s.pigg.ameba.jp/gacha/coin/purchase?code=" + codeGacha + "&free=false&token=" + token
		try:
			print("\nSpinning the Gacha\n")
			req = r.get(URL).json()
		except requests.exceptions.RequestsException as e:
			print("Req Error : " + str (e))
			continue
		token = req['newToken']
		try:
			item = str(req['drawItem']['code'])
			gachaRarity = str(req['drawItem']['rarity'])
			if gachaRarity == '1':
				gachaRarity = "Rare"
			elif gachaRarity == '2':
				gachaRarity = "Super Rare"
			else:
				gachaRarity = "Normal"

			print("HIT {0} ! {1}\n".format(gachaRarity, item))
		except Exception as e:
			print("\nGacha Already Played or Not enough coins\n")
			continue

		# Write Output
		if gachaRarity == "Rare":
			with open('langka.csv', 'a+') as r:
				r.write(Username + "," + item + "," + gachaRarity +  '\n')
		elif gachaRarity == "Super Rare":
			with open('langka.csv', 'a+') as r:
				r.write(Username + "," + item + "," + gachaRarity +  '\n')
			sys.exit(0)
		else:
			with open('hasil.csv', 'a+') as r:
				r.write(Username + "," + item + "," + gachaRarity +  '\n')

		


