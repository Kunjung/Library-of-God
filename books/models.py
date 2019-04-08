from django.db import models

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    name = models.CharField(max_length=64)
    summary = models.CharField(max_length=300)
    current_owner = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="ownedbooks")

    def __str__(self):
        return f"{self.name}"
