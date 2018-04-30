from django.db import models

# Create your models here.

class Account(models.Model):
    username = models.EmailField(primary_key=True)
    password = models.CharField(max_length=16, null=False)
    nickname = models.CharField(max_length=16, null=True)

class Label(models.Model):
    name = models.CharField(max_length=10, null=False)

class Article(models.Model):
    title = models.CharField(max_length=32, null=False)
    content = models.TextField(null=False)
    createDate= models.DateTimeField(auto_now_add=True)

    account = models.ForeignKey(to="Account",on_delete=True)

    labels = models.ManyToManyField(to="Label")

