from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('allexchanges', views.allexchanges, name='allexchanges'),

    path('book/<int:book_id>', views.book, name='book'),

    path('person/<int:person_id>', views.person, name='person'),
    path('person/<int:person_id>/yourbooks', views.yourbooks, name='yourbooks'),
    path('person/<int:person_id>/changebookavailability', views.changebookavailability, name='changebookavailability'),
    # path('person/<int:person_id>/addbook', views.addbook, name='addbook'),          ### DON'T use this right now when only one person one book
    path('person/<int:person_id>/yourwishes', views.yourwishes, name='yourwishes'),
    path('person/<int:person_id>/addwish', views.addwish, name='addwish'),

    path('person/<int:person_id>/yourmatches', views.yourmatches, name='yourmatches'),
    path('person/<int:person_id>/yourexchanges', views.yourexchanges, name='yourexchanges'),

    path('match', views.match, name='match'), ##### Triggers the KING QUEEN matching ALGORITHM. Only works once the available books is 2/3 * Total books
]
