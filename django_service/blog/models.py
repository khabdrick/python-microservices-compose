from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    details = models.CharField(max_length=2000)
    timestamp  = models.DateTimeField()
    likes = models.PositiveIntegerField(default=0)


class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True, editable=True)
