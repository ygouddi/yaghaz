from django.shortcuts import render, redirect



def under_construction(request):
    return render(request, 'construct.html')
