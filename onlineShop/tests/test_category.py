import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@pytest.mark.django_db
def test_category_list_authenticated():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)
    url = reverse('category-list')  # Ensure the URL is mapped correctly
    response = client.get(url)
    assert response.status_code == 200
    assert 'result' in response.data


@pytest.mark.django_db
def test_category_list_unauthenticated():
    client = APIClient()
    url = reverse('category-list')
    response = client.get(url)
    assert response.status_code == 403  # Unauthenticated users should not be allowed


@pytest.mark.django_db
def test_add_category_authenticated():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)
    url = reverse('add-category')
    data = {'name': 'Electronics', 'status': 1}
    response = client.post(url, data, format='json')
    assert response.status_code == 200
    assert response.data['status'] == True
    assert response.data['result']['name'] == 'Electronics'


@pytest.mark.django_db
def test_add_category_unauthenticated():
    client = APIClient()
    url = reverse('add-category')
    data = {'name': 'Electronics', 'status': 1}
    response = client.post(url, data, format='json')
    assert response.status_code == 403

