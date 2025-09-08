from django.contrib import admin
from .models import Author, Book, ActivationToken
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id','name','biography']
    list_display_links = ['name']
    search_fields = ['name']

class BookAdmin(admin.ModelAdmin):
    list_display = ['id','title','author','published_date','price','stock']
    list_display_links = ['title']
    search_fields = ['title']

class ActivationTokenAdmin(admin.ModelAdmin):
    list_display = ['user','token','created_at']
    list_display_links = ['user']
    search_fields = ['user']

admin.site.register(Author,AuthorAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(ActivationToken, ActivationTokenAdmin)
