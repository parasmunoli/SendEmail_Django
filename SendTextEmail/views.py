import os
from django.shortcuts import render
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.http import HttpResponse
from dotenv import load_dotenv

load_dotenv()


def index(request):
    return HttpResponse("<h1>Welcome to Learning!</h1><h3>This is a simple email sending app</h3>")

def signup(request):
    # Render the signup form (signup.html)
    return render(request, "SendTextEmail/signup.html")

def send_text_email(request):
    if request.method == "POST":
        senderEmail = os.getenv('HOST_EMAIL_USER')
        appPassword = os.getenv('HOST_EMAIL_PASSWORD')
        receiverEmail = request.POST['email']
        message = MIMEMultipart()
        message['From'] = senderEmail
        message['To'] = receiverEmail
        message['Subject'] = "Welcome to Learning!"
        body = "This email is sent using EmailMessage in Django."
        message.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(senderEmail, appPassword)

            server.sendmail(senderEmail, receiverEmail, message.as_string())
            server.quit()

            return HttpResponse("<h1>Email sent successfully!</h1>")

        except Exception as e:
            print(f"Email sending failed: {e}")
            return HttpResponse(f"<h1>Failed to send email: {e}</h1>")

    return HttpResponse("<h1>Invalid Method</h1>")
