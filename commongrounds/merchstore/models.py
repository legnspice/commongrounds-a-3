from django.db import models
from django.urls import reverse
from accounts.models import Profile


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Product(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('On sale', 'On sale'),
        ('Out of stock', 'Out of stock'),
    ]

    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        ProductType,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    owner = models.ForeignKey(
        Profile,
        related_name="products",
        on_delete=models.CASCADE,
        null=True
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def get_absolute_url(self):
        return reverse('merchstore:item_detail', args=[self.pk])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('On cart', 'On cart'),
        ('To Pay', 'To Pay'),
        ('To Ship', 'To Ship'),
        ('To Receive', 'To Receive'),
        ('Delivered', 'Delivered'),
    ]

    buyer = models.ForeignKey(
        Profile,
        related_name="transactions",
        on_delete=models.SET_NULL,
        null=True
    )
    product = models.ForeignKey(
        Product,
        related_name="transactions",
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='On cart')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer} - {self.product} x{self.amount}"
