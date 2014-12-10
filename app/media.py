
class Show(object):

	def __init__(self, show):

		self.name = show.getAttribute('title')
		self.showKey = show.getAttribute('key')
		self.id = show.getAttribute('ratingKey')
		self.seasons = []
		self.episodes = []



class MediaType(object):

	def __init__(self, media):

		self.name = media.getAttribute('title')
		self.summary = media.getAttribute('summary')
		self.key = media.getAttribute('key')
		self.filePath = media.childNodes[1].childNodes[1].getAttribute('file')
		self.id = media.getAttribute('ratingKey')
		self.showKey = media.getAttribute('grandparentRatingKey')
		self.watched = self._is_watched(media)
		self.duration = media.getAttribute('duration')
		self.viewOffset = self._set_viewOffset(media)


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

	def __init__(self, episode, showName, seasonNumber):
		
		MediaType.__init__(self, episode)
		self.showName = showName
		self.season = seasonNumber
		self.episodeNumber = episode.getAttribute('index')
		self.airDate = episode.getAttribute('originallyAvailableAt')


class Movie(MediaType):

	def __init__(self, movie):
		
		MediaType.__init__(self, movie)
		self.thumb = movie.getAttribute('thumb') 
		self.art = movie.getAttribute('art')
