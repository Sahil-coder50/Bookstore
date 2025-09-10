from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from user.models import Book, Author, ActivationToken
from user.api.serializers import BookSerializer, AuthorSerializer

from django.shortcuts import get_object_or_404
from django.db.models import Q



"""
The code for Books APIs is Below
"""


class Book_List_View(APIView):

    permission_classes = [IsAuthenticated]    

    def get(self, request):
        item_name = request.GET.get('search')
        try:
            books = Book.objects.all()
        except Book.DoesNotExist:
            return Response({'error':'Book Data Does Not Exists'}, status=status.HTTP_404_NOT_FOUND)
        else:
            if item_name:
                books = books.filter(title__icontains=item_name)
                
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


"""
The code for Author APIs is Below.
"""


class Author_List_View(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):

        item_name = request.GET.get('search')
        try:
            author = Author.objects.all()

            if item_name:
                author = author.filter(name__icontains=item_name)
                
        except Author.DoesNotExist:
            return Response({'error':'Author Database is Empty'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = AuthorSerializer(author, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AuthorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def delete(self, request):
        try:
            author = Author.objects.all()
        except Author.DoesNotExist:
            return Response({'error':'No Authors to be deleted'}, status=status.HTTP_404_NOT_FOUND)
        else:
            author.delete()
            return Response({'messages':'Authors are Deleted'}, status=status.HTTP_204_NO_CONTENT)


class Author_Detail_View(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response({'error':'Author Does not Exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = AuthorSerializer(author)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response({'error':'Author Does not Exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = AuthorSerializer(author, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
            
    def patch(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response({'error':'Author Does not Exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = AuthorSerializer(author, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self,request, author_id):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response({'error':'Author Does not Exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            author.delete()
            return Response({'messages':'Author is Deleted'}, status=status.HTTP_204_NO_CONTENT)
        

