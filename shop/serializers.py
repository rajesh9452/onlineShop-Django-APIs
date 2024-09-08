from rest_framework import serializers
from django.contrib.auth.models import User
from shop.models import Category, Product, Order


class UserSerializers(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('id', 'username', 'password', 'email')


class CategorySerializers(serializers.ModelSerializer):
    class Meta(object):
        model = Category
        fields = ['id', 'name', 'description', 'created_at']

    def validate(self, data):
        name = data.get('name', None)
        description = data.get('description', None)
        if name == '':
            raise serializers.ValidationError('Category name cannot be empty.')
        if description == '':
            raise serializers.ValidationError('Category description cannot be empty.')
        return data


class ProductSerializers(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta(object):
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'category_name', 'stock', 'created_at']

    def validate(self, data):
        name = data.get('name', None)
        description = data.get('description', None)
        price = data.get('price', None)
        category = data.get('category', None)
        stock = data.get('stock', None)
        if name == '':
            raise serializers.ValidationError({'name': 'Product name cannot be empty.'})
        if description == '':
            raise serializers.ValidationError({'description': 'Product description cannot be empty.'})
        if price == '':
            raise serializers.ValidationError({'Price': 'Price cannot be empty.'})
        if category == '':
            raise serializers.ValidationError({'category': 'Category cannot be empty.'})
        if stock == '':
            raise serializers.ValidationError({'stock': 'Stock cannot be empty.'})
        return data


class OrderSerializers(serializers.ModelSerializer):
    products = ProductSerializers(many=True, read_only=False)

    class Meta(object):
        model = Order
        fields = ['id', 'name', 'products', 'total_amount', 'created_at']