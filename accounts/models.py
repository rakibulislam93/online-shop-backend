from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

ACCOUNT_ROLE = [
    ('admin','Admin'),
    ('seller','Seller'),
    ('customer','Customer'),
]
APPROVAL_STATUS = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    approval_status = models.CharField(max_length=50,choices=APPROVAL_STATUS,default='pending')
    user_role = models.CharField(choices=ACCOUNT_ROLE,max_length=50,default='customer')


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile')
    profile_pic = models.ImageField(upload_to='profile_pics/',blank=True,null=True)
    address = models.TextField(help_text='Enter full address including city, district, etc.')
    phone = models.CharField(max_length=12)
    
    def __str__(self):
        return self.user.username