import time

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse


from .models import Person, Book, Wish, Exchange

# The Matching Algorithm #
from .algorithm_king_and_queen import begin_King_and_Queen_Match
# from .order_nlp import order_remaining_wishes

# Create your views here.

## Index Page shows all the books that have the Field value of "Available" = True
def index(request):
    context = {
        "books": Book.objects.all(),
        "book_number": len(Book.objects.all()),
        "people_number": len(Person.objects.all())
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
        "wishes": person.wishes.all(),
        "matched_wishes": person.wishes.filter(fulfilled=True)
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
        "books": person.books.all(),
    }
    return render(request, "books/yourbooks.html", context)

def changebookavailability(request, person_id):
    try:
        book_id = int(request.POST["book_id"])
        book_available = request.POST.get("available", False)
        book = Book.objects.get(pk=book_id)
        person = Person.objects.get(pk=person_id)
        book_available = bool(book_available)

        if book.owner != person:
            return render(request, "books/error.html", {"message": "Can't change someone else's book Boy or Girl."})

        # STOP if the book is waiting to be exchanged
        # Here the condition will be true when The Exchange object for the person has been created and the meeting is False
        # and also when the wish object is there where the Wish.angel is the person and fulfilled = True
        wish2fulfill = person.wishes_to_fulfill.filter(book=book).filter(fulfilled=True)
        if len(wish2fulfill) >= 1:
            message = "Can't change the availability now. You fulfilled the wish and The Book is waiting to be exchanged to someone else."
            return render(request, "books/error.html", {"message": message})

    except KeyError:
        # available = request.POST["available"]
        message = "Key Error " + str(book_available)
        print(message)
        return render(request, "books/error.html", {"message": message})
    except Person.DoesNotExist:
        return render(request, "books/error.html", {"message": "No person."})
    except Book.DoesNotExist:
        return render(request, "books/error.html", {"message": "No book."})
    except:
        return render(request, "books/error.html", {"message": "Unknown Error"})
    book.available = book_available
    book.save()
    return HttpResponseRedirect(reverse("yourbooks", args=(person_id,) ))

# Show all the wishes of a particular person
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
        "available_ranks": [ rank for rank in [1, 2, 3] if rank not in wished_ranks ],
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

def allexchanges(request):
    exchanges = Exchange.objects.filter(kingmeeting=False)

    context = {
        "exchanges": exchanges,
    }
    return render(request, "books/allexchanges.html", context)

def yourexchanges(request, person_id):
    try:
        person = Person.objects.get(pk=person_id)
        exchanges = Exchange.objects.filter(king=person)
    except Person.DoesNotExist:
        raise Http404("Person does not exist.")
    except Exchange.DoesNotExist:
        raise Http404("Exchange does not exist.")

    context = {
        "person": person,
        "exchanges": exchanges,
    }
    return render(request, "books/yourexchanges.html", context)


