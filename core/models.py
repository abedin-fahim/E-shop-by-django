from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=120,null=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance, email=instance.email, name=instance.username)

post_save.connect(create_customer, sender=User)

class Product(models.Model):
    name = models.CharField(max_length=150, null=True)
    price = models.FloatField()
    is_digital = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if item.product.is_digital == False:
                shipping = True
        return shipping
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.product.price * item.quantity for item in orderitems])
        return total
        
class OrderItem(models.Model):
     product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
     order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
     quantity = models.IntegerField(default=0, null=True,blank=True)
     date_added = models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return f"({self.order}) {self.product}"
     
     @property
     def get_total(self):
         total = self.product.price * self.quantity
         return total

class ShippingAddress(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True)  
  order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
  address = models.CharField(max_length=150, null=True)
  city = models.CharField(max_length=150, null=True)
  state = models.CharField(max_length=150, null=True)
  zipcode = models.CharField(max_length=150, null=True)
  date_added = models.CharField(max_length=150, null=True)

  def __str__(self):
        return str(self.address)