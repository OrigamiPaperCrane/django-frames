from django.db import models
from django_frames.extensions import FramedModel


class College(models.Model, FramedModel):
    name = models.CharField(max_length=255)
    objects = models.Manager

class Club(models.Model, FramedModel):
    name = models.fields.CharField(max_length=255, null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    founding_date = models.DateTimeField(null=True)
    invitation_only = models.BooleanField(default=False)
    college = models.ForeignKey(College, null=True, on_delete=models.CASCADE)
    objects = models.Manager

class Role(models.Model, FramedModel):
    name = models.CharField(max_length=255, null=False)
    is_elected = models.BooleanField(default=False)
    objects = models.Manager

class Member(models.Model, FramedModel):
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=255, null=False)
    memberships = models.ManyToManyField(Club, through='Membership')
    occupation = models.CharField(max_length=255, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    objects = models.Manager

class Membership(models.Model, FramedModel):
    join_date = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=255, default='standard')
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    fee = models.FloatField(null=True)
    objects = models.Manager
