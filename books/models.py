from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=20, default="Mr Nobody")
    photo = models.FileField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)

class Book(models.Model):
    name = models.CharField(max_length=20, default="Invisible Book")
    summary = models.TextField(max_length=100, null=True)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="books", null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return "{}".format(self.name)

class Wish(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="wishes")
    wisher = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="wishes") ### The Person who is making the wish
    angel = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='wishes_to_fulfill', null=True) ### The Person who fulfills the wish therefore, the ANGEL

    fulfilled = models.BooleanField(default=False)
    rank = models.IntegerField(default=1)  ### The Number One Book

    def __str__(self):
        return "{} wants {} from {}".format(
            self.wisher, self.book, self.angel
        )


class Exchange(models.Model):
    king = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="king_exchanges")
    queen = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="queen_exchanges")

    kingbook = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="kingbook_exchanges", null=True)
    queenbook = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="queenbook_exchanges", null=True)

    kingmeeting = models.BooleanField(default=False)
    queenmeeting = models.BooleanField(default=False)

    def __str__(self):
        return "{} should meet {} in person. King Met? {}. Queen Met? {}".format(
            self.king, self.queen, self.kingmeeting, self.queenmeeting
        )
