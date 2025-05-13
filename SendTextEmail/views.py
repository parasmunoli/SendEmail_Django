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
        receiverEmail = request.POST.get('email')
        
        if not receiverEmail:
            return HttpResponse("<h1>Error: No email address provided</h1>")
            
        print(receiverEmail)
        message = MIMEMultipart()
        message['From'] = f'Support Team {senderEmail}'
        message['To'] = receiverEmail
        message['Subject'] = "Welcome to Learning!"
        body = "This email is sent using EmailMessage in Django."
        message.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.login(senderEmail, appPassword)
            server.sendmail(senderEmail, receiverEmail, message.as_string())
            server.quit()

            return HttpResponse("<h1>Email sent successfully!</h1>")

        except smtplib.SMTPAuthenticationError:
            error_msg = "Failed to authenticate with email server. Please check credentials."
            print(error_msg)
            return HttpResponse(f"<h1>{error_msg}</h1>")
        except smtplib.SMTPException as e:
            error_msg = f"SMTP error occurred: {str(e)}"
            print(error_msg)
            return HttpResponse(f"<h1>{error_msg}</h1>")
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(error_msg)
            return HttpResponse(f"<h1>{error_msg}</h1>")

    return HttpResponse("<h1>Invalid Method</h1>")