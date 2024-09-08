import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from shop.models import Product,Category


@pytest.mark.django_db
def test_create_order():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)

    # Create product
    category = Category.objects.create(name='Electronics', status=1)
    product = Product.objects.create(name='Laptop', category=category, price=1000, stock=10)

    # Create order
    url = reverse('create-order')
    data = {
        'products': [product.id]  # Send the product ID in the request
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 200
    assert response.data['status'] == True
    assert response.data['result']['total_amount'] == 1000
    assert product.stock == 9
