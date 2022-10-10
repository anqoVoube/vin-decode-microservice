from rest_framework.serializers import ModelSerializer

from vins.models import VIN
from vins.serializers.base_vin import BaseVINModelSerializer
from vins.services.insane_group import InsaneGroupParseVIN


class VINRetrieveSerializer(ModelSerializer):
    class Meta:
        model = VIN
        fields = "__all__"


class VINCreateSerializer(BaseVINModelSerializer):
    parser_class = InsaneGroupParseVIN
