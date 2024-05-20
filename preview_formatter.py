import json
import re

from string_helper import truncate


class FormatterInterface:

    def match(self, content_type) -> bool:
        pass

    def format(self, text) -> str | None:
        pass


class JsonFormatter(FormatterInterface):

    def __init__(self, max_lines: int = 1000, max_columns: int = 500):
        self._max_lines = max_lines
        self._max_columns = max_columns

    def match(self, content_type) -> bool:
        return re.match(r'\b(application|text)/json\b', content_type.lower()) is not None

    def format(self, content: bytes) -> str | None:
        try:
            parsed_data = json.loads(content.decode('utf-8'))
            return truncate(json.dumps(parsed_data, indent=2, ensure_ascii=False), lines=self._max_lines)
        except(json.JSONDecodeError, UnicodeDecodeError):
            return None


class TextFormatter(FormatterInterface):
    def __init__(self, max_lines: int = 1000, max_columns: int = 500):
        self._max_lines = max_lines
        self._max_columns = max_columns

    def match(self, content_type) -> bool:
        return re.match(r'^text/', content_type.lower()) is not None

    def format(self, content: bytes) -> str | None:
        try:
            return truncate(content.decode('utf-8'), lines=self._max_lines, columns=self._max_columns)
        except UnicodeDecodeError:
            return None


class Formatter:
    def __init__(self):
        self.formatters = [JsonFormatter(), TextFormatter()]

    def format(self, content_type: str, content: bytes):
        for formatter in self.formatters:
            if formatter.match(content_type):
                formatted_content = formatter.format(content)
                if formatted_content is not None:
                    return formatted_content
        return None
