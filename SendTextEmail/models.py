from django.db import models

class UserRegistration(models.Model):
    userID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=255)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username
