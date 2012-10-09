# Search In Project

A plugin for [Sublime Text 2](http://www.sublimetext.com/).

## Synopsis

This plugin makes it possible to use various external search tools (`grep`, `ack`, `ag`, `git grep`, or `findstr`) to find strings inside your current Sublime Text project.

It opens a quick selection panel to browse results, and highlights matches inside files.

It's easy to add another search tool, if you so desire.

## Installation

Copy the folder into the Packages folder.

## Usage

Call the "Search in Project" command.

## Configuration

Configuration is stored in a separate, user-specific `SearchInProject.sublime-settings` file. See the default file for configuration options; links to both could be
found in the main menu in `Preferences -> Package Settings -> Search In Project`.

On any OS I recommend you to install [ack](http://betterthangrep.com/), and use it instead of the default `grep`/`findstr`, because it's much faster.

* * *

Made by [Leonid Shevtsov](http://leonid.shevtsov.me)