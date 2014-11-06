import urllib2
import json

class SickBeard(object):
	def __init__(self, host="127.0.0.1:8081", apiKey="0"):
		self.host = host
		self.apiKey = apiKey


	def _send_to_sb(self, command):
		"""Handles communication to sickbeard servers via API
		Args:
		    command: API Command to Sickbeard
	
		Returns:
		    Returns response.result for successful commands or False if there was an error
		"""  
		url = 'http://%s/api/%s/?cmd=%s' % (self.host, self.apiKey, command)
		try:
			req = urllib2.Request(url)     
			response = urllib2.urlopen(req)
			
			# parse the json result
			result = json.load(response)
			response.close()
			return result # need to return response for parsing

		except (urllib2.URLError, IOError), e:
			print "Warning: Couldn't contact SickBeard at " + url 
			return False

	def ping(self):
		command = "sb.ping"
		ping = self._send_to_sb(command)
		if ping == False:
			print "Sickbeard is down on Host: " + self.host
			return False
		elif ping['result'] == 'success':
			print "SickBeard is up!"
			return True
		elif ping['result'] == 'denied':
			print "SickBeard Access Denied: Please check SickBeard API key"
			return False

	def get_history(self, limit=2):
		command ='history&limit=%s' % (limit)
		history = self._send_to_sb(command)
		if history:
			return history['data']
		else:
			return False

			"""
			date1 = item['date']
			dateTest = datetime.datetime.strptime(date1, "%Y-%m-%d %H:%M")
			print dateTest.date()
		
			"""

	def find_not_downloaded(self, limit=10):
		snatchedList = []
		not_downloaded = []
		items = self.get_history(limit)
		for item in items:
			if item['status'] == "Snatched":
				snatchedList.append(HistoryItem(item))

		for snatched in snatchedList:
			for item in items:
				if item['status'] == 'Downloaded' and snatched.is_match(item):
					snatched.downloaded = True

		for snatched in snatchedList:
			if not snatched.downloaded:
				not_downloaded.append(snatched)

		return not_downloaded


class HistoryItem(object):

	def __init__(self, item):
		self.date = item['date']
		self.episode = item['episode']
		self.provider = item['provider']
		self.quality = item['quality']
		self.resource = item['resource']
		self.resource_path = item['resource_path']
		self.season = item['season']
		self.show_name = item['show_name']
		self.status = item['status']
		self.tvdbid = item['tvdbid']
		self.downloaded = False

	def is_match(self, item):
		if item['tvdbid'] == self.tvdbid:
			if item['season'] == self.season and item['episode'] == self.episode:
				return True


