from rest_framework import serializers
from user.models import Book, Author, ActivationToken




class BookSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(queryset=Author.objects.all(), slug_field='name')

    class Meta:
        model = Book
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id','name','biography','books']

class ActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivationToken
        fields = '__all__'

