from django.urls import path
from views import send_email

path('sendTextEmail/', views.sendTextEmail, name='sendTextEmail')