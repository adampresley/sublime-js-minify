#
# History:
# 		2/13/2012:
# 			- Fixed issue with running on a file with a UNC path in Windows. Now uses the
# 			  user's home directory as the current working directory.
#
import sublime, sublime_plugin
import re, os, subprocess
import time, json

from subprocess import Popen

targetView = None
targetCode = None
PLUGIN_DIRECTORY = os.getcwd()

def replaceWithNewCode(view):
	global targetCode

	r = sublime.Region(0, view.size())

	ed = view.begin_edit()
	view.erase(ed, r)
	s = view.insert(ed, 0, targetCode)
	view.end_edit(ed)


class LoadListener(sublime_plugin.EventListener):
	def on_load(self, view):
		global targetView

		if view.file_name() == targetView:
			replaceWithNewCode(view)
			targetView = None


class MinifyjsCommand(sublime_plugin.TextCommand):
	__window = None
	__view = None

	def run(self, edit):
		#
		# Read our settings file
		#
		jsonData = open(os.path.normpath("%s/settings.json" % (PLUGIN_DIRECTORY)))
		settings = json.load(jsonData)
		jsonData.close()


		#
		# Assemble the command to the YUI compressor
		#
		currentBuffer = self.__getCurrentBufferInfo()
		filename = currentBuffer["fileName"]
		processCommand = self.__getCommand('"' + os.path.normpath("%s/yuicompressor-2.4.7.jar" % (PLUGIN_DIRECTORY)) + '"', settings["args"], filename)


		self.__view = self.view
		self.__window = self.view.window()

		results = []


		#
		# Run it, compress it, capture it.
		#
		p = Popen(processCommand, shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, cwd = os.getenv('USERPROFILE') or os.getenv('HOME'))
		for line in p.stdout.readlines():
			results.append(line)

		ret = p.wait()

		newCode = self.__getNewCode(results)


		#
		# Display the results in a new tab, or alter existing minified file.
		#
		if not self.__findExistingMinifiedMatches(filename, settings["suffixes"], newCode):
			self.__displayResults(newCode)


	def __getCurrentBufferInfo(self):
		return { "id": self.view.buffer_id(), "fileName": self.view.file_name() }


	def __getCommand(self, command, args, filename):
		return "java -jar %s %s \"%s\"" % (command, args, filename)


	def __getNewCode(self, output):
		newCode = "".join(output)
		return newCode


	def __displayResults(self, code):
		tab = self.__window.new_file()
		ed = tab.begin_edit()
		tab.insert(ed, 0, code)
		tab.end_edit(ed)


	def __findExistingMinifiedMatches(self, filename, suffixes, newCode):
		global targetView
		global targetCode

		if filename == None:
			return
			
		if not len(filename):
			return False


		namePart, extension = os.path.splitext(filename)
		found = False
		foundFileName = ""

		tab = None

		#
		# Search for files that match the suffix settings passed in 
		#
		for suffix in suffixes:
			fileToMatch = "%s%s%s" % (namePart, suffix, extension)

			if os.path.isfile(fileToMatch):
				found = True
				foundFileName = fileToMatch
				break

		if found:
			tab = self.__window.open_file(foundFileName)
			targetCode = newCode

			if not tab.is_loading():
				replaceWithNewCode(tab)
			else:
				targetView = tab.file_name()

			return True

		return False