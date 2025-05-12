import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage, send_mail
from dotenv import load_dotenv

load_dotenv()

# Create your views here.
def index(request):
    return HttpResponse("<h1>Welcome to Learning!</h1><h3>This is a simple email sending app</h3>")

def send_text_email(request):
    try:
        send_mail(
            'Welcome to Learning!',
            'This email is sent for testing the Django application',
            'parasmunoli@gmail.com',
            ['sumitmunoli789@gmail.com'],
            fail_silently=False,
            auth_password=os.getenv('HOST_EMAIL_PASSWORD'),
        )
        return HttpResponse("<h1>Email sent successfully!</h1>")
    except Exception as e:
        print(f'Email sending failed: {e}')
        return HttpResponse("Failed to send email")