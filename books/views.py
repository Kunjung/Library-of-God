from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse


from .models import Person, Book, Wish

### The Matching Algorithm ###
from .algorithm_king_and_queen import begin_King_and_Queen_Match

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
		"books": person.books.all(),
		"wishes": person.wishes.all()
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
		person = Person.objects.get(pk=person_id)

		### LIMIT NUMBER OF BOOKS TO 1 for now - next feature will make it possible to add more books. But not now.
		if len(person.books.all()) >= 1:
			return render(request, "books/error.html", {"message": "Sorry You can only add 1 book right now. You will be able to add more books in the next feature only."})

		name = request.POST["name"]
		summary = request.POST["summary"]

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
		"available_ranks": [ rank for rank in [1, 2] if rank not in wished_ranks ],
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


def yourmatches(request, person_id):
	try:
		person = Person.objects.get(pk=person_id)
		mybook = person.books.all().first()

	except Person.DoesNotExist:
		raise Http404("Person does not exist.")
	except Book.DoesNotExist:
		raise Http404("Book does not exist.")

	context = {
		"person": person,
		"mybook": mybook,
		"matched_wishes": person.wishes.filter(fulfilled=True)
	}
	return render(request, "books/yourmatches.html", context)


#############################################################################################
################# King and Queen Matching View  ###########################################
def match(request):

	all_books = Book.objects.filter(available=True)		### All books will be kings and queens at the same time. They'll have the rank order of last for themselves
	faces = [book.id for book in all_books]			### For now just check on the book names. later find the book id, okay. bro
	all_king_preferences = []

	for book in all_books:
		king_preference = []
		wishes = book.owner.wishes.filter(fulfilled=False).order_by('rank')
		queen_books = [wish.book.id for wish in wishes]
		for queen_book in queen_books:
			king_preference.append(queen_book)
		remaining_books = Book.objects.exclude(id__in=king_preference).exclude(id__in=[book.id])
		for r_book in remaining_books:
			king_preference.append(r_book.id)

		### Adding yourself to the very end for the non match
		king_preference.append(book.id)

		### ADDING king_preference of book b[i]
		all_king_preferences.append(king_preference)

	### Now change all the king preferences from being strings to being indexes based on the faces list
	all_king_preferences_indexed = []
	for king_preference in all_king_preferences:
		king_preference_indexed = [faces.index(king_p) for king_p in king_preference]
		all_king_preferences_indexed.append(king_preference_indexed)


	### King and Queen preferences are the same for the same book
	matches = begin_King_and_Queen_Match(faces, king_preferences=all_king_preferences_indexed, queen_preferences=all_king_preferences_indexed)
	info_matches = []
	for (king, queen) in matches:
		king_book = Book.objects.get(pk=king)
		queen_book = Book.objects.get(pk=queen)
		king_owner = king_book.owner
		queen_owner = queen_book.owner
		info_match = f"{king_book} (Person: {king_owner}) --------> matched to ---------> {queen_book} (Person: {queen_owner}) "
		info_matches.append(info_match)

	context = {
		"matches": info_matches
	}

	return render(request, "books/match.html", context)
