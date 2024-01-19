"""
URL configuration for studypeople project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # include for views.py routes

# from django.http import HttpResponse

# Best to have views in app's views.py file
# def home(request):
#     # Request is an http object, what user is sending to backend
#     return HttpResponse("Home Page")


# def room(request):
#     return HttpResponse("ROOM")


urlpatterns = [path("admin/", admin.site.urls), path("", include("base.urls"))]
