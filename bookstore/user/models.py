from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=300)
    biography = models.TextField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(Author, to_field='id', on_delete=models.CASCADE)
    published_date = models.DateField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    class Meta:
        permissions = [
            ("can_add_book","Can Add Book"),
            ("can_update_book","Can Update Book"),
            ("can_delete_book","Can Delete Book")
        ]
    

""" Activation Model """

class ActivationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

