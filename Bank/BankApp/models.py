from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User


class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_banker = models.BooleanField(default=False)
    is_customeruser = models.BooleanField(default=False)




class user(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    account_no = models.IntegerField()
    image = models.ImageField(upload_to='images/')
    address = models.CharField(max_length=500)
    email = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.IntegerField()
    dob = models.DateField()
    adharcard = models.IntegerField()
    pancard = models.IntegerField()
    initial_amount = models.IntegerField()

    def __str__(self):
        return self.name


class Transaction(models.Model):
    custom_id = models.ForeignKey(user, on_delete=models.CASCADE)
    amount = models.IntegerField(null=True, blank=True)
    details = models.CharField(null=True, blank=True, max_length=200)
    balance = models.IntegerField(null=True, blank=True)
    branch = models.CharField(max_length=250)
    bank_name = models.CharField(max_length=250, null=True, blank=True)
    ifsc_code = models.CharField(max_length=250, null=True, blank=True)
    dateandtime = models.DateTimeField(auto_now_add=True)

