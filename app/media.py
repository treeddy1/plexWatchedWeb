
class Show(object):
	def __init__(self, name, showKey):
		self.name = name
		self.showKey = showKey
		self.seasons = []
		self.episodes = []
		self.id = 0

class Episode(object):
	def __init__(self):
		self.name = ""
		self.summary = ""
		self.key = ""
		self.season = 0
		self.episodeNumber = 0
		self.airDate = ""
		self.filePath = ""
		self.watched = False
		self.showKey = ""
		self.id = 0
		self.duration = 0
		self.viewOffset = 0

class Movie(object):
	def __init__(self, movie):
		self.name = movie.getAttribute('title')
		self.summary = movie.getAttribute('summary')
		self.key = movie.getAttribute('key')
		self.filePath = movie.childNodes[1].childNodes[1].getAttribute('file')
		self.id = movie.getAttribute('ratingKey')
		self.thumb = movie.getAttribute('thumb') 
		self.art = movie.getAttribute('art')
		self.watched = self._is_watched(movie)
		self.duration = movie.getAttribute('duration')
		self.viewOffset = self._set_duration(movie)

	def _is_watched(self, movie):
		if movie.getAttribute('viewCount'):
			return True
		else:
			return False

	def _set_duration(self, movie):
		if movie.getAttribute('viewOffset'):
			return movie.getAttribute('viewOffset')
		elif self.watched:
			return self.duration
		else:
			return 0