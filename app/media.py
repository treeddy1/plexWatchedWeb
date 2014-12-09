
class Show(object):
	def __init__(self, show):
		self.name = show.getAttribute('title')
		self.showKey = show.getAttribute('key')
		self.id = show.getAttribute('ratingKey')
		self.seasons = []
		self.episodes = []



class MediaType(object):
	def _is_watched(self, media):
		if media.getAttribute('viewCount'):
			return True
		else:
			return False
	
	def _set_viewOffset(self, media):
		if media.getAttribute('viewOffset'):
			return media.getAttribute('viewOffset')
		elif self.watched:
			return self.duration
		else:
			return 0


class Episode(MediaType):
	def __init__(self, episode, season):
		self.name = episode.getAttribute('title')
		self.summary = episode.getAttribute('summary')
		self.key = episode.getAttribute('key')
		self.season = season.getAttribute('index')
		self.episodeNumber = episode.getAttribute('index')
		self.airDate = episode.getAttribute('originallyAvailableAt')			
		self.filePath = episode.childNodes[1].childNodes[1].getAttribute('file')
		self.id = episode.getAttribute('ratingKey')
		self.showKey = episode.getAttribute('grandparentRatingKey')
		self.watched = self._is_watched(episode)
		self.duration = episode.getAttribute('duration')
		self.viewOffset = self._set_viewOffset(episode)


class Movie(MediaType):
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
		self.viewOffset = self._set_viewOffset(movie)

