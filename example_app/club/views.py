import random
from datetime import datetime
import pandas as pd
import pytz
from django.db.models import Min, F
from django.shortcuts import render
from django.http import HttpResponse

from club.models import Member, Club, Membership


def display_members(request):
    members = Member.objects.all()
    df_members = Member.to_df(members)
    print(df_members)
    print(Member.to_entities(df_members))
    return HttpResponse("<h1>Members</h1>")

def display_clubs(request):
    clubs = Club.objects.all().prefetch_related('membership_set')
    df_clubs = Club.to_df(clubs, join_prefetch=['membership_set'])
    df_fox_club = df_clubs.loc[df_clubs.name == 'Fox Club']
    print(df_fox_club)
    df_fox_club = df_fox_club.assign(fee=25.66)
    memberships = Membership.to_entities(df_fox_club, pk='membership_set_id')
    Membership.objects.bulk_update(memberships, fields=['fee'])
    return HttpResponse("<h1>Clubs</h1>")

def set_memberships(request):
    members = Member.objects.all()
    clubs_list = [c for c in Club.objects.all()]
    for member in members:
        member.memberships.add(random.choice(clubs_list))
    return HttpResponse(status=200)

def display_memberships(request):
    memberships = Membership.objects.all().annotate(club_name=F('club__name'))
    df_memberships = Membership.to_df(memberships)
    print(df_memberships)
    return HttpResponse("<h1>memberships</h1>")