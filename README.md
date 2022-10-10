# VIN Decode Microservice

Microservice which provides information about VIN

## Installation
+ Build the containers
```bash
docker-compose build
```

+ Run the containers
```bash
docker-compose up
```
> Take into the consideration that you may need to run above command twice, if TCP/IP connection error will be raised. 
+ Once you were able to run the containers, run following command to initialize DB tables.
```bash
docker-compose run web python3 manage.py migrate
```

## Testing
+ Run pytest
```bash
docker-compose run web pytest
```

## Usage
+ Create new class for new service by inheriting `VinURLParser` and using metaclass `ParseFormat`
```python3
from vins.services.base_decode_vin import VinURLParser, ParseFormat


class NewServiceParser(VinURLParser, metaclass=ParseFormat):
    ...
```

+ Now you should specify url and format you need
```python3
class NewServiceParser(VinURLParser, metaclass=ParseFormat):
    url = "https://service.com/"
    formats = {"key": "find.value/0/type"}
```
> Those two attributes `url` and `formats` are required.

> Refer to docstring of `class VinURLParser` _->_ `vins/services/base_decode_vin.py` to get more information about
format syntax.

> Also see `class DynamicVINParser` _->_ `vins/services/dynamic_decode_vin.py` that doesn't require creation of new class,
but instead all the information about service, such as url, format, vin you should pass as parameters.

+ Go to serializers _->_ `vins/serializers/vin.py` and replace the default parser class as you need.
```python3
class VINCreateSerializer(BaseVINModelSerializer):
    parser_class = YourParserClass
```
> I recommend you to take a look for `class BaseVINModelSerializer` to see suggestions I left in the comments 
and see what is happening under the hood.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Contacts
Feel free to contact me if you have any questions or suggestions:
+ Telegram: @youngerwolf
+ Email: jamoliddin.bakhriddinov@gmail.com

## License
[MIT](https://choosealicense.com/licenses/mit/)