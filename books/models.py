from django.db import models

# Create your models here.


class Person(models.Model):
    username = models.CharField(max_length=32, null=True)
    first = models.CharField(max_length=15, null=True)
    last = models.CharField(max_length=15, null=True)

    # phone = models.CharField(max_length=11)
    # email = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first} {self.last}"


class Book(models.Model):
    name = models.CharField(max_length=64)
    summary = models.TextField(max_length=300, null=True)
    current_owner = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="ownedbooks")

    def __str__(self):
        return f"{self.name}"
