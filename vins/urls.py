from django.urls import path
from vins.views import VINAPIView


urlpatterns = [
    path('vin/<str:pk>/', VINAPIView.as_view(), name="vin-get"),
]