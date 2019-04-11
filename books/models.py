from django.db import models

# Create your models here.

class P(models.Model):
    name = models.CharField(max_length=8)

    def __str__(self):
        return f"Person {self.name}"

class B(models.Model):
    name = models.CharField(max_length=8)
    owner = models.ForeignKey(P, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return f"Book {self.name}"
