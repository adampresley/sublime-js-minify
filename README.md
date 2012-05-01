# Sublime JavaScript Minifier

## About
Sublime JavaScript Minifier is a Sublime Text 2 plugin designed to allow
users an easy way to minify a JavaScript file they are working on. It also sports
the ability to try and find an existing minified file and alter it based on a 
configurable list of file name suffixes. For example, when minifying *yourFile.js*
it will look for *youFile.min.js* or *yourFile-min.js*.


## Installation
To "install" this plugin find your User Packages directory for Sublime. In Windows 7
this would be something to the effect of **C:\Users\me\AppData\Roaming\Sublime Text 2\Packages\User**.
For most \*nix distributions that would be **/home/me/.conf/Sublime Text 2/Packages/User**.

Download the project and place the *sublime-js-minify* directory into the above packages directory. 
This will load up the plugin. It also will create menus, context menus, and a key binding. 

This plugin, however, depends on the Yahoo! YUI Compressor, which is provided along with this
repository. Take the *yuicompressor-2.4.7* directory and place it somewhere. Anywhere you
can get to it is fine. Once this is done you will need to alter the following files for
the minification tool to work:

* Main.sublime-menu
* Default (Windows).sublime-keymap
* Default (OSX).sublime-keymap
* Default (Linux).sublime-keymap
* Context.sublime-menu

Note that you don't have to modify every key map file, just the one that applies to the OS
you are using. In each of those files you will see a key labelled **"command"** that has
a path to the **yuicompressor-2.4.7.jar** file. Change the path to this to match where you
placed the *yuicompressor-2.4.7* directory.

Once complete you should be able to open a JavaScript file and execute it one of the 
following ways:

* CTRL + ALT + M
* Right-click -> Adam Presley -> Minify JavaScript
* Tools -> Adam Presley -> Minify JavaScript


## License

Sublime JavaScript Minifier
Copyright (C) 2011 Adam Presley

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

adam [at] adampresley [dot] com