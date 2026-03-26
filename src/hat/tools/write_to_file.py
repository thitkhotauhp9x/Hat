from pathlib import Path

from langchain_core.tools import tool


@tool
def write_to_file(content: str, file_path: str) -> None:
    """
    Write content to a file at a specified file path.

    :param content: The content to write to the file
    :param file_path: The path of the file to write to
    :return:
    """
    Path(file_path).write_text(content)
