import textwrap
from collections import UserString


class StrFormat(UserString):
    def indent(self, prefix: str) -> str:
        return textwrap.indent(self.data, prefix, lambda line: True)
