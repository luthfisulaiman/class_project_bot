from bs4 import BeautifulSoup as bs
import requests, urllib


class Movie_Cinema:

	def __init__(self):
		self.BASE_URL = "https://www.cgv.id/en/schedule/cinema/0200"
		self.cinema_id = self.BASE_URL[-4:]

	def get_base(self):
		return self.BASE_URL

	def get_cinema_id(self):
		return self.cinema_id

	def set_base(self, new_url):
		self.BASE_URL = new_url
	
	def find_gold(self):
		req = requests.get(self.BASE_URL).text
		try:
			soup = bs(req, "html.parser")
			result = temp_result = ""

			cinema = soup.find_all(id=self.cinema_id)
			for s_c in cinema:
				result += 'Cinema: CGV Blitz ' + s_c.text + '\n'*2

			sched = soup.find_all(class_='schedule-type')
			for stype in sched:
				if 'gold class' in stype.text.lower():
					temp_showtime = stype.findNext('ul').text.split('\n')
					movie = stype.findNext('a')['movietitle']
					temp_result = "('{}', {})".format(movie, temp_showtime[1:-1])
					result += temp_result + "\n"

			if len(temp_result) == 0:
				return "There is no schedule"
			else:
				return result
		except:
			return 'error retrieving'

	def find_reg2d(self):
		req = requests.get(self.BASE_URL).text
		try:
			soup = bs(req, "html.parser")
			result = temp_result = ""

			cinema = soup.find_all(id=self.cinema_id)
			for s_c in cinema:
				result += 'Cinema: CGV Blitz ' + s_c.text + '\n'*2

			sched = soup.find_all(class_='schedule-type')
			for stype in sched:
				if 'regular 2d' in stype.text.lower():
					temp_showtime = stype.findNext('ul').text.split('\n')
					movie = stype.findNext('a')['movietitle']
					temp_result = "('{}', {})".format(movie, temp_showtime[1:-1])
					result += temp_result + "\n"

			if len(temp_result) == 0:
				return "There is no schedule"
			else:
				return result
		except ConnectionError:
			return 'error retrieving'

	def find_3d(self):
		req = requests.get(self.BASE_URL).text
		try:
			soup = bs(req, "html.parser")
			result = temp_result = ""

			cinema = soup.find_all(id=self.cinema_id)
			for s_c in cinema:
				result += 'Cinema: CGV Blitz ' + s_c.text + '\n'*2

			sched = soup.find_all(class_='schedule-type')
			for stype in sched:
				if '4dx 2d cinema' in stype.text.lower():
					temp_showtime = stype.findNext('ul').text.split('\n')
					movie = stype.findNext('a')['movietitle']
					temp_result = "('{}', {})".format(movie, temp_showtime[1:-1])
					result += temp_result + "\n"

			if len(temp_result) == 0:
				return "There is no schedule"
			else:
				return result
		except:
			return 'error retrieving'

	def find_velvet(self):
		req = requests.get(self.BASE_URL).text
		try:
			soup = bs(req, "html.parser")
			result = temp_result = ""

			cinema = soup.find_all(id=self.cinema_id)
			for s_c in cinema:
				result += 'Cinema: CGV Blitz ' + s_c.text + '\n'*2

			sched = soup.find_all(class_='schedule-type')
			for stype in sched:
				if 'velvet class' in stype.text.lower():
					temp_showtime = stype.findNext('ul').text.split('\n')
					movie = stype.findNext('a')['movietitle']
					temp_result = "('{}', {})".format(movie, temp_showtime[1:-1])
					result += temp_result + "\n"

			if len(temp_result) == 0:
				return "There is no schedule"
			else:
				return result
		except:
			return 'error retrieving'

	def find_sweetbox(self):
		req = requests.get(self.BASE_URL).text
		try:
			soup = bs(req, "html.parser")
			result = temp_result = ""

			cinema = soup.find_all(id=self.cinema_id)
			for s_c in cinema:
				result += 'Cinema: CGV Blitz ' + s_c.text + '\n'*2

			sched = soup.find_all(class_='schedule-type')
			for stype in sched:
				if 'sweet box' in stype.text.lower():
					temp_showtime = stype.findNext('ul').text.split('\n')
					movie = stype.findNext('a')['movietitle']
					temp_result = "('{}', {})".format(movie, temp_showtime[1:-1])
					result += temp_result + "\n"

			if len(temp_result) == 0:
				return "There is no schedule"
			else:
				return result
		except:
			return 'error retrieving'


	def change_cinema(self, nurl):
		req = requests.get(self.BASE_URL)
		base = "/schedule/cinema/"

		try:
			soup = bs(req.text, "html.parser")
			sched = soup.find_all(class_='schedule-type')

			result = ""
			cinema = soup.find_all(id=self.cinema_id)

			if not base in nurl or req.status_code == '404':
				return "invalid url"
			elif len(sched) == 0 or sched == None:
				return "cinema does not exist"
			else:
				self.set_base(nurl)
				result += "Cinema has changed successfully"
				return result
		except:
			return 'error retrieving'
