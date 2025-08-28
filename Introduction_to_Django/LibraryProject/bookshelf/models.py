from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)  # Title field with max length of 200
    author = models.CharField(max_length=100)  # Author field with max length of 100
    publication_year = models.IntegerField()   # Integer field for publication year

    def __str__(self):
        return f"{self.title} by {self.author}"
