import base


class FindStr (base.Base):
    """Uses Windows built-in findstr command."""

    def _command_line(self, query, folders):
        return " ".join([
            self.path_to_executable,
            self.mandatory_options,
            self.common_options,
            '"/d:%s"' % ":".join(folders),
            query,
            "*.*"
            ])


engine_class = FindStr
