from pathlib import Path

HIDE_MENU = """
<style>
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
"""


def read_markdown_file(md_file) -> str:
    """Given a path to a markdown file, it reads the file."""
    return Path(md_file).read_text()