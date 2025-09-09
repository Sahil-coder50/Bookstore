from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from user.models import Book, Author, ActivationToken
from user.api.serializers import BookSerializer, AuthorSerializer

from django.shortcuts import get_object_or_404

class Book_List_View(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            books = Book.objects.all()
        except Book.DoesNotExist:
            return Response({'error':'Book Data Does Not Exists'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializers = BookSerializer(books, many=True)
            return Response(serializers.data, status= status.HTTP_200_OK)


class Book_Detail_View(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request,book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error':'Book not found'}, status= status.HTTP_404_NOT_FOUND)
        else:
            serializer = BookSerializer(book)
            return Response(serializer.data, status= status.HTTP_200_OK)
        

