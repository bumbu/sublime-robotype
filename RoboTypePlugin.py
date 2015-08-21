import sublime, sublime_plugin, random, time

class RoboTypeCommand(sublime_plugin.TextCommand):

	# A basic map of the keyboard.
	keys = [
		['q','w','e','r','t','y','u','i','o','p','[',']'],
		['a','s','d','f','g','h','j','k','l',';','\''],
		['z','x','c','v','b','n','m',',','.','/']
	]

	# The fastest possible keystroke, in milliseconds
	intervalLow = 10

	# The slowest possible keystroke, in milliseconds
	intervalHigh = 100

	# The delay, in milliseconds for each keystroke. Continually augmented.
	timeout = None

	# The index of the cliboard text
	stringIndex = 0

	def run(self, edit):
		# Get text from clipboard
		self.text_to_print = sublime.get_clipboard()

		# Override from settings
		self.intervalLow = self.view.settings().get('robotype_keystroke_interval_low')
		self.intervalHigh = self.view.settings().get('robotype_keystroke_interval_high')

		# Establish an initial timout
		self.timeout = self.getInterval()

		# Loop through the string
		while self.stringIndex < len(self.text_to_print):
			nextChar = self.text_to_print[self.stringIndex]
			keystroke = self.generateKeystroke(nextChar)

			self.renderChar(keystroke)
			self.stringIndex += 1

		self.reset()

	# Queues the rendering of a character
	def renderChar(self, char):
		self.queueAction(lambda char=char: self.view.run_command('robo_type_add_char', {"args" : { 'char': char }}))

	# Backspaces to a position in the string
	def backspaceTo(self, index):
		while self.stringIndex > index:
			self.queueAction(lambda: self.view.run_command('robo_type_delete_char'))
			self.stringIndex -= 1

	# Schedule an action, using the incrementing timeout
	def queueAction(self, func):
		self.timeout += self.getInterval()
		sublime.set_timeout(func, self.timeout)

	# Gets a random keystroke speed, using the low/high threshold from the settings
	def getInterval(self):
		return random.randrange(self.intervalLow, self.intervalHigh+1)

	# Given a character, render it
	def generateKeystroke(self, char):
		return char

	def reset(self):
		self.stringIndex = 0


# Adds a character to the screen
class RoboTypeAddCharCommand(sublime_plugin.TextCommand):

	def run(self, edit, args):
		self.view.insert(edit, self.view.sel()[0].begin(), args['char'])


# Deletes the previous character from the screen
class RoboTypeDeleteCharCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		point = self.view.sel()[0].begin()
		region = sublime.Region(point-1, point)
		self.view.erase(edit, region)

