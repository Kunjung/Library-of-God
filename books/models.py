from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=20, default="Mr Nobody")

    def __str__(self):
        return f"{self.name}"

class Book(models.Model):
    name = models.CharField(max_length=20, default="Invisible Book")
    summary = models.TextField(max_length=100, null=True)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="books", null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

class Wish(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="wishes")
    wisher = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="wishes") ### The Person who is making the wish
    angel = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='wishes_to_fulfill', null=True) ### The Person who fulfills the wish therefore, the ANGEL

    fulfilled = models.BooleanField(default=False)
    rank = models.IntegerField(default=1)  ### The Number One Book

    def __str__(self):
        return f"{self.wisher} wants '{self.book}' from {self.angel}"
