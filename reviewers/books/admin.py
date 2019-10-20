from django.contrib import admin
from .models import Book, Author, Review

admin.site.register([Author, Book, Review])