# King and Queen Matching View
def match(request):
    match_time_start = time.time()

    complete_book_collection = Book.objects.all()
    # All books will be kings and queens at the same time.
    # They'll have the rank order of last for themselves
    all_books = Book.objects.filter(available=True)
    ## Trigger King Queen Matching Algorithm only when available books is at least 2/3 of all complete book collection
    ## Stop it if it fails the Condition #1.
    if len(all_books) < 2:
        message = "Algorithm not ready. Total Book Number: " + str(len(complete_book_collection)) + " .  Available Book Number: " + str(len(all_books))
        return render(request, "books/error.html", {"message": message})


    ## STOP CONDITION #2. Stop King Queen Match when not enough wishes are made.
    ## Every person should make at least 3 wishes. Otherwise, don't run algorithm
    all_persons = Person.objects.all()
    STOP = False
    for person in all_persons:
        if len(person.wishes.all()) < 2:
            STOP = True
            break

    if STOP == True:
        message = "Algorithm not ready. Not enough wishes have been made so far."
        return render(request, "books/error.html", {"message": message})

    # All books will be kings and queens at the same time.
    # They'll have the rank order of last for themselves
    all_books_dict = {}
    for book in all_books:
        all_books_dict[book.name] = book
    all_books_name = [book for book in all_books_dict.keys()]
    # For now just check on the book names. later find the book id, okay. bro
    faces = [book.id for book in all_books]
    all_king_preferences = []

    for book in all_books:
        start_time = time.time()

        all_books_name_copy = list(all_books_name)
        all_books_name_copy.remove(book.name)
        king_preference = []
        wishes = book.owner.wishes.filter(fulfilled=False).order_by('rank')
        queen_books = [wish.book.id for wish in wishes]
        for queen_book in queen_books:
            king_preference.append(queen_book)

        # Make sure the remaining_books is ordered intelligently
        wished_books = [wish.book.name for wish in wishes]
        
        remaining_books = all_books_name_copy[:]
        for wished_book in wished_books:
            try:
                remaining_books.remove(wished_book)
            except Exception as e:
                print(e)

        ## remaining_books = order_remaining_wishes(wished_books, all_books_name_copy)
        for remaining_book in remaining_books:
            # book = Book.objects.get(name=r_book)
            r_book = all_books_dict[remaining_book]
            king_preference.append(r_book.id)

        # Adding yourself to the very end for the non match
        king_preference.append(book.id)

        # ADDING king_preference of book b[i]
        all_king_preferences.append(king_preference)
        end_time = time.time()
        print("Single book time: ", end_time-start_time)

    # Now change all the king preferences from being strings to being indexes based on the faces list
    all_king_preferences_indexed = []
    for king_preference in all_king_preferences:
        king_preference_indexed = [faces.index(king_p) for king_p in king_preference]
        all_king_preferences_indexed.append(king_preference_indexed)

    # King and Queen preferences are the same for the same book
    matches = begin_King_and_Queen_Match(faces, king_preferences=all_king_preferences_indexed, queen_preferences=all_king_preferences_indexed)
    info_matches = []
    for (king_id, queen_id) in matches:
        king_book = Book.objects.get(pk=king_id)
        queen_book = Book.objects.get(pk=queen_id)
        king_owner = king_book.owner
        queen_owner = queen_book.owner
        match_info = [king_owner, king_book, queen_owner, queen_book]
        info_matches.append(match_info)

    # Set all the kings wishes to fulfilled = True
    for (king_id, queen_id) in matches:
        king_book = Book.objects.get(pk=king_id)
        queen_book = Book.objects.get(pk=queen_id)
        king = king_book.owner
        queen = queen_book.owner

        # The queen's book is what is being wished for, the king makes the wish so he is the wisher and the queen is the angel
        king_wish = Wish.objects.filter(book=queen_book, wisher=king, angel=queen).first()
        if king_wish:
            king_wish.fulfilled = True
            king_wish.save()

            # Now the queen's book becomes not available for anyone else. It is married now.
            queen_book.available = False
            queen_book.save()

        else:
            new_king_wish = Wish(book=queen_book, wisher=king, angel=queen, fulfilled=True)
            new_king_wish.save()
            queen_book.available = False
            queen_book.save()

        # For each king and queen pair, now make the exchange objects and set the meeting value to false
        exchange = Exchange(
            king=king, queen=queen, kingmeeting=False, queenmeeting=False,
            kingbook=king_book, queenbook=queen_book
        )
        exchange.save()

    context = {
        "matches": info_matches
    }
    match_time_end = time.time()
    print("match time: ", match_time_end - match_time_start)
    return render(request, "books/match.html", context)


def meeting_done(request, person_id):
    person = Person.objects.get(pk=person_id)

    exchange_id = int(request.POST["exchange_id"])
    meeting = request.POST.get("meeting", False)
    exchange = Exchange.objects.get(pk=exchange_id)

    meeting = bool(meeting)

    if exchange.king != person:
        return render(request, "books/error.html", {"message": "Can't change someone else's meeting."})

    # CHeck if the anti exchange pair is available
    anti_exchange = Exchange.objects.filter(queen=person).first()

    print(anti_exchange)
    # IF anti exchange pair is found, then set queen meeting of this exchange to True
    if anti_exchange:
        exchange.kingmeeting = meeting
        exchange.save()

        anti_exchange.queenmeeting = meeting 		# The anti exchange pairs queen has also done the meeting
        anti_exchange.save()

        # see if the king meeting for the anti exchange pair is True and the
        # king meeting for the current exchange pair is True
        # This is the condition for when there both have confirmed that they've made the exchange
        if anti_exchange.kingmeeting == True and exchange.kingmeeting == True:

            ## Find the anti person that is the queen for the exchange
            anti_person = exchange.queen

            exchange.queenmeeting = True 	# and set queen meeting of that exchange to True too
            anti_exchange.queenmeeting	= True # same for the anti exchange

            # Delete The wish of the person for the books on both sides
            anti_person.wishes.all().delete()
            person.wishes.all().delete()

            anti_person.save()
            person.save()

            # Change Ownership of the books
            particle_book = person.books.first()
            anti_particle_book = anti_person.books.first()

            particle_book.owner = anti_person
            anti_particle_book.owner = person

            # Set the exchanged books to unavailable for now
            particle_book.available = False
            anti_particle_book.available = False

            particle_book.save()
            anti_particle_book.save()

    else:
        return render(request, "books/error.html", {"message": "Couldn't find the exchange pair"})
    return HttpResponseRedirect(reverse("yourexchanges", args=(person_id,)))
