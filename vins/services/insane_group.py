from core.settings import INSANE_GROUP_URL
from vins.services.base_decode_vin import BaseVINURLParser


class InsaneGroupParseVIN(BaseVINURLParser):
    """
    InsaneGroup class is an example of using VinURLParser,
    change anything as you want or create another class,
    and use it to decode the VIN and to save it in DB

    Note:
        The required fields are `url` and `formats`
    """
    url = INSANE_GROUP_URL
    prefix = "decode.vehicle/0"
    formats = {
        "year": "year",
        "make": "make",
        "model": "model",
        "type": "Equip/0/value",
        "color": "color",
        "dimensions": "dimensions",
        "weight": "weight"
    }
    require_all_keys = True
