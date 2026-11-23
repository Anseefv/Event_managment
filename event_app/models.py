from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):

    ROLE_OPTIONS=[

        ('admin','admin'),
        ('supervisor','supervisor'),
        ('employee','employee')

    ]
    email=models.EmailField(unique=True)

    role=models.CharField(max_length=30,choices=ROLE_OPTIONS,default='employee')
    phone=models.CharField(max_length=13,unique=True)
    
    

    def __str__(self):
        return self.username

    

class Profile(models.Model):

    age=models.PositiveIntegerField()
    photo=models.ImageField(upload_to='user_photo',null=True)
    owner=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='profile')
    wage=models.PositiveIntegerField(default=0)
    over_time_wage=models.PositiveIntegerField(default=0)


class PendingList(models.Model):

    STATUS_OPTIONS=[
        ("rejected","rejected"),
        ("pending","pending"),
    ]


    start_date=models.DateField()
    start_time=models.TimeField()
    stop_date=models.DateField()
    stop_time=models.TimeField()
    status=models.CharField(max_length=30,choices=STATUS_OPTIONS,default="pending")
    employee=models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.username