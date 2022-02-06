from django.shortcuts import render
from django.http import HttpResponse

def display_members(request):
    return HttpResponse("<h1>Members</h1>")

def display_club(request):
    return HttpResponse("<h1>Clubs</h1>")
