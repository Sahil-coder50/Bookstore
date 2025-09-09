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
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def delete(self, request):
        try:
            books = Book.objects.all()
        except Book.DoesNotExist:
            return Response({'error':'Books cannot be deleted'}, status=status.HTTP_404_NOT_FOUND)
        else:
            books.delete()
            return Response({'messages':'Books are Deleted'}, status=status.HTTP_204_NO_CONTENT)


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
        
    def put(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error':'This book does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = BookSerializer(book, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        
    
    def patch(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error':'This book does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = BookSerializer(book, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def delete(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error':'Book does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            book.delete()
            return Response({'messages':'Book is Deleted'}, status=status.HTTP_204_NO_CONTENT)

