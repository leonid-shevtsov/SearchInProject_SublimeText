import subprocess


class Base:
    """
        This is the base search engine class.
        Override it to define new search engines.
    """

    SETTINGS = [
        "path_to_executable",
        "mandatory_options",
        "common_options"
    ]

    def __init__(self, settings):
        """
            Receives the sublime.Settings object
        """
        self.settings = settings
        for setting_name in self.__class__.SETTINGS:
            setattr(self, setting_name, self.settings.get(self._full_settings_name(setting_name), ''))
        pass

    def run(self, query, folders):
        """
            Run the search engine. Return a list of tuples, where first element is
            the absolute file path, and optionally row information, separated
            by a semicolon, and the second element is the result string
        """
        command_line = self._command_line(query, folders)
        print("Running: %s" % command_line)
        pipe = subprocess.Popen(command_line, shell=True, stdout=subprocess.PIPE)
        output, error = pipe.communicate()
        if pipe.returncode != 0:
            raise Exception('Search engine returned error level: %s' % pipe.returncode, output, error)
        return self._parse_output(self._sanitize_output(output).strip())

    def _command_line(self, query, folders):
        """
            Prepare a command line for the search engine.
        """
        return " ".join([
            self.path_to_executable,
            self.mandatory_options,
            self.common_options,
            query
            ] + folders)

    def _sanitize_output(self, output):
        return unicode(output, errors='replace')

    def _parse_output(self, output):
        lines = output.split("\n")
        line_parts = [line.split(":", 2) for line in lines]
        line_parts = self._filter_lines_without_matches(line_parts)
        return [(":".join(line[0:-1]), line[-1].strip()) for line in line_parts]

    def _full_settings_name(self, name):
        return "search_in_project_%s_%s" % (self.__class__.__name__, name)

    def _filter_lines_without_matches(self, line_parts):
        return filter(lambda line: len(line) > 2, line_parts)
