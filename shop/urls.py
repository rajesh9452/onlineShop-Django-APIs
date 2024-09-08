from django.urls import path, include
from shop import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('category_list/', views.category_list, name='category-list'),
    path('add_category/', views.add_category, name='add-category'),
    path('update_category/<int:pk>/', views.update_category, name='update-category'),
    path('delete_category/<int:pk>/', views.delete_category),
    path('product/', views.product, name='product'),
    path('product/<int:pk>/', views.product, name='product-update'),
    path('order_list/', views.order_list),
    path('create_order/', views.create_order, name='create-order'),
]
