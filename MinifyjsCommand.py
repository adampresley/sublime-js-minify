#
# History:
#
# 		5/23/2012: 
# 			- Plugin now looks in the current directory for yuicompressor.jar
# 			- All options are stored in central settings.json file instead of each
# 			  keymap and menu file.
#
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
code_charset = None
open_tab_when_saved = None
PLUGIN_DIRECTORY = os.getcwd()

def replaceWithNewCode(view):
	global targetCode
	global code_charset

	r = sublime.Region(0, view.size())

	ed = view.begin_edit()
	view.erase(ed, r)
	if code_charset:
		code = targetCode.decode(code_charset)
	else:
		code = targetCode
	s = view.insert(ed, 0, code)
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
		global open_tab_when_saved
		open_tab_when_saved = settings["open_tab_when_saved"]



		#
		# Assemble the command to the YUI compressor
		#
		currentBuffer = self.__getCurrentBufferInfo()
		filename = currentBuffer["fileName"]

		charset_priority = settings["charset_priority"]

		strCode = open(filename, "r").read()

		global code_charset

		for charset in charset_priority:
			try:
				code_charset = charset
				strCode.decode(charset)
			except Exception, e:
				code_charset = False
			else:
				break
			finally:
				pass
		
		print "charset: ", code_charset

		arg_charset = ""
		if code_charset:
			arg_charset = " --charset %s" % code_charset

		processCommand = self.__getCommand('"' + os.path.normpath("%s/yuicompressor-2.4.7.jar" % (PLUGIN_DIRECTORY)) + '"', settings["args"] + arg_charset, filename)


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
		if not self.__findExistingMinifiedMatches(filename, settings["suffixes"], newCode, settings["default_suffix"]):
			self.__displayResults(newCode)

		print "%s successful compressed." % filename


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

		if code_charset:
			code = code.decode(code_charset)
		else:
			code = code

		tab.insert(ed, 0, code)
		tab.end_edit(ed)


	def __findExistingMinifiedMatches(self, filename, suffixes, newCode, default_suffix):
		global open_tab_when_saved
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

		if default_suffix:
			if not found:
				found = True
				foundFileName = "%s%s%s" % (namePart, default_suffix, extension)

			fileCode = open( foundFileName, "w" )
			fileCode.write(newCode)
			fileCode.close()
			if not open_tab_when_saved:
				return True

		if found:
			tab = self.__window.open_file(foundFileName)
			targetCode = newCode

			if not tab.is_loading():
				replaceWithNewCode(tab)
			else:
				targetView = tab.file_name()

			return True

		return False