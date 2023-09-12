from django.shortcuts import render,redirect
from app01 import models

def city_list(request):
    queryset = models.City.objects.all()
    return render(request,'city_list.html',{"queryset":queryset})


def city_add(request):
    return redirect("/upload/modelform/")