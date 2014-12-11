

class LogReader(object):

	def __init__(self, log_file):
		self.log_file = log_file
		self.log_levels = dict([
			('DEBUG', 1),
			('INFO', 2),
			('WARNING', 3),
			('ERROR', 4)
		])


	def reverse_level(self, log_level):
		return self.log_levels[log_level]


	def log_level_filter(self, line, min_log_level):
		tmp_line = line.split(' ')
		line_log_level = tmp_line[3]
		line_log_level_num = self.reverse_level(line_log_level)

		if line_log_level_num >= self.reverse_level(min_log_level):
			return line


	def read_log(self, min_log_level="INFO"):
		with open(self.log_file, 'r') as log_file:
			log_file_lines = log_file.readlines()

		log_lines = []

		for line in log_file_lines:
			if self.log_level_filter(line, min_log_level):
				log_lines.append(line)

		return log_lines


