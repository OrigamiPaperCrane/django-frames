from django.db import models

# Create your models here.
class Club(models.Model):
    name = models.fields.CharField(max_length=255, null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    founding_date = models.DateTimeField(null=True)
    invitation_only = models.BooleanField(default=False)

class Member(models.Model):
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=255, null=False)
    memberships = models.ManyToManyField(Club, through='Membership', on_delete=models.SET_NULL)
    creation_date = models.DateTimeField(auto_now_add=True)

class Membership(models.Model):
    join_date = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=255, default='standard')
    fee = models.FloatField(null=True)
