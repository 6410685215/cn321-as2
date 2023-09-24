from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.sign_in, name='login'),
]