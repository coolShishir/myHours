from __future__ import unicode_literals
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from rest_framework.authtoken.models import Token

class User(AbstractUser):
    CONST_USER_CLIENT = 'C'
    CONST_USER_ADMIN = 'A'
    CONST_USER_EMPLOYEE = 'E'
    CONST_USER_TYPE_CHOICES = (
        (CONST_USER_CLIENT, 'client'),
        (CONST_USER_ADMIN, 'admin'),
        (CONST_USER_EMPLOYEE, 'employee'),
    )
    Id = models.UUIDField(default=uuid.uuid4,
                           primary_key=True)
    UserType = models.CharField(choices=CONST_USER_TYPE_CHOICES,
                                 default=CONST_USER_ADMIN,
                                 max_length=2,
                                 )
    PhoneNumber = models.CharField(max_length=100, blank=True, null = True)
    UserPic = models.ImageField(upload_to='/home/shishir/Documents/shishir/project/static/images',
                                 default='/home/shishir/Pictures/')
    def __str__(self):
        return self.username

    def get_or_create_auth_token(self):
        token = Token.objects.get_or_create(user=self)
        token_key = token[0].key if type(token) == type((1, 2)) else token.key
        return token_key

class UserLog(models.Model):
    Id = models.UUIDField(default=uuid.uuid4, primary_key=True, name='Id')
    Name = models.CharField(max_length=100, blank=True , null=True)
    Action = models.CharField(max_length=100,blank=True, null=True)
    Time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class Project(models.Model):
    Id = models.UUIDField(default=uuid.uuid4,primary_key=True,name='Id')
    Created = models.DateTimeField(auto_now_add=True)
    Title = models.CharField(max_length=100, blank=True, null = True)
    HoursSpent = models.CharField(max_length=100, blank=True, null = True)
    HoursEstimated = models.CharField(max_length=100, blank=True , null=True)
    LastBuildDate =  models.CharField(max_length=100, blank=True, null=True)
    NextBuildDate =  models.CharField(max_length=100, blank=True, null=True)
    IsPending =  models.IntegerField(blank=True, default=1, null=True)
    IsDeliever = models.IntegerField(blank=True, default=0, null=True)
    TotalProjectValue = models.IntegerField( blank=True, null= True)
    TotalInvoiceValue =  models.IntegerField( blank=True, null = True )
    ModelPic = models.ImageField(upload_to='/home/shishir/Documents/shishir/project/static/images', default='/home/shishir/Pictures/images.jpg')
    Users = models.ManyToManyField(User)
    class Meta:
        ordering = ['Created']

