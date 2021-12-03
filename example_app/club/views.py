from django.shortcuts import render
from django.http import HttpResponse

def display_members(request):
    return HttpResponse("<h1>MyClub Event Calendar</h1>")