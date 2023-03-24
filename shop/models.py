from django.db import models
from django.conf import settings


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    cat = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=None, blank=True, null=True)

    sub_name = models.CharField(
        max_length=200, default=None, blank=True, null=True)

    def __str__(self):
        return self.sub_name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, default=None, blank=True, null=True)
    slug = models.SlugField()
    desc = models.TextField()
    image = models.ImageField()
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    brand = models.CharField(max_length=100)
    image1 = models.ImageField(null=True, blank=True, default=None)
    image2 = models.ImageField(null=True, blank=True, default=None)
    image3 = models.ImageField(null=True, blank=True, default=None)

    def __str__(self):
        return self.name
    
    def price_discount(self):
        p=self.price - (self.price*self.discount_price)/100
        return round(p)


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return self.item.name

    def get_price(self):
        return self.item.price * self.qty

    def get_discount_price(self):
        result = (self.item.price*self.item.discount_price)/100
        tresult = result*self.qty
        return round(tresult)

    def pay(self):
        payble = self.get_price() - self.get_discount_price()
        return round(payble)


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey( Coupon, on_delete=models.CASCADE, null=True, blank=True)
    address=models.ForeignKey("Address",on_delete=models.CASCADE,null=True,blank=True)
    order_id=models.CharField(max_length=20,null=True,blank=True,default=None)

    def __str__(self):
        return self.user.username

    def get_total_amount(self):
        total = 0
        for oi in self.items.all():
            total += oi.get_price()
        return (total)

    def get_total_discount(self):
        total_discount = 0
        for oi in self.items.all():
            total_discount += oi.get_discount_price()
        return (total_discount)

    def total_after_discount(self):
        return (self.get_total_amount()-self.get_total_discount())

    def gst(self):
        return round(self.total_after_discount()*0.18)

    def getcoupondiscount(self):
        return self.coupon.amount

    def total_payble(self):
        if self.total_after_discount()+self.gst() > 0:
            return self.total_after_discount()+self.gst()-self.getcoupondiscount()
        else:
            return 0

    def total(self):

        return self.total_after_discount()+self.gst()


class Address(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    alt_contact = models.CharField(max_length=200, null=True, blank=True)
    street = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    pincode = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=(('Home', 'home'), ('Office', 'Office')))
    isDefault = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.user.username
