from django.contrib import admin
from .models import Genre, Book, Comment

admin.site.register([Genre, Book, Comment])
