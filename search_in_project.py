import sublime
import sublime_plugin
import os.path
import os
import sys
import inspect

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
    def __init__(self, window):
        sublime_plugin.WindowCommand.__init__(self, window)
        self.last_search_string = ''
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
            not "\n" in selection_text and selection_text or self.last_search_string,
            self.perform_search, None, None)
        pass

    def perform_search(self, text):
        if not text:
            return

        self.last_search_string = text
        folders = self.search_folders()

        self.common_path = self.find_common_path(folders)
        try:
            self.results = self.engine.run(text, folders)
            if self.results:
                self.results = [[result[0].replace(self.common_path.replace('\"', ''), ''), result[1]] for result in self.results]
                self.window.show_quick_panel(self.results, self.goto_result)
            else:
                self.results = []
                self.window.show_quick_panel(["No results"], None)
        except Exception as e:
            self.results = []
            sublime.error_message("%s running search engine %s:"%(e.__class__.__name__,self.engine_name) + "\n" + str(e))


    def goto_result(self, file_no):
        if file_no != -1:
            file_name = self.common_path.replace('\"', '') + self.results[file_no][0]
            view = self.window.open_file(file_name, sublime.ENCODED_POSITION)
            regions = view.find_all(self.last_search_string)
            view.add_regions("search_in_project", regions, "entity.name.filename.find-in-files", "circle", sublime.DRAW_OUTLINED)

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
