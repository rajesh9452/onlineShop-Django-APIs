import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@pytest.mark.django_db
def test_login_success():
    client = APIClient()
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
    url = reverse('login')
    data = {'email': 'test@example.com', 'password': 'testpass'}
    response = client.post(url, data, format='json')
    # Assert token and response
    assert response.status_code == 200
    assert 'token' in response.data


@pytest.mark.django_db
def test_login_invalid_password():
    client = APIClient()
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
    url = reverse('login')
    data = {'email': 'test@example.com', 'password': 'wrongpass'}
    response = client.post(url, data, format='json')
    assert response.status_code == 404
    assert response.data['error'] == 'Please enter your valid password'
