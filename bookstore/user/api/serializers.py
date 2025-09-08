from rest_framework import serializers
from user.models import Book, Author, ActivationToken


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'
        include = ['books']


class BookSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(queryset=Author.objects.all(), slug_field='name')

    class Meta:
        model = Book
        fields = '__all__'


class ActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivationToken
        fields = '__all__'

