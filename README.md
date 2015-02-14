# Search In Project

This plugin for [Sublime Text 2 and 3](http://www.sublimetext.com/) lets you use your favorite search tool (`grep`, `ack`, `ag`, `git grep`, or `findstr`) to find strings aross your entire current Sublime Text project.

It opens a quick selection panel to browse results, and highlights matches inside files.

It's easy to add another search tool, if you so desire.

**Important note for Windows users: the current release has known issues with running executables, I'd appreciate any bug reports from the field.**

## Installation

* [Package Control](http://sublime.wbond.net): install package **Search in Project** (this is the recommended method)

* Download an [archive of the repository](https://github.com/leonid-shevtsov/SearchInProject_SublimeText/archive/master.zip), and unzip into the Sublime Text Packages folder.

### Installing search engines

My idea is that if you use this plugin it's because you already use one of the superior search engines like [The Silver Searcher](https://github.com/ggreer/the_silver_searcher) and want to use it from within Sublime Text.

## Usage

* Use the key binding (`⌘⌥⇧F` on OS X, `Ctrl+Alt+Shift+F` on Windows), or
* Call the "Search in Project" command;
* Enter the search query;
* Hit `Enter` (`Return`). In a short while you'll be presented with a "quck select" panel with the search results. Select any file from that panel (it supports fuzzy searching) to go to the match. The search string will be highlighted with an outline and a circle symbol in the gutter area.

If you select text and then run Search In Project, it will pre-fill the search string with the selection text; for example, to search for a word project-wide, do `⌘D, ⌘⌥⇧F, ↩`

If you run Search In Project again, it will remember the last search string, so the next search is just an `↩` away.

## Configuration

Configuration is stored in a separate, user-specific `SearchInProject.sublime-settings` file. See the default file for configuration options; links to both could be
found in the main menu in `Preferences -> Package Settings -> Search In Project`.

## Issues with locating executables

If Search In Project has problems with locating executables in Mac, install the [Fix Mac Path plugin](https://github.com/int3h/SublimeFixMacPath).

You can always configure the full path to any search engine in the settings, as a catch-all solution.

* * *

Made by [Leonid Shevtsov](http://leonid.shevtsov.me)
