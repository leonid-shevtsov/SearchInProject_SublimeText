import sublime
import sublime_plugin
import os.path
import searchengines

basedir = os.getcwdu()


class SearchInProjectCommand(sublime_plugin.WindowCommand):
    def __init__(self, window):
        sublime_plugin.WindowCommand.__init__(self, window)
        self.last_search_string = ''
        pass

    def run(self):
        self.settings = sublime.load_settings('SearchInProject.sublime-settings')
        self.engine_name = self.settings.get("search_in_project_engine")
        pushd = os.getcwdu()
        os.chdir(basedir)
        __import__("searchengines.%s" % self.engine_name)
        self.engine = searchengines.__dict__[self.engine_name].engine_class(self.settings)
        os.chdir(pushd)
        view = self.window.active_view()
        selection_text = view.substr(view.sel()[0])
        self.window.show_input_panel(
            "Search in project:",
            selection_text or self.last_search_string,
            self.perform_search, None, None)
        pass

    def perform_search(self, text):
        self.last_search_string = text
        folders = self.search_folders()

        self.common_path = self.find_common_path(folders)
        self.results = self.engine.run(text, folders)
        if self.results:
            self.results = [[result[0].replace(self.common_path, ''), result[1]] for result in self.results]
            self.window.show_quick_panel(self.results, self.goto_result)
        else:
            self.results = []
            self.window.show_quick_panel(["No results"], None)

    def goto_result(self, file_no):
        if file_no != -1:
            file_name = self.common_path + self.results[file_no][0]
            view = self.window.open_file(file_name, sublime.ENCODED_POSITION)
            regions = view.find_all(self.search_string)
            view.add_regions("ack", regions, "entity.name.filename.find-in-files", "circle", sublime.DRAW_OUTLINED)

    def search_folders(self):
        return self.window.folders() or [os.path.dirname(self.window.active_view().file_name())]

    def find_common_path(self, paths):
        paths = [path.split("/") for path in paths]
        common_path = []
        while 0 not in [len(path) for path in paths]:
            next_segment = list(set([path.pop(0) for path in paths]))
            if len(next_segment) == 1:
                common_path += next_segment
            else:
                break
        return "/".join(common_path) + "/"
