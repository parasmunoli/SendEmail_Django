import os
import random
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from django.http import HttpResponse
from django.shortcuts import render, redirect
from email.mime.multipart import MIMEMultipart
from django.contrib.auth.models import User

load_dotenv()

def index(request):
    return HttpResponse("<h1>Welcome to Learning!</h1><h3>This is a simple email sending app</h3>")

def signup(request):
    # Render the signup form (signup.html)
    return render(request, "SendTextEmail/signup.html")

def validate_password(password, confirm_password):
    if password != confirm_password:
        return False
    else:
        return True

def validateOTP(request):
    if request.method == "POST":
        user_otp = request.POST.get('user_otp')
        session_otp = request.session.get('otp')

        if not user_otp:
            return render(request, "SendTextEmail/otpfill.html", {'error_message': 'Please enter OTP'})

        if not session_otp:
            return render(request, "SendTextEmail/otpfill.html", {'error_message': 'Session expired. Please try again'})

        if user_otp == session_otp:
            # OTP matches, proceed with registration/login
            email = request.session.get('email')
            username = request.session.get('username')
            phone = request.session.get('phone')
            gender = request.session.get('gender')
            password = request.session.get('password')

            user = User.objects.create_user(username=username, email=email, password=password, phone=phone, gender=gender)
            user.save()

            for key in ['otp', 'email', 'username', 'phone', 'gender', 'password']:
                if key in request.session:
                    del request.session[key]

            return HttpResponse("<h1>Registration Successful!</h1><p>You have been registered successfully.</p>")
        else:
            return render(request, "SendTextEmail/otpfill.html", {'error_message': 'Invalid OTP. Please try again'})

    return redirect('signup')

def send_text_email(request):
    if request.method == "POST":
        senderEmail = os.getenv('HOST_EMAIL_USER')
        appPassword = os.getenv('HOST_EMAIL_PASSWORD')

        receiverEmail = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')

        if not receiverEmail:
            return HttpResponse("<h1>Error: No email address provided</h1>")

        if not validate_password(password, confirm_password):
            return HttpResponse("<h1>Error: Passwords do not match</h1>")

        otp = random.randint(100000, 999999)

        request.session['otp'] = str(otp)
        request.session['email'] = receiverEmail
        request.session['username'] = username
        request.session['phone'] = phone
        request.session['gender'] = gender
        request.session['password'] = password

        # Compose Email
        message = MIMEMultipart()
        message['From'] = f'Support Team <{senderEmail}>'
        message['To'] = receiverEmail
        message['Subject'] = "Your OTP Code"
        body = f"Thank you for signing up! Your OTP is {otp}"
        message.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(senderEmail, appPassword)
            server.sendmail(senderEmail, receiverEmail, message.as_string())
            server.quit()

            return render(request, "SendTextEmail/otpfill.html")  # Make sure this template exists
        except smtplib.SMTPAuthenticationError:
            return HttpResponse("<h1>SMTP Authentication Error. Check credentials.</h1>")
        except Exception as e:
            return HttpResponse(f"<h1>Unexpected Error: {e}</h1>")

    return HttpResponse("<h1>Invalid Method</h1>")