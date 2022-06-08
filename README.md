# django-frames
Use Django entities with pandas data frames
Django-Frames lets you:
+ switch back and forth between Django entities and pandas DataFrames
+ operate on cached objects
+ no loops required


## How to use
```Python
from django_frames.extensions import FramedModel

# let the models inherit the FramedModel
class Member(models.Model, FramedModel):
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=255, null=False)
    memberships = models.ManyToManyField(Club, through='Membership')
    occupation = models.CharField(max_length=255, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    objects = models.Manager
```


## Querysets as DataFrames
```Python
members = Member.objects.all()
df_members = Member.to_df(members)
print(df_members)
```

```Python
     first_name last_name  ...                    creation_date  role
id                         ...                                       
1         Natka    Berard  ... 2022-06-06 15:52:17.523585+00:00  None
2      Willetta   Goldina  ... 2022-06-06 15:52:17.523681+00:00  None
3         Eadie  Federica  ... 2022-06-06 15:52:17.523743+00:00  None
4      Genovera     Ailyn  ... 2022-06-06 15:52:17.523804+00:00  None
5      Christal     Wenda  ... 2022-06-06 15:52:17.523864+00:00  None
```

Turn the DataFrames back into entities
```python
members = Member.to_entities(df_members)
print(members)
```
```bash
[<Member: Member object (1)>, <Member: Member object (2)>,...]
```

## Related Sets

Prefetched relations can be joined at will
```Python
clubs = Club.objects.all().prefetch_related('membership_set')
df_clubs = Club.to_df(clubs, join_prefetch=['membership_set'])
print(df_clubs)
```
```python
    membership_set_id  ... college_id
0                   7  ...          2
1                  16  ...          2
2                  19  ...          2
3                  20  ...          2
4                  21  ...          2
```

Django-Frames can make the related sets more accessible in your code
```Python
clubs = Club.objects.all().prefetch_related('membership_set')  # prefetch the m2m relation
df_clubs = Club.to_df(clubs, join_prefetch=['membership_set'])  # join the cached objects
df_fox_club = df_clubs.loc[df_clubs.name == 'Fox Club']
df_fox_club = df_fox_club.assign(fee=25.66)
# deserialise the entities as the relation model intances 
memberships = Membership.to_entities(df_fox_club, pk='membership_set_id')
Membership.objects.bulk_update(memberships, fields=['fee'])
```

Frames include annotations as well
```Python
memberships = Membership.objects.all().annotate(club_name=F('club__name'))
df_memberships = Membership.to_df(memberships)
print(df_memberships)
```

```Python
                          join_date     level  ...   fee                   club_name
id                                             ...                                  
2  2022-06-08 18:47:35.890820+00:00  standard  ...  None                Delphic Club
3  2022-06-08 18:47:35.896090+00:00  standard  ...  None                the Delilahs
4  2022-06-08 18:47:35.900720+00:00  standard  ...  None  the Piers Gaveston Society
5  2022-06-08 18:47:35.906737+00:00  standard  ...  None                Delphic Club
6  2022-06-08 18:47:35.914585+00:00  standard  ...  None                Delphic Club
```


