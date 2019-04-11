from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:book_id>', views.book, name='book'),
    path('person/<int:person_id>', views.person, name='person'),
    path('person/<int:person_id>/yourbooks', views.yourbooks, name='yourbooks'),
    path('person/<int:person_id>/addbook', views.addbook, name='addbook'),
    path('wishlist/<int:person_id>', views.wishlist, name='wishlist'),
    path('angel/<int:person_id>', views.angel, name='angel'),
]
