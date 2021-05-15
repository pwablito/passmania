from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30)
    password_hash = models.CharField(max_length=30)
    password_salt = models.CharField(max_length=30)


class Password(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    service = models.CharField(max_length=100)


class TwoFactorCode(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
