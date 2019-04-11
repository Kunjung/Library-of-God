from django.contrib import admin

from .models import Book, Person, Wish

# Register your models here.

# class PersonAdmin(admin.ModelAdmin):
#     filter_horizontal = ("owned_books", )

admin.site.register(Book)

# admin.site.register(Person, PersonAdmin)
admin.site.register(Person)

admin.site.register(Wish)
