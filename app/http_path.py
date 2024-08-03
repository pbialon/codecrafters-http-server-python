import re


class HttpPath:
    ARG_INDICATOR = ":"
    PATH_SEPARATOR = "/"

    def __init__(self, raw_path_pattern: str):
        self._raw_path_pattern = self._sanitize_path_pattern(raw_path_pattern)

    def match(self, raw_path: str):
        sanitized_raw_path = self._ensure_trailing_slash(raw_path)
        return re.match(self._regex_pattern(), sanitized_raw_path)
    
    def parse(self, raw_path: str):
        match = self.match(raw_path)
        return {
            arg: value
            for arg, value in zip(self._dynamic_arguments(), match.groups())
        }
        

    def _dynamic_arguments(self):
        return [
            arg[1:]
            for arg in self._raw_path_pattern.split(self.PATH_SEPARATOR)
            if arg.startswith(self.ARG_INDICATOR)
        ]

    def _regex_pattern(self):
        pattern = self._raw_path_pattern
        for arg in self._dynamic_arguments():
            pattern = pattern.replace(f":{arg}", "(.+)")
        # add start and end of string anchors
        return f"^{pattern}$"

    def _sanitize_path_pattern(self, raw_path: str) -> str:
        if not raw_path.startswith("/"):
            raise ValueError("Path must start with /")
        return self._ensure_trailing_slash(raw_path)
    
    def _ensure_trailing_slash(self, raw_path: str) -> str:
        return raw_path if raw_path.endswith("/") else f"{raw_path}/"        
