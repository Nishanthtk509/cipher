from django.db import models


class Signup(models.Model):

    username = models.CharField(
        max_length=100,
        unique=True
    )

    password = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.username




class Knowledge(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title


