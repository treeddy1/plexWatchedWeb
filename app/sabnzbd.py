import urllib2
import json

class Sabnzbd(object):
	def __init__(self, host="127.0.0.1:8080", apiKey="0"):
		self.host = host
		self.apiKey = apiKey


	def _send_to_sabnzbd(self, command):
		"""Handles communication to Sabnzbd servers via API
		Args:
		    command: API Command to Sabnzbd
	
		Returns:
		    Returns response.result for successful commands or False if there was an error
		"""  
		url = 'http://%s/api?%s&apikey=%s' % (self.host, command, self.apiKey)
		try:
			req = urllib2.Request(url)     
			response = urllib2.urlopen(req)
			# parse the json result
			result = json.load(response)
			response.close()
			if 'status' in result:
				print "Sabnzbd: " + result['error']
				return False
			return result # need to return response for parsing

		except (urllib2.URLError, IOError), e:
			print "Warning: Couldn't contact Sabnzbd at " + url 
			return False

	def version(self):
		command="mode=version&output=json"
		output = self._send_to_sabnzbd(command)
		if output:
			print "Version: " + output['version']
			return True
		else:
			return output

	def get_warnings(self):
		command ="mode=warnings&output=json"
		output = self._send_to_sabnzbd(command)
		if output:
			#print output
			for item in output['warnings']:
				if "ERROR" in item:
					print item
			return output
		else:
			return output

	def queue_status(self):
		command = "mode=qstatus&output=json"
		output = self._send_to_sabnzbd(command)
		if output:
			if output['noofslots'] == 0:
				print "Nothing being downloaded"
				return True
			else:
				print "Stuff being downloaded: %i Active Downloads" % (output['noofslots'])
				return True
		else:
			return False


	def get_history(self,limit=10):
		command = "mode=history&start=START&limit=%s&output=json" % (limit)
		output = self._send_to_sabnzbd(command)
		if output:
			return output['history']['slots']
		else:
			return False

	def get_history_fail(self, limit=10):
		failed_history = []
		history = self.get_history(limit)
		if history:
			for item in history:
				if item['fail_message'] != "":
					failed_history.append(item)

		return failed_history





