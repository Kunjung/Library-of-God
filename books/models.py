from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=20, default="Mr Nobody")

    def __str__(self):
        return f"Person {self.name}"

class Book(models.Model):
    name = models.CharField(max_length=20, default="Invisible Book")
    summary = models.TextField(max_length=100, null=True)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="books", null=True)

    def __str__(self):
        return f"Book {self.name}"
