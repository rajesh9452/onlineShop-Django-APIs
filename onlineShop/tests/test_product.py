import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_create_product():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)

    url = reverse('product')
    data = {
        'name': 'Smartphone',
        'price': 500,
        'stock': 20,
        'category': 3,
        'description': 'Test',

    }
    response = client.post(url, data, format='json')

    assert response.status_code == 200
    assert response.data['status'] == True
    assert response.data['result']['name'] == 'Smartphone'
