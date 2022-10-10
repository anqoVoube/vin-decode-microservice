from rest_framework.serializers import ModelSerializer

from vins.models import VIN


class BaseVINModelSerializer(ModelSerializer):
    parser_class = None

    class Meta:
        model = VIN
        fields = ["id"]

    def create(self, validated_data):
        # Here I used default VINParser class, but you can use Dynamic one, but with post method
        # with required fields in it.
        # TODO: Make exceptions here if needed or change ParseError to ValidationError with message for client
        # TODO: Otherwise it will throw 500 - Internal Error
        parsed_data = self.parser_class(validated_data["id"], trailing_slash=True).parse()
        validated_data.update(parsed_data)
        return super().create(validated_data)

