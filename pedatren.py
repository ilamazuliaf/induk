import requests, json, base64, sys
from requests.auth import HTTPBasicAuth
from app import logger

class Login():

	__url = 'https://api.pedatren.nuruljadid.app/'
	# __url = 'http://207.148.75.98:3000/api/v1/'
	def __init__(self):
		try:
			open("token.txt", "r")
		except IOError:
			open("token.txt", "w")
		with open('token.txt', 'r') as f:
			token = f.read()
		self.__token = token
		self.__url = Login.__url

	@property
	def headers(self):
		header = {
			'content-type' : 'application/json',
			'connection' : 'keep-alive',
			# 'User-Agent' : conf['agent'],
			'x-token' : self.__token,
		}
		return header

	@property
	def url(self):
		return self.__url

	def login(self):
		data = requests.get(self.url+'auth/login', auth=('username','password'), headers=self.headers)
		if data.status_code == 200:
			self.__token = data.headers['x-token']
			with open('token.txt', 'w') as f:
				f.write(self.__token)

	def cekLogin(self):
		data = requests.get(self.url+'auth/login', headers = self.headers)
		return data.status_code

	@property
	def token(self):
		if self.cekLogin() != 200:
			self.login()
		return self.__token

	def level(self):
		user = self.token.split(".")[0]
		user += "=" * ((4 - len(user) % 4) % 4)
		level = json.loads(base64.b64decode(user))['scope'][1]
		return level

	@property
	def urlUser(self):
		lev = self.level()
		if 'lembaga' in lev:
			urlUser = "{}{}/".format(self.url, lev.replace('-','/'))
		else:
			print ("Mohon Maaf hanya untuk aku Lembaga")
			sys.exit(0)
		return urlUser

class Pedatren(Login):

	def person(self, uuid):
		with requests.get(self.url+'person/{}'.format(uuid), headers = self.headers) as f:
			return json.loads(f.content)

	def updateInduk(self, uuid, induk, id_lembaga, id_pendidikan, tanggal_masuk):
		payloads = {
			"nomor_induk": induk,
			"id_lembaga": id_lembaga,
			"tanggal_mulai": tanggal_masuk,
		}
		try:
			updateSiswa = requests.put(
				self.url+'person/{}/pendidikan/{}'.format(uuid,id_pendidikan),
				data=json.dumps(payloads), headers= self.headers,
				)
			return updateSiswa.status_code
		except Exception as e:
			logger.exception(e)

	def all_pelajar(self):#, kelas=None, jurusan=None, jenis_kelamin=None):
		# try:
		params = {
			'page' : '1',
			'limit' : '1000',
		}
		f = requests.get(self.urlUser+'pelajar', headers=self.headers, params=params)
		total = f.headers['x-pagination-total-page']
		json_file = []
		for r in range(1,int(total)+1):
			params['page'] = str(r)
			f = requests.get(self.urlUser+'pelajar', headers=self.headers, params=params)
			to_json = json.loads(f.content)
			json_file.append(to_json)
		json_file = [j for i in json_file for j in i]
		return json_file

def cetakExcel(data):
	from openpyxl import Workbook
	wb = Workbook(write_only=True)
	ws = wb.create_sheet()
	sheet = wb.active
	for i in data:
		sheet.append(i)
	wb.save("data_siswa.xlsx")
