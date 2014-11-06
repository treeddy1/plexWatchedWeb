
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
	def __init__(self):
		self.name = ""
		self.summary = ""
		self.key = ""
		self.filePath = ""
		self.watched = False
		self.id = 0
		self.art = ""
		self.thumb = ""
		self.duration = 0
		self.viewOffset = 0