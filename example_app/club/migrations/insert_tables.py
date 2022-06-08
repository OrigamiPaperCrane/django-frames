import pytz
from django.db import migrations, models
import django.db.models.deletion
import pandas as pd
import os
from datetime import datetime
from club.models import *
from example_app.settings import BASE_DIR


def insert_clubs(*args, **kwargs):
    df_clubs = pd.read_csv(os.path.join(BASE_DIR,'fixtures', 'clubs.csv'))
    clubs = []
    for c in df_clubs.itertuples():
        clubs.append(Club(name=c.name,
                          creation_date=pytz.utc.localize(datetime.utcnow()),
                          founding_date=datetime.strptime(c.founding_date, '%Y-%m-%d'),
                          invitation_only=c.invitation_only)
                     )
    Club.objects.bulk_create(clubs)

def insert_colleges(*args, **kwargs):
    df_colleges = pd.read_csv(os.path.join(BASE_DIR,'fixtures', 'colleges.csv'))
    colleges = []
    for c in df_colleges.itertuples():
        colleges.append(College(name=c.name))
    College.objects.bulk_create(colleges)

def insert_members(*args, **kwargs):
    df_members = pd.read_csv(os.path.join(BASE_DIR,'fixtures', 'members0.csv'))
    members = []
    for m in df_members.itertuples():
        members.append(Member(first_name=m.firstname,
                              last_name=m.lastname,
                              email=m.email,
                              occupation=m.profession))
    Member.objects.bulk_create(members)

def insert_roles(*args, **kwargs):
    df_roles = pd.read_csv(os.path.join(BASE_DIR,'fixtures', 'roles.csv'))
    roles = []
    for r in df_roles.itertuples():
        roles.append(Role(name=r.name))
    Role.objects.bulk_create(roles)



class Migration(migrations.Migration):

    dependencies = [
        ('club', '0003_auto_20220606_1533'),
    ]

    operations = [
        migrations.RunPython(insert_roles),
        migrations.RunPython(insert_colleges),
        migrations.RunPython(insert_clubs),
        migrations.RunPython(insert_members)
    ]