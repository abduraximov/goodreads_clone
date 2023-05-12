from django.contrib import admin
from .models import Book, Author, BookAuthor, BookReview

class BookModel(admin.ModelAdmin):
    search_fields = ('title', 'description', 'isbn')
    list_display = ('title','isbn', 'description')

admin.site.register(Book, BookModel)
admin.site.register(Author)
admin.site.register(BookAuthor)
admin.site.register(BookReview)