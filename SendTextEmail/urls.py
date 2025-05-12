from django.urls import path
from views import send_text_email
urlpatterns = [
    path('sendTextEmail/', views.sendTextEmail, name='sendTextEmail'),
]
