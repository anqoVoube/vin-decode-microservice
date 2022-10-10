import json

from django.db.models import Model
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from vins.models import VIN
from vins.schemas.vin import response_schema_dict
from vins.serializers import VINRetrieveSerializer, VINCreateSerializer


class VINAPIView(APIView):
    """
    Returns VIN data by its ID.

    Creates instance and returns its data
    by decoding it from given service if VIN wasn't found in this DB.
    """
    model = VIN
    serializer_class = VINRetrieveSerializer
    create_serializer_class = VINCreateSerializer

    def is_exist(self, pk: str):
        # ID is primary key and unique field in DB,
        # so we can make sure that while doing filter,
        # we won't get two objects. We either get one or nothing.
        return self.model.objects.filter(id=pk).exists()

    def get_object(self, pk: str) -> Model:
        return self.model.objects.get(id=pk)

    @swagger_auto_schema(responses=response_schema_dict)
    def get(self, request, pk: str) -> Response:
        # If we have not any information about this VIN
        # we send request to another service and creating new instance.
        if not self.is_exist(pk):
            self.create_instance(pk)
        instance = self.model.objects.get(id=pk)
        return Response(self.serializer_class(instance).data)

    def create_instance(self, pk: str):
        serializer = self.create_serializer_class(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
