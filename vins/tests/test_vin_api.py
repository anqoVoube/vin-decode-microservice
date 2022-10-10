import pytest
from django.urls import reverse

from vins.models import VIN

TEST_INPUTS = ["1P3EW65F4VV300946", "JN8DR07XX1W514175"]


@pytest.fixture
def create_instance():
    VIN.objects.bulk_create(
        [VIN(id=test_input) for test_input in TEST_INPUTS]
    )


@pytest.mark.django_db
@pytest.mark.parametrize("test_input", TEST_INPUTS)
def test_get_with_creation(client, test_input):
    url = reverse('vin-get', kwargs={"pk": test_input})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("test_input", TEST_INPUTS)
def test_get_without_creation(client, create_instance, test_input):
    if not VIN.objects.filter(id=test_input).exists():
        assert False
    url = reverse('vin-get', kwargs={"pk": test_input})
    response = client.get(url)
    assert response.status_code == 200
