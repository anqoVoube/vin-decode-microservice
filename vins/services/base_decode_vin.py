from typing import List, Optional, Union, Dict

from utils.converter.json_to_python import JSonToPythonConverter
from utils.errors.parse import ParseError
from utils.response_getter import ResponseDataGetter


class ParseFormat(type):
    REQUIRED_FIELDS = ("url", "formats")

    def __new__(mcs, name, bases, attrs):
        for field in mcs.REQUIRED_FIELDS:
            assert attrs.get(field, None) is not None, (
                    "'%s' should include a `%s` attribute" % (name, field)
            )

        return super().__new__(mcs, name, bases, attrs)


class VinURLParser:
    """
    Base class for Parsing a VIN via URL.

    Override set_format for your service
    Attributes:
        `url`: url of service from which json data will be fetched.
        `prefix`: Cut off unnecessary data to update
        response and fetch the data from it (updated one) not from base response
        `formats`: key-value object where key is key of dictionary
        and value is format. Format should be string.
        To separate sequential keys you should put dot between them.
        For Example if you want ['Equip']['value'] -> you should pass 'Equip.value'
        In order to show indexation (in case of lists) separate them with slash
        before and at the end like /0/ -> [0] (zero index)
        For Example: ['Equip']['type'][0]['value'] -> 'Equip.type/0/value'
        `require_all_keys`: Indicates if all the keys should be fetched
        without errors. If attribute set to True and for some reason
        the data didn't fetch successfully, the error will be raised.
        `__init__`:
            `vin`: VIN itself.
            `trailing_slash`: Indicates whether url should end with slash.
    Note:
        This is base class, it won't work without overriding
        required attributes such as `url` and `formats`
    """

    url: str = ""
    prefix: Optional[str] = None
    formats: Dict[str, str] = {}
    require_all_keys: Optional[bool] = False

    def __init__(self, vin: str, trailing_slash: bool = False):
        self.set_full_url(vin, trailing_slash)
        self.response = self.get_decoded_info(self.url)
        self.translated_values = []

    def set_full_url(self, vin, trailing_slash):
        """
        Method that sets full url for sending the request to service

        Args:
            `vin`: VIN itself
            `trailing_slash`: Is decode service needs trailing slash,
            when sending request.
        """

        # Checking if there is trailing slash
        if self.url[-1] != "/":
            self.url += "/"

        # Adding vin to url
        self.url += f"{vin}"

        # If service requires trailing slash set to True
        if trailing_slash:
            self.url += "/"

    def parse(self):
        """
        Main method for parsing the JSon data.

        Returns:
            A dict mapping keys to the corresponding json data
            fetched. Each row can be represented as `dict`, `str` or `int`. For
            example:

            {
              "vin": "SCBBR9ZA1AC063223",
              "year": "1997",
              "make": "Plymouth",
              "model": "Prowler",
              "type": "DOHC 48V TURBO",
              "color": "Yellow",
              "dimensions": {
                "Wheelbase": "112.50",
                "Rear Legroom": "39.50",
                "Front Legroom": "41.20",
              },
              "weight": {
                "type": "Curb Weight",
                "unit": "lbs",
                "value": 5568
              }
            }

            Output and validation depends on dict value `formats`
        """
        return {key: value for key, value in zip(self.formats.keys(), self.get_values())}

    def get_values(self):
        if self.prefix:
            # Updating our `response` attribute, because of prefix,
            # thereby cutting off unnecessary data
            self.response = self.translate_value(self.response, self.prefix)

        for decode_format in self.formats.values():
            # Adding to list our converted values
            self.translated_values.append(
                self.translate_value(self.response, decode_format)
            )

        return self.translated_values

    def translate_value(self, value: Union[Dict, List], decode_format: str) -> Union[Dict, List, str, int]:
        """
        Function that gets the value by passed format

        Args:
            `value`: Python-object from which data will be fetched.
            `decode_format`: Full format. Indicates the way how data should be fetched

        Example:
             `'year.month/1/type'` -> will be converted to `value['year']['month'][1]['type']`

        Raises:
            ParseError - Couldn't get the value by (key, index) with given format.
            Note that error raises if required_all_keys is True.

        Note:
            For loop block contains `if not info: continue`. It is written to avoid
            appending slashes in format. Example: 'year.month/1/type/', slash at the end
            or in short trailing slash.
        """
        for info in decode_format.split("/"):
            # We will continue our iteration if `info` is empty string ('')
            # in case of trailing slash.
            if not info:
                continue
            try:
                if info.isdigit():
                    value = self.get_by_indexation(value, int(info))
                else:
                    value = self.get_by_keys(value, info)
            except (KeyError, IndexError) as ex:
                if self.require_all_keys:
                    self._raise_exception(ex, decode_format)
                # TODO: Logging here... To be able to see that field wasn't fetched
                value = None

        return value

    @staticmethod
    def _raise_exception(ex: Exception, decode_format: str):
        error_name = type(ex).__name__
        # TODO: Change to serializers.ValidationError if needed. Otherwise it will throw 500 error.
        raise ParseError(
            f"Couldn't get the value because of `{ex.args[0]}` with format {decode_format}. Original exception is: {str(ex)}",
            error_name
        )

    @staticmethod
    def get_by_indexation(value, index) -> Union[Dict, List, str, int]:
        return value[index]

    @staticmethod
    def get_by_keys(value, keys) -> Union[Dict, List, str, int]:
        for key in keys.split("."):
            value = value[key]
        return value

    @staticmethod
    def get_decoded_info(url):
        return JSonToPythonConverter(
            ResponseDataGetter(url).fetch()
        ).convert()