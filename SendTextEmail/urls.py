from django.urls import path
from views import send_text_email

path('sendTextEmail/', views.sendTextEmail, name='sendTextEmail')