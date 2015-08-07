# Changelog for SearchInProject

## v1.7.0 2015-08-07

* Support The Platinum Searcher (thanks to @jodaka)
* Added links to configuration files to the command palette, and a post-install message.

## v1.6.2 2015-07-29

* Fix for missing result in results view (thanks to @dtaub)
* Show line and file count in results view

## v1.6.1 2015-07-21

* Avoid showing console window on Windows platform (thanks to @kojoru)

## v1.6.0 2015-07-21

* List results in view

## v1.5.1 2015-03-18

* Fix ack detection code for Sublime Text 2, by @keimlink
* Show empty results message in a messagebox instead of the results window

## v1.5.0 2015-01-21 "The Tested Release"

* No more using bash to locate executables.
* Actually, no more using shell when invoking search engine at all! This leads to a huge performance boost on typical systems.
* The search string is now passed as a single argument to the engine. This means you no longer have to quote special characters.
* Fix The Silver Searcher empty results incorrectly reporting as an error message.
* Show error messages in a nice error box instead of the list view.
* Do not run search with empty query.
* Do not use selection text as preset query if it is multi-line.
* Tested for full compatibility with OSX and Linux. Unfortunately, Windows compatibility will have to wait for the next release.
* Multiple compatibility fixes for ag, ack, git-grep.

## v1.4.1 2014-06-30

* Fix for erros when search engine output contains binary or non-UTF text

## v1.4.0 2014-06-10

* Use bash to locate executables; should work out-of-the-box on the majority of systems
* Verbose error message when the search engine fails to execute for any reason

## v1.3.0 2013-11-11

* Further fixes for Sublime Text 3

## v1.2.0 2013-04-21

* Works with Sublime Text 3 (thanks to @basteln, and also at his word)
* Correctly handles quoted  paths with The Silver Searcher (#3, also thanks to @basteln)

## v1.1.0 2012-12-01

* Fixed: The Silver Searcher not providing line numbers
* Fixed: "No Results" message was never displayed
* Fixed: column information was never correctly parsed and used
* Added: highlighting of search results in files that are opened

## v1.0.0 2012-10-10

* Initial release
