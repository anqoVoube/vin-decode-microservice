from vins.services.base_decode_vin import VinURLParser


class DynamicVINParser(VinURLParser):
    """
    Dynamic Parser class to parse data from any service.

    This class allows to parse the data without creating new separate classes.
    Note that you should use POST method to be able to use it in your application,
    since you need all the information.
    """
    def __init__(self, url: str, prefix: str, convert_format: Dict[str, str], require_all_keys, vin, trailing_slash):
        self.url = url
        self.prefix = prefix
        self.format = convert_format
        self.require_all_keys = require_all_keys
        super().__init__(vin, trailing_slash)
