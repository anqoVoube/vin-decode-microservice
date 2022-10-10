import json
from typing import Union

from utils.converter.base import Converter


class JSonToPythonConverter(Converter):
    """
    JSonConverter which converts parsed text to dict
    Attrs:
        `text`: Parsed text from file
    Examples:
        Data type of string will be::
        {
            "title": "Hello World",
            "source": "Check it"
        }
        which will eventually converted to python data type
    """

    text: str

    def __init__(self, text):
        self.text = text

    def convert(self) -> Union[dict, list]:
        """
        Converts to python data type
        Returns:
            converted dict or list
        """
        return json.loads(self.text)
