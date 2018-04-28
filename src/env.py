import os

class Env():
	def __init__(self, filepath):
		self.variables = {}
		self.filepath = filepath
		self.read()

	def read(self):
		with open(self.filepath) as f:
			for line in f.readlines():
				key,value = line.split('=')
				self.variables[key] = value.strip('\n')

	def get(self, key, default=None):
		if key in self.variables:
			return self.variables[key]
		return default

	def set(self, key, value):
		self.variables[key] = value
		self.save()

	def save(self):
		with open(self.filepath, 'w') as f:
			for key in self.variables:
				f.write('{}={}\n'.format(key, self.variables[key]))

	def __repr__(self):
		return str(self.variables)
