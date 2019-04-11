import sys
import os
import django

sys.path.append("/c/Users/HP1/Desktop/Our Library Django/God's Library/libraryofgod")
os.environ['DJANGO_SETTINGS_MODULE'] = 'libraryofgod.settings'
django.setup()


print("starting..................")
########### START ####################
from books.models import Person, Book

kunjung = Person(name="Kunjung")
mingmar = Person(name="Mingmar")
kunjung.save()
mingmar.save()

b1 = Book(name="Rich Dad Poor Dad", owner=mingmar)
b2 = Book(name="Power of Habit", owner=kunjung)
b3 = Book(name="Arthatantra", owner=kunjung)
b1.save()
b2.save()
b3.save()
print("Done Loading Dummy Data")
