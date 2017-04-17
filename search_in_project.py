import sublime
import sublime_plugin
import os.path
import os
import sys
import inspect
import re
from collections import defaultdict

### Start of fixing import paths
# realpath() with make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
# use this if you want to include modules from a subforder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "subfolder")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
 # Info:
 # cmd_folder = os.path.dirname(os.path.abspath(__file__)) # DO NOT USE __file__ !!!
 # __file__ fails if script is called in different ways on Windows
 # __file__ fails if someone does os.chdir() before
 # sys.argv[0] also fails because it doesn't not always contains the path
### End of fixing import paths

import searchengines

basedir = os.getcwd()


class SearchInProjectCommand(sublime_plugin.WindowCommand):

    # Used to trim lines for the results quick panel. Without trimming Sublime Text
    # *will* hang on long lines - often encountered in minified Javascript, for example.
    MAX_RESULT_LINE_LENGTH = 1000

    def __init__(self, window):
        sublime_plugin.WindowCommand.__init__(self, window)
        self.last_search_string = [''] 
        pass

    def run(self):
        self.settings = sublime.load_settings('SearchInProject.sublime-settings')
        self.engine_name = self.settings.get("search_in_project_engine")
        pushd = os.getcwd()
        os.chdir(basedir)
        __import__("searchengines.%s" % self.engine_name)
        self.engine = searchengines.__dict__[self.engine_name].engine_class(self.settings)
        os.chdir(pushd)
        view = self.window.active_view()
        selection_text = view.substr(view.sel()[0])
        self.window.show_input_panel(
            "Search in project:",
            not "\n" in selection_text and selection_text,
            self.perform_search, None, None)
        pass

    def perform_search_from_history(self, index):
        if index > -1:
            text = self.last_search_string[index]
            self.perform_search(text)

    def perform_search(self, text):

        if not text:
            # show the list of previous searches
            self.window.show_quick_panel(self.last_search_string, self.perform_search_from_history)
            return

        # add the current search to the list of previous searches
        # self.last_search_string.append(text)
        self.last_search_string = [text] + self.last_search_string
        self.last_search_string = self.makeUnique(self.last_search_string)
        folders = self.search_folders()

        self.common_path = self.find_common_path(folders)

        try:
            self.results = self.engine.run(text, folders)
            self.results = self.makeUnique(self.results);
            if self.results:
                self.results = [
                    [result[0].replace(self.common_path.replace('\"', ''), ''), 
                    result[1][:self.MAX_RESULT_LINE_LENGTH]
                ] for result in self.results]
                self.results.append("``` List results in view ```")
                self.window.show_quick_panel(self.results, self.goto_result)
            else:
                self.results = []
                sublime.message_dialog('No results')
        except Exception as e:
            self.results = []
            sublime.error_message("%s running search engine %s:"%(e.__class__.__name__,self.engine_name) + "\n" + str(e))

    def makeUnique(self,seq): 
        # order preserving
        checked = []
        for e in seq:
           if e not in checked:
               checked.append(e)
        return checked

    def goto_result(self, file_no):
        if file_no != -1:
            if file_no == len(self.results) - 1: # last result is "list in view"
                self.list_in_view()
            else:
                file_name = self.common_path.replace('\"', '') + self.results[file_no][0]
                view = self.window.open_file(file_name, sublime.ENCODED_POSITION)
                regions = view.find_all(self.last_search_string[-1])
                view.add_regions("search_in_project", regions, "entity.name.filename.find-in-files", "circle", sublime.DRAW_OUTLINED)

    def list_in_view(self):
        self.results.pop()
        view = sublime.active_window().new_file()
        view.run_command('search_in_project_results',
            {'query': self.last_search_string[-1],
             'results': self.results,
             'common_path': self.common_path.replace('\"', '')})

    def search_folders(self):
        search_folders = self.window.folders()
        if not search_folders:
            filename = self.window.active_view().file_name()
            if filename:
                search_folders = [os.path.dirname(filename)]
            else:
                search_folders = [os.path.expanduser("~")]
        return search_folders

    def find_common_path(self, paths):
        paths = [path.replace("\"", "") for path in paths]
        paths = [path.split("/") for path in paths]
        common_path = []
        while 0 not in [len(path) for path in paths]:
            next_segment = list(set([path.pop(0) for path in paths]))
            if len(next_segment) == 1:
                common_path += next_segment
            else:
                break
        return "\"" + "/".join(common_path) + "/\""

class SearchInProjectResultsCommand(sublime_plugin.TextCommand):
    def format_result(self, common_path, filename, lines):
        lines_text = "\n".join(["  %s: %s" % (location, text) for location, text in lines])
        return "%s%s\n%s\n" % (common_path, filename, lines_text)

    def format_results(self, common_path, results, query):
        grouped_by_filename = defaultdict(list)
        for result in results:
            filename, location = result[0].split(':', 1)
            text = result[1]
            grouped_by_filename[filename].append((location, text))
        line_count = len(results)
        file_count = len(grouped_by_filename)

        file_results = [self.format_result(common_path, filename, grouped_by_filename[filename]) for filename in grouped_by_filename]
        return ("Search In Project results for \"%s\" (%u lines in %u files):\n\n" % (query, line_count, file_count)) \
            + "\n".join(file_results)

    def run(self, edit, common_path, results, query):
        self.view.set_name('Find Results')
        self.view.set_scratch(True)
        self.view.set_syntax_file('Packages/Default/Find Results.hidden-tmLanguage')
        results_text = self.format_results(common_path, results, query)
        self.view.insert(edit, self.view.text_point(0,0), results_text)
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(0,0))

class FindInFilesGotoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        if view.name() == "Find Results":
            line_no = self.get_line_no()
            file_name = self.get_file()
            if line_no is not None and file_name is not None:
                file_loc = "%s:%s" % (file_name, line_no)
                view.window().open_file(file_loc, sublime.ENCODED_POSITION)
            elif file_name is not None:
                view.window().open_file(file_name)

    def get_line_no(self):
        view = self.view
        if len(view.sel()) == 1:
            line_text = view.substr(view.line(view.sel()[0]))
            match = re.match(r"\s*(\d+):.+", line_text)
            if match:
                return match.group(1)
        return None

    def get_file(self):
        view = self.view
        if len(view.sel()) == 1:
            # get the current line
            line = view.line(view.sel()[0])
            # while we are not at the beginning of the file
            while line.begin() > 0:
                # get the line text
                line_text = view.substr(line)
                match = re.match(r"^(?!.\s.\d).*", line_text)
                if match:
                    if os.path.exists(line_text):
                        return line_text
                line = view.line(line.begin() - 1)
        return None