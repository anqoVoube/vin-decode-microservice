import os

from core.settings import BASE_DIR
from utils.converter.json_to_python import JSonToPythonConverter
from utils.errors.parse import ParseError
from vins.services.insane_group import InsaneGroupParseVIN
import pytest

from vins.tests.test_vin_api import TEST_INPUTS

FILE_PATH = os.path.join(BASE_DIR, 'vins', 'fixtures', 'service_data.json')


@pytest.fixture
def load_sample():
    with open(FILE_PATH, "r") as data:
        return JSonToPythonConverter(data.read()).convert()


@pytest.mark.parametrize("test_input", TEST_INPUTS)
def test_parser_success(load_sample, test_input):
    assert load_sample[test_input] == InsaneGroupParseVIN(test_input, trailing_slash=True).parse()


@pytest.mark.parametrize("test_input", TEST_INPUTS)
def test_parser_format_key_fail(load_sample, test_input):
    parser = InsaneGroupParseVIN(test_input, trailing_slash=True)
    parser.prefix = "incorrect_format"
    with pytest.raises(ParseError) as error_info:
        parser.parse()
    assert error_info.value.reason == "KeyError"


@pytest.mark.parametrize("test_input", ["1P3EW65F4VV300946", "JN8DR07XX1W514175"])
def test_parser_format_index_fail(load_sample, test_input):
    parser = InsaneGroupParseVIN(test_input, trailing_slash=True)
    parser.prefix = "decode.vehicle/1"
    with pytest.raises(ParseError) as error_info:
        parser.parse()
    assert error_info.value.reason == "IndexError"
