from django.shortcuts import render
from django.http import HttpResponse, Http404


from .models import Person, Book

# Create your views here.
def index(request):
    context = {
        "books": Book.objects.all()
    }
    return render(request, "books/index.html", context)


def book(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist.")

    context = {
        "book": book
    }
    return render(request, "books/book.html", context)


def person(request, person_id):
    try:
        person = Person.objects.get(pk=person_id)
    except Person.DoesNotExist:
        raise Http404("Person does not exist.")

    context = {
        "person": person,
        "books": person.books.all()
    }
    return render(request, "books/person.html", context)


def wishlist(request, person_id):
    try:
        person = Person.objects.get(pk=person_id)
    except Person.DoesNotExist:
        raise Http404("Person does not exist.")

    context = {
        "person": person,
        "wishes": person.wishes.all()
    }
    return render(request, "books/wishlist.html", context)
