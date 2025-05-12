from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('sendTextEmail/', views.send_text_email, name='sendTextEmail'),
]
