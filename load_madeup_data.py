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
kunjung = Person(name="Kunjung")
mingmar = Person(name="Mingmar")
aagya = Person(name="Aagya")
kushal = Person(name="Kushal")

kunjung.save()
mingmar.save()
aagya.save()
kushal.save()


print("Done Loading People Data")
print("#######################################")

print("Adding Books")
b1 = Book(name="Rich Dad Poor Dad", owner=mingmar)
b2 = Book(name="Reality is Broken", owner=kunjung)
b3 = Book(name="Man's Search for Meaning", owner=aagya)
b4 = Book(name="Subtle Art of not giving a F**k", owner=kushal)

b1.save()
b2.save()
b3.save()
b4.save()

print("Done Loading Book Data")
print("#######################################")

print("Adding Wishes")
## Kunjung Ranks Rich Dad Poor Dad
w1 = Wish(book=b1, wisher=kunjung, angel=b1.owner)
w1.save()

## Mingmar wishes Reality is Broken
w2 = Wish(book=b2, wisher=mingmar, angel=b2.owner)
w2.save()

## Aagya wishes for Reality is Broken
w3 = Wish(book=b2, wisher=aagya, angel=b2.owner)
w3.save()


## Kushal wishes for Man's Search for Meaning
w4 = Wish(book=b3, wisher=kushal, angel=b3.owner)
w4.save()
