from app import db


class Server(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	label = db.Column(db.String(80), unique=True)
	host = db.Column(db.String(80))
	username = db.Column(db.String(80))
	password = db.Column(db.String(80))

	def __init__(self, label, host, username, password):
		self.label = label
		self.host = host
		self.username = username
		self.password = password


class Show(object):

	def __init__(self, show):

		self.name = show.getAttribute('title')
		self.showKey = show.getAttribute('key')
		#self.id = show.getAttribute('ratingKey')
		self.seasons = []
		
"""
class MediaType(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	summary = db.Column(db.String(250))
	key = db.Column(db.String(250))
	filePath = db.Column(db.String(250))
	showKey = db.Column(db.String(250))
	watched = db.Column(db.Boolean())
	duration = db.Column(db.Integer())
	viewOffset = db.Column(db.Integer())
	type = db.Column(db.String(50))

	__mapper_args__ = {
        'polymorphic_identity':'mediatype',
        'polymorphic_on':type
    }

	def __init__(self, media):

		self.name = media.getAttribute('title')
		self.summary = media.getAttribute('summary')
		self.key = media.getAttribute('key')
		self.filePath = media.childNodes[1].childNodes[1].getAttribute('file')
		#self.id = media.getAttribute('ratingKey')
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

"""
class Episode(db.Model):
	#id = db.Column(db.Integer, db.ForeignKey('mediatype.id'), primary_key=True)
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	summary = db.Column(db.String(250))
	key = db.Column(db.String(250))
	filePath = db.Column(db.String(250))
	showKey = db.Column(db.String(250))
	watched = db.Column(db.Boolean())
	duration = db.Column(db.Integer())
	viewOffset = db.Column(db.Integer())
	showName = db.Column(db.String(250))
	season = db.Column(db.String(10))
	episodeNumber = db.Column(db.String(10))
	airDate = db.Column(db.String(250))
	"""
	__mapper_args__ = {
        'polymorphic_identity':'episode',
    }
    """
	def __init__(self, episode, showName, seasonNumber):
		self.name = episode.getAttribute('title')
		self.summary = episode.getAttribute('summary')
		self.key = episode.getAttribute('key')
		self.filePath = episode.childNodes[1].childNodes[1].getAttribute('file')
		#self.id = media.getAttribute('ratingKey')
		self.showKey = episode.getAttribute('grandparentRatingKey')
		self.watched = self._is_watched(episode)
		self.duration = episode.getAttribute('duration')
		self.viewOffset = self._set_viewOffset(episode)
		#MediaType.__init__(self, episode)
		self.showName = showName
		self.season = seasonNumber
		self.episodeNumber = episode.getAttribute('index')
		self.airDate = episode.getAttribute('originallyAvailableAt')

	def _is_watched(self, episode):

		if episode.getAttribute('viewCount'):
			return True
		else:
			return False
	
	def _set_viewOffset(self, episode):

		if episode.getAttribute('viewOffset'):
			return episode.getAttribute('viewOffset')
		elif self.watched:
			return self.duration
		else:
			return 0



class Movie(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	summary = db.Column(db.String(250))
	key = db.Column(db.String(250))
	filePath = db.Column(db.String(250))
	showKey = db.Column(db.String(250))
	watched = db.Column(db.Boolean())
	duration = db.Column(db.Integer())
	viewOffset = db.Column(db.Integer())
	#id = db.Column(db.Integer, db.ForeignKey('mediatype.id'), primary_key=True)
	thumb = db.Column(db.String(250))
	art = db.Column(db.String(250))
	"""
	__mapper_args__ = {
        'polymorphic_identity':'episode',
    }
    """
	def __init__(self, movie):
		self.name = movie.getAttribute('title')
		self.summary = movie.getAttribute('summary')
		self.key = movie.getAttribute('key')
		self.filePath = movie.childNodes[1].childNodes[1].getAttribute('file')
		#self.id = movie.getAttribute('ratingKey')
		self.showKey = movie.getAttribute('grandparentRatingKey')
		self.watched = self._is_watched(movie)
		self.duration = movie.getAttribute('duration')
		self.viewOffset = self._set_viewOffset(movie)
		#MediaType.__init__(self, movie)
		self.thumb = movie.getAttribute('thumb') 
		self.art = movie.getAttribute('art')

	def _is_watched(self, movie):
		if movie.getAttribute('viewCount'):
			return True
		else:
			return False
	
	def _set_viewOffset(self, movie):
		if movie.getAttribute('viewOffset'):
			return movie.getAttribute('viewOffset')
		elif self.watched:
			return self.duration
		else:
			return 0
