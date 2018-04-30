from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from blog import views

urlpatterns = [
    url('^register/$', views.register),
    url('^login/$', views.login),
    url('^verification-code.html$', views.verification_code),
    url('^', views.index),
]