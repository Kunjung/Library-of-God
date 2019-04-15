from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse


from .models import Person, Book, Wish

# Create your views here.

## Index Page shows all the books that have the Field value of "Available" = True
def index(request):
	context = {
		"books": Book.objects.filter(available=True)
	}
	return render(request, "books/index.html", context)


## Show details of a Particular Book
def book(request, book_id):
	try:
		book = Book.objects.get(pk=book_id)
	except Book.DoesNotExist:
		raise Http404("Book does not exist.")

	context = {
		"book": book
	}
	return render(request, "books/book.html", context)

## Show details of a Particular Person
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

## Show all the books of a particular Person
def yourbooks(request, person_id):
	try:
		person = Person.objects.get(pk=person_id)
	except Person.DoesNotExist:
		raise Http404("Person does not exist.")

	context = {
		"person": person,
		"books": person.books.all()
	}
	return render(request, "books/yourbooks.html", context)

## Let a person add new books
def addbook(request, person_id):
	try:
		name = request.POST["name"]
		summary = request.POST["summary"]

		person = Person.objects.get(pk=person_id)
	except KeyError:
		return render(request, "books/error.html", {"message": "No selection."})
	except Person.DoesNotExist:
		return render(request, "books/error.html", {"message": "No person."})
	except:
		return render(request, "books/error.html", {"message": "Unknown Error"})

	new_book = Book(name = name, summary = summary, owner = person)
	new_book.save()

	return HttpResponseRedirect(reverse("yourbooks", args=(person_id,) ))

## Show all the wishes of a particular person
def wishlist(request, person_id):
	try:
		person = Person.objects.get(pk=person_id)
	except Person.DoesNotExist:
		raise Http404("Person does not exist.")

	context = {
		"person": person,
		"wishes": person.wishes.all().order_by('rank')
	}
	return render(request, "books/wishlist.html", context)

## Show all the wishes to be fulfilled by a Particular Person
def angel(request, person_id):
	try:
		person = Person.objects.get(pk=person_id)
	except Person.DoesNotExist:
		raise Http404("Person does not exist.")

	context = {
		"person": person,
		"wishes_to_fulfill": person.wishes_to_fulfill.all().order_by('rank')
	}
	return render(request, "books/angel.html", context)


## Show all the wishes of a particular person
def yourwishes(request, person_id):
	try:
		person = Person.objects.get(pk=person_id)
		book_id_list = [book.id for book in person.books.all()]
		wish_book_id_list = [wish.book.id for wish in person.wishes.all()]

		wished_ranks = [wish.rank for wish in person.wishes.all()]

	except Person.DoesNotExist:
		raise Http404("Person does not exist.")

	context = {
		"person": person,
		"wishes": person.wishes.all(),
		"available_ranks": [ rank for rank in [1, 2, 3, 4, 5, 6, 7] if rank not in wished_ranks ],
		"newbooks": Book.objects.exclude(id__in = book_id_list).exclude(id__in = wish_book_id_list).all()
	}
	return render(request, "books/yourwishes.html", context)

def addwish(request, person_id):
	try:
		book_id = request.POST["book_id"]
		rank = int(request.POST["rank"])

		book = Book.objects.get(pk=book_id)
		wisher = Person.objects.get(pk=person_id)

		angel_id = book.owner.id
		angel = Person.objects.get(pk=angel_id)

	except KeyError:
		return render(request, "books/error.html", {"message": "No selection."})
	except Person.DoesNotExist:
		return render(request, "books/error.html", {"message": "No wish maker or angel to fulfill the wish. God is Dead."})
	except Book.DoesNotExist:
		return render(request, "books/error.html", {"message": "No book."})
	except:
		return render(request, "books/error.html", {"message": "Unknown Error"})

	new_wish = Wish(book = book, wisher = wisher, rank = rank, angel=angel)
	new_wish.save()

	return HttpResponseRedirect(reverse("yourwishes", args=(person_id,) ))
