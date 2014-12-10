from flask import render_template, request, redirect, url_for, flash
from app import app, MYPLEX, MYSICKBEARD, MYSABNZBD
import os, time, shutil

@app.route('/')
@app.route('/index')
def index(type = ""):
	sb_fails = MYSICKBEARD.find_not_downloaded()
	sab_fails = MYSABNZBD.get_history_fail()

	return render_template('index.html', shows = MYPLEX.showList, 
		episodes = MYPLEX.episodeList, movies = MYPLEX.movieList)

@app.route('/shows')
@app.route('/shows/<all>')
def shows(all = False):
	shows = MYPLEX.showList
	if all:
		all = True
	return render_template('index.html', shows = MYPLEX.showList, episodes = MYPLEX.episodeList, all = all)


@app.route('/movies')
@app.route('/movies/<all>')
def movies(all = False):
	if all:
		all = True
	return render_template('index.html', movies = MYPLEX.movieList, all = all)

@app.route('/show/<id>')
def show(id):
	myShow = []
	myShow = [show for show in MYPLEX.showList if show.id == id]
	return render_template('show.html', shows = myShow, episodes = MYPLEX.episodeList, all = True)

@app.route('/movie/<id>')
def movie(id):
	myMovie	 = MYPLEX.movieList[id]
	return render_template('movie.html', movie = myMovie)

@app.route('/update')
def update():
	MYPLEX.movieList.clear()
	MYPLEX.showList[:] =[]
	MYPLEX.get_movies()
	MYPLEX.get_shows()
	return redirect(url_for('index'))



@app.route('/delete', methods=['GET', 'POST'])
def delete():
	if request.method == 'POST':
		delete_items = request.values
		for item in delete_items.keys():
			if "episode" in item:
				episode_id = delete_items[item]
				episode = MYPLEX.episodeList[episode_id]
				print "Removing: " + episode.filePath
				if os.path.isfile(episode.filePath):
					os.remove(episode.filePath)
					del MYPLEX.episodeList[episode_id]
					message = "{0}: {1} was deleted!".format(episode.showName, episode.name)
					print message
					flash(message, 'success')
					#app.logger.info("Deleted episode: " + episode.filePath + "from disk")
				else:
					message = "Error: {0} file not found".format(episode.filePath)
					print(message)
					flash(message, 'error')
		
			elif "movie" in item:
				movie_id = delete_items[item]
				movie = MYPLEX.movieList[movie_id]
				if movie.id == delete_items[item]:
					print "Removing: " + movie.name
					try:
						if os.path.isfile(movie.filePath):
							path = os.path.dirname(movie.filePath)
							shutil.rmtree(path, ignore_errors=False)
							MYPLEX.movieList.remove(movie)
							#app.logger.info("Deleted movie: " + movie.filePath + "from disk")
						else:
							message = "Error: %s file not found" % movie.filePath
							print(message)
							flash(message, 'error')
					except:
						pass
				
	MYPLEX.refesh_library()
	return redirect(url_for('index'))


@app.route('/sickbeard')
@app.route('/sickbeard/<item_limit>')
def sickbeard(item_limit=20):

	sb_fails = MYSICKBEARD.find_not_downloaded(item_limit)
	return render_template('sickbeard.html', sb_fails=sb_fails)

@app.route('/sabnzbd')
@app.route('/sabnzbd/<item_limit>')
def sabnzbd(item_limit=20):
	sab_fails = MYSABNZBD.get_history_fail(item_limit)
	return render_template('sabnzbd.html', sab_fails=sab_fails)


@app.route('/config', methods=['GET', 'POST'])
def config():
	if request.method == 'POST':
		for item in request.values:
				print item + " : " + request.values[item]

	return render_template('config.html', config=app.config)




