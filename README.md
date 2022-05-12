# django-frames
Use Django entities with pandas data frames
Django-Frames lets you:
+ switch back and forth between Django entities and pandas DataFrames
+ operate on cached objects
+ no loops required

consider a Django app
```Python
from django_frames.frames import FramedModel 

# let the model inherit the FramedModel methods as well
class Club(models.Model, FramedModel):
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

class Membership(models.Model, FramedModel):
    join_date = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=255, default='standard')
    fee = models.FloatField(null=True)
```

```Python
clubs = Club.objects.filter(invitation_only=True)
df_clubs = Club.to_df(clubs)
print(df_clubs)
```
Turn the DataFrames back into Entities
```python
clubs = Club.to_entities(df_clubs)
```

Django-Frames can make the related sets more accessible in your code
```Python
clubs = Club.objects.filter(invitation_only=True).prefetch_related('membership')
# join the prefetch cache when making the dataframe
df_membership = Clubs.to_df(clubs, join_prefetch=['membership'])
df_membership = df_members.assign(fee=0)  # do everything at once!
memberships = Membership.to_entities(df_membership)  # turn back into entities
Membership.objects.bulk_update(memberships, fields=['fee'])  # update the database
```
