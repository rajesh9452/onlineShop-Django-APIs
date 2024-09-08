from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from shop.serializers import UserSerializers, CategorySerializers, ProductSerializers, OrderSerializers
from .models import Category, Product, Order


@api_view(['POST'])
def login(request):
    try:
        user = get_object_or_404(User, email=request.data['email'])
        if not user.check_password(request.data['password']):
            return Response({'error': 'Please enter your valid password'}, status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        content = {'token': token.key, 'result': UserSerializers(instance=user).data}
        return Response(content, status=status.HTTP_200_OK)
    except:
        return Response({'error': '!Oops something error'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def category_list(self):
    try:
        serializer = CategorySerializers(Category.objects.filter(status=1), many=True)
        if serializer.data:
            return Response({'status': True, 'result': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'message': 'Data not found', 'result': []}, status=status.HTTP_200_OK)
    except:
        return Response({'error': '!Oops something error'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_category(request):
    serializer = CategorySerializers(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'status': True, 'result': serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def update_category(request, pk):
    item = Category.objects.get(pk=pk)
    data = CategorySerializers(instance=item, data=request.data)
    data.is_valid(raise_exception=True)
    data.save()
    return Response({'status': True, 'result': data.data}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete_category(request, pk):
    try:
        item = get_object_or_404(Category, pk=pk)
        item.delete()
        return Response({'status': True}, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def product(request, pk=None):
    if request.method == "POST":
        serializer = ProductSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': True, 'result': serializer.data}, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        item = Product.objects.get(pk=pk)
        data = ProductSerializers(instance=item, data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        return Response({'status': True, 'result': data.data}, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        productItem = get_object_or_404(Product, pk=pk)
        productItem.delete()
        return Response({'status': True}, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        serializer = ProductSerializers(Product.objects.filter(status=1), many=True)
        if serializer.data:
            return Response({'status': True, 'result': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'message': 'Data not found', 'result': []}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def order_list(request):
    serializer = OrderSerializers(Order.objects.filter(status=1, name=request.user), many=True)
    if serializer.data:
        return Response({'status': True, 'result': serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'status': False, 'message': 'Data not found', 'result': []}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_order(request):
    total_amount = 0
    products = []
    for item in request.data['products']:
        try:
            productItem = Product.objects.get(pk=item)
        except Product.DoesNotExist:
            return Response({'status': False, 'result': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        if productItem.stock > 0:
            productItem.stock -= 1  # Decrease stock
            productItem.save()  # Save product with updated stock
            total_amount += productItem.price  # Add product price to total
            products.append(productItem)
        else:
            return Response({'status': False, 'result': f"Product '{productItem.name}' is out of stock."}, status=status.HTTP_400_BAD_REQUEST)

    order = Order.objects.create(
        name=request.user,
        total_amount=total_amount,
    )
    order.products.set(products)
    order.save()
    serializer = OrderSerializers(order)
    return Response({'status': True, 'result': serializer.data}, status=status.HTTP_200_OK)