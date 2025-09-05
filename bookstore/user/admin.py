from django.contrib import admin
from .models import Author, Book
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id','name','biography']
    list_display_links = ['name']
    search_fields = ['name']

class BookAdmin(admin.ModelAdmin):
    list_display = ['id','title','author','published_date','price','stock']
    list_display_links = ['title']
    search_fields = ['title']

admin.site.register(Author,AuthorAdmin)
admin.site.register(Book,BookAdmin)
