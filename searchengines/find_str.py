###  Start of fixing import paths
import os, sys, inspect
# realpath() with make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
# use this if you want to include modules from a subforder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
 # Info:
 # cmd_folder = os.path.dirname(os.path.abspath(__file__)) # DO NOT USE __file__ !!!
 # __file__ fails if script is called in different ways on Windows
 # __file__ fails if someone does os.chdir() before
 # sys.argv[0] also fails because it doesn't not always contains the path
### End of fixing import paths

import shlex
import base


class FindStr (base.Base):
    """Uses Windows built-in findstr command."""

    def _arguments(self, query, folders):
        return (
            [self.path_to_executable] +
            shlex.split(self.mandatory_options) +
            shlex.split(self.common_options) +
            ['"/d:%s"' % ":".join(folders), query, "*.*"])

    def _is_search_error(self, returncode, output, error):
        return self._sanitize_output(error) != ""

engine_class = FindStr
