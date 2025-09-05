from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from . models import Author, Book

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import PasswordResetView

# Create your views here.

@login_required(login_url='login')
def Books_List(request):
    if request.method == 'GET':
        books = Book.objects.all()

        return render(request, 'books.html', {'books': books})

    elif request.method == 'POST':
        ...

@login_required(login_url='login')
def Book_Detail(request, book_id):
    if request.method == 'GET':
        book = Book.objects.get(id=book_id)

        return render(request, 'detail.html', {'book': book})

    elif request.method == 'PATCH':
        ...


""" Login, Logout and Signup Functionality """

def Signup_View(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    
    elif request.method == 'POST':
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.info(request, "Password and Confirm Password are not same")
            return render(request, 'signup.html')

        else:
            user = User.objects.filter(username=username)

            if user.exists():
                messages.info(request, "Username already exists")
            else:
                user = User.objects.create(username=username, first_name=first_name, email=email, password=password)
                user.set_password(password)
                user.save()

                messages.info(request, "Profile is Created")
                return render(request, 'signup.html')
            
            return render(request, 'signup.html')


def Login_View(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('books-list')
        else:
            messages.info(request, "Username or Password is invalid")
        
        return render(request, 'login.html')
            

def Logout_View(request):
    if request.method == 'GET':
        logout(request)
        messages.info(request, "Logout Successful")
        return redirect('login')


""" Password Reset """

class MyPasswordResetView(PasswordResetView):
    template_name = 'reges/password_reset_form.html'
    email_template_name = 'reges/password_reset_email.html'
    subject_template_name = 'reges/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')