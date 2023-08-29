from django.db import models
from django.contrib.auth import get_user_model
import uuid
import random
from django.utils import timezone
import string


class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    name = models.CharField(max_length=255, default="")
    description = models.TextField(default="")

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255, default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    name = models.CharField(max_length=255, default="")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    description = models.TextField(default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    sizes = models.ManyToManyField('ProductSize', related_name='products', default="Default Size")
    colors = models.ManyToManyField('ProductColor', related_name='products', default="Default Color")
    images = models.ManyToManyField('ProductImage', related_name='products')

class ProductSize(models.Model):
    name = models.CharField(max_length=20)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductColor(models.Model):
    color = models.CharField(max_length=255)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = "No image found"
        return url

class Cart(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    color = models.CharField(max_length=20, null=True, blank=True, default="Default Color")
    size = models.CharField(max_length=20, null=True, blank=True, default="Default Size")

    def subtotal(self):
        return self.product.price * self.quantity

class Order(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    items = models.ManyToManyField('OrderItem', related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=200, default="")
    payment_status_choices = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    ]
    DELIVERY_STATUS_CHOICES = (
        ('P', 'Pending'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
        ('F', 'Failed Delivery'),
    )
    payment_status = models.CharField(max_length=20, choices=payment_status_choices, default="Pending")
    delivery_status = models.CharField(max_length=1, choices=DELIVERY_STATUS_CHOICES, default='P')
    shipping_address = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
        
        super(Order, self).save(*args, **kwargs)

class OrderItem(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    color = models.CharField(max_length=20, null=True, blank=True, default="Default Color")
    size = models.CharField(max_length=20, null=True, blank=True, default="Default Size")

    def subtotal(self):
        return self.item_price * self.quantity

class ShippingAddress(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, default="")
    country = models.CharField(max_length=200)
    appartment = models.CharField(max_length=200, null=True, blank=True, default="None specified")
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    date_added = models.DateField(auto_now_add=True)

class Return(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=1, choices=(
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected')
    ), default='P')
    created_at = models.DateTimeField(auto_now_add=True)

class DiscountCode(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    code = models.CharField(max_length=20, default="")
    percentage = models.PositiveIntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

        current_time = timezone.now()

        if self.valid_from <= current_time <= self.valid_to:
            self.active = True
        else:
            self.active = False
        
        if self.is_used:
            self.active = False

        super(DiscountCode, self).save(*args, **kwargs)

class Notification(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    NOTIFICATION_TYPE = (
        ('REPORTS', 'Reports'),
        ('FINANCE', 'Finance'),
        ('ALERT', 'Alert'),
        ('REGISTRATION', 'Registration'),
        ('ORDER', 'Order'),
        ('ACTIVITY', 'Activity'),
    )
    title = models.CharField(max_length=255)
    notification = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=255, choices=NOTIFICATION_TYPE, default='Reports')
    date_created = models.DateTimeField(auto_now_add=True)

    def formatted_datetime(self):
        return self.date_created.strftime("%B %d, %Y")

class Review(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField(default="")
    authorFullName = models.CharField(max_length=255, default="")
    authorEmail = models.CharField(max_length=255, default="")
    authorPhoneNumber = models.CharField(max_length=255, default="")
    ratings = models.CharField(max_length=10, default="1")
    date_created = models.DateTimeField(auto_now_add=True)

class NewsletterSubscribers(models.Model):
    email = models.CharField(max_length=255, default="")

class WishListItem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="wishlist_item", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)