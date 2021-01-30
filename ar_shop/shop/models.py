from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Catogery(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    catogery = models.ForeignKey(Catogery, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    discount = models.FloatField(null=True, blank=True)
    active = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = '/static/assets/img/product/product-1.jpg'
        return url

    @property
    def discount_price(self):
        new_price = self.price - (self.price * (self.discount/100))
        return new_price

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
	    return self.product.title

    @property
    def imageURL(self):
	    try:
	    	url = self.image.url
	    except:
	    	url = '/static/assets/img/product/product-1.jpg'
	    # print('URL:', url)
	    return url


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
     	('Out for delivery', 'Out for delivery'),
     	('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    date_odered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum(item.get_total for item in orderitems)
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum(item.quantity for item in orderitems)
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    # def __str__(self):
    #     return str(self.order.customer.name+":"+self.product.title)

    @property
    def get_total(self):
        if self.product.discount:
            total = self.quantity * self.product.discount_price
        else:
            total = self.quantity * self.product.price
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    pincode = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=13, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)


class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=2000, null=False)
    state = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=50, null=False)
    pincode = models.CharField(max_length=6, null=False)
    country = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=13, null=False)

    def __str__(self):
        return str(self.customer.id)


class Country(models.Model):
    country = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return str(self.country)


class Pincode(models.Model):
    pincode = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return str(self.pincode)
