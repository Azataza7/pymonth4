import datetime
from django.shortcuts import render, HttpResponse


# Create your views here.

def general_page(request):
    return HttpResponse(datetime.datetime.now())


def about_us_view(request):
    return render(request, 'about_us.html')

