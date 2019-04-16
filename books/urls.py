from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:book_id>', views.book, name='book'),

    path('person/<int:person_id>', views.person, name='person'),
    path('person/<int:person_id>/yourbooks', views.yourbooks, name='yourbooks'),
    path('person/<int:person_id>/addbook', views.addbook, name='addbook'),          ### DON'T use this right now when only one person one book
    path('person/<int:person_id>/yourwishes', views.yourwishes, name='yourwishes'),
    path('person/<int:person_id>/addwish', views.addwish, name='addwish'),

    path('person/<int:person_id>/yourmatches', views.yourmatches, name='yourmatches'),

    path('match', views.match, name='match'),
]
