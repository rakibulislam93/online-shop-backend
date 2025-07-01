from django.db import models
from accounts .models import CustomUser
from django.conf import settings
# Create your models here.

# categories model
class Category(models.Model):
    name = models.CharField(max_length=100)
    # icon = models.ImageField(upload_to='category_icons/', null=True, blank=True)
    icon = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    title = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    description = models.TextField()
    # image = models.ImageField(upload_to='product_images/',null=True,blank=True)
    image = models.URLField(blank=True,null=True)
    price = models.DecimalField(max_digits=12,decimal_places=2,default=0.0)
    discount_percentages = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='products',null=True,blank=True)
    
    def __str__(self):
        return f'{self.title} ----> {self.name}'
   


class Cart(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Cart for {self.user.username}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'product')  # same product not in the cart..

    def __str__(self):
        return f"{self.product.name} in {self.cart.user.username} 's cart"

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Order #{self.id} for {self.user.username}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    


RATING = [
    ('1', '⭐'),
    ('2', '⭐⭐'),
    ('3', '⭐⭐⭐'),
    ('4', '⭐⭐⭐⭐'),
    ('5', '⭐⭐⭐⭐⭐'),
]
class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    reviewer = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='reviews')
    comment = models.TextField()
    rating = models.CharField(choices=RATING,max_length=20)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['reviewer', 'product'], name='unique_reviewer_product')
        ]
        
    
    def __str__(self):
        return f'{self.product.name} review by {self.reviewer.username}'

