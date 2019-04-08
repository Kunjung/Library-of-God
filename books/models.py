from django.db import models

# Create your models here.


## Trying the Many to Many relationship
class Book(models.Model):
    name = models.CharField(max_length=64)
    summary = models.TextField(max_length=300, null=True)

    def __str__(self):
        return f"{self.name}"


class Person(models.Model):
    username = models.CharField(max_length=32, null=True)
    first = models.CharField(max_length=15, null=True)
    last = models.CharField(max_length=15, null=True)
    owned_books = models.ManyToManyField(Book, blank=True, related_name='owners')

    # phone = models.CharField(max_length=11)
    # email = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first} {self.last}"


## Old DataBase Models for the One to many relationship.
## I can query the database fine. But querying like this:
## Books.objects.filter(current_owner=p) is gonna be a lot a lot of waste of db
## also i can't easily see what books a single person owns easily in the admin page

# class Person(models.Model):
#     username = models.CharField(max_length=32, null=True)
#     first = models.CharField(max_length=15, null=True)
#     last = models.CharField(max_length=15, null=True)
#
#     # phone = models.CharField(max_length=11)
#     # email = models.CharField(max_length=20)
#
#     def __str__(self):
#         return f"{self.first} {self.last}"
#
#
# class Book(models.Model):
#     name = models.CharField(max_length=64)
#     summary = models.TextField(max_length=300, null=True)
#     current_owner = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="ownedbooks")
#
#     def __str__(self):
#         return f"{self.name}"
