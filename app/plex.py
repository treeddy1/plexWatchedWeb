import urllib
import urllib2
import base64
import sys
import app
from xml.dom import minidom
from optparse import OptionParser
from media import Show, Episode, Movie

class Plex(object):
	def __init__(self, host, username="", password=""):
		self.host = host
		self.showKey = 0
		self.movieKey = 0
		self.token = ""
		self.username = username
		self.password = password
		if username:
			self.authRequired = True
		else:
			self.authRequired = False

		self.get_sections()
		self.movieList = []
		self.showList = []

	def _get_plex_token(self):
		url = "https://my.plexapp.com/users/sign_in.xml"
		try:
			req = urllib2.Request(url, data="")
			base64string = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
			authheader = "Basic %s" % base64string
			req.add_header("Authorization", authheader)
			req.add_header("X-Plex-Client-Identifier","myapp")    

			response = urllib2.urlopen(req)
			result = minidom.parse(response)
			response.close()
			self.token =  result.getElementsByTagName('authentication-token')[0].childNodes[0].data
			return True


		except (urllib2.URLError, IOError), e:
			print "_get_plex_token: Couldn't contact plex service at: " + url 
			print e
			

	def _send_to_plex(self, command):
		url = "http://%s%s" % (self.host, command)
		try:
			req = urllib2.Request(url)
			if self.authRequired:
				if self.token == "":
					self._get_plex_token()
					print self.token
				#logger.log(u"Contacting Plex (with auth header) via url: " + url)     
				req.add_header("X-Plex-Token", self.token)
			response = urllib2.urlopen(req)
			#print response.headers
			if response.headers['content-length'] != "0":
				if response.headers['content-type'] == "text/xml;charset=utf-8":
					result = minidom.parse(response)
				elif response.headers['content-type'] == "image/jpeg":
					result = response.read()
			else:
				result = ""
			response.close()
			return result

		except (urllib2.URLError, IOError), e:
			print "Warning: Couldn't contact Plex at: " + url 
			sys.exit()

	def get_plex_images(self, media):

		thumb = self._send_to_plex(media.thumb)
		fileName = "./app/static/cache/thumb-" + media.id
		output = open( fileName, 'wb+')
		output.write(thumb)
		output.close()

		art = self._send_to_plex(media.art)
		fileName = "./app/static/cache/art-" + media.id
		output = open( fileName, 'wb+')
		output.write(art)
		output.close()


	def get_sections(self):

		sections = self._send_to_plex('/library/sections/').getElementsByTagName('Directory')
		for section in sections:
			if section.getAttribute('type') == "show":
				self.showKey = section.getAttribute('key')
			elif section.getAttribute('type') == "movie":
				self.movieKey = section.getAttribute('key')


	def get_shows(self):
		showList = []
		mycommand = "/library/sections/%s/all" % (self.showKey)
		shows = self._send_to_plex(mycommand).getElementsByTagName('Directory')
		for show in shows:
			newShow = Show(show)
			newShow.seasons = self.get_show_seasons(show.getAttribute('key'))

			for season in newShow.seasons:
				newShow.episodes = self.get_episode_list(season)

			self.showList.append(newShow)

		return True

	def get_show_seasons(self, showKey):
		seasons = self._send_to_plex(showKey).getElementsByTagName('Directory')
		return seasons
		

	def get_episode_list(self, season):
		seasonNumber = season.getAttribute('index')
		seasonPath = season.getAttribute('key')
		episodeList = []
		episodes = self._send_to_plex(seasonPath).getElementsByTagName('Video')

		for episode in episodes:
			episodeNew = Episode(episode, seasonNumber)
			episodeList.append(episodeNew)

		return episodeList


	def get_movies(self):
		movieList = []
		mycommand = "/library/sections/%s/all" % (self.movieKey)
		movies = self._send_to_plex(mycommand).getElementsByTagName('Video')
		for movie in movies:
			newMovie = Movie(movie)
			self.get_plex_images(newMovie)
			self.movieList.append(newMovie)

		return True

	def refesh_library(self):
		sections = []
		sections.append(self.showKey)
		sections.append(self.movieKey)
		for section in sections:
			mycommand = "/library/sections/%s/refresh" % (section)
			self._send_to_plex(mycommand)

	def clear_cache(self):
		cache_path = app.static_folder + "/cache"
		#not done		


