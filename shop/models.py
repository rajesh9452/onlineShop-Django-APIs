from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    status = ((1, 'Active'), (2, 'Deactivate'), (3, 'Delete'))
    name = models.CharField(max_length=100,blank=True,default='')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, choices=status, default=1)

    def __str__(self):
        return f"{self.name}"
    # class Meta:
    #     abstract = True


class Product(models.Model):
    status = ((1, 'Active'), (2, 'Deactivate'), (3, 'Delete'))
    name = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True)
    price = models.FloatField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=status, default=1)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    status = ((1, 'Active'), (2, 'Deactivate'), (3, 'Delete'))
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_amount = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=status, default=1)

    def __str__(self):
        return f"{self.name}"

