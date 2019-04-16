import sys
import os
import django

sys.path.append("/c/Users/HP1/Desktop/Our Library Django/God's Library/libraryofgod")
os.environ['DJANGO_SETTINGS_MODULE'] = 'libraryofgod.settings'
django.setup()



########### START ####################
print("starting..................")
print("*****************************")
print("Deleting Previous Data")

from books.models import Person, Book, Wish

### DELETE ###
Person.objects.all().delete()
Book.objects.all().delete()
Wish.objects.all().delete()

print("Done Deleting ALL Data")

print("***************************")
print("Adding People:")
persons = ["Dolma", "Kunjung", "Mingmar", "Aagya", "Kushal", "Galileo"]

persons_list = []
for person in persons:
    p = Person(name=person)
    p.save()
    persons_list.append(p)

print("Done Loading People Data")
print("#######################################")

print("Adding Books")
books = ["Win Friends and Influence People",
        "Power of Habit",
        "Rich Dad Poor Dad",
        "Quiet",
        "Arthatantra",
        "All of me"
]
books_list = []
for i, book in enumerate(books):
    b = Book(name=book, owner=persons_list[i]) ## Set the ith book owner to the ith person
    b.save()
    books_list.append(b)

print("Done Loading Book Data")
print("#######################################")

print("Adding Wishes")
wish_orders = [
    (6, 2, 4),
    (5, 1, 6),
    (5, 4, 6),
    (1, 2, 3),
    (1, 2, 3),
    (1, 4, 5)
]

for i, wish_order in enumerate(wish_orders):
    wisher = persons_list[i]
    ### 3 wishes for everyone
    for rank, j in enumerate(wish_order):
        book = books_list[j-1]
        angel = book.owner
        wish = Wish(book=book, wisher=wisher, angel=angel, rank=rank+1)
        wish.save()

print("Done Adding Top 3 Wishes for everyone")
