from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from . models import Author, Book, ActivationToken

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import PasswordResetView

import requests
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from django.utils import timezone
from datetime import timedelta

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

# Create your views here.


"""
Books FrontEnd Code Views are here
"""


@login_required(login_url='login')
def Books_List(request):

    access = request.session.get('access')

    if not is_access_token_valid(access):
        refresh_resp = requests.post("http://127.0.0.1:8000/api/token/refresh/", json={
            "refresh": request.session.get("refresh")
        })
        new_access = refresh_resp.json().get("access")
        
        request.session["access"] = new_access

        access = new_access

    headers = {"Authorization": f"Bearer {access}",
               "Content-Type": "application/json",
                "Accept": "application/json"}

    if request.method == 'GET':
        # books = Book.objects.all()

        """Search Code"""
        item_name = request.GET.get('item_name')
        params = {}
        if item_name:
            params['search'] = item_name

        # GET request with JWT auth
        resp = requests.get("http://127.0.0.1:8000/api/books/", params=params, headers=headers)
        books = resp.json()

        return render(request, 'books.html', {'books': books})
        
    elif request.method == 'DELETE':

        # DELETE request with JWT auth
        resp = requests.delete("http://127.0.0.1:8000/api/books/", headers=headers)
        books = resp.json()

        return render(request, 'books.html', {'books':books})



@login_required(login_url='login')
def Books_Add(request):

    access = request.session.get('access')

    if not is_access_token_valid(access):
        refresh_resp = requests.post("http://127.0.0.1:8000/api/token/refresh/", json={
            "refresh": request.session.get("refresh")
        })
        new_access = refresh_resp.json().get("access")
        
        request.session["access"] = new_access

        access = new_access

    headers = {"Authorization": f"Bearer {access}",
               "Content-Type": "application/json",
                "Accept": "application/json"}

    if request.method == 'GET':
        return render(request, 'book_add.html')
    
    elif request.method == 'POST':
        
        payload = {
            'title':request.POST.get('title'),
            'author':request.POST.get('author'),
            'published_date':request.POST.get('published_date'),
            'price':request.POST.get('price'),
            'stock':request.POST.get('stock'),
        }


        # POST request with JWT auth
        resp = requests.post("http://127.0.0.1:8000/api/books/", json=payload, headers=headers)

        return redirect('books-list')
    



@login_required(login_url='login')
def Book_Detail(request, book_id):

    access = request.session.get('access')

    if not is_access_token_valid(access):
        refresh_resp = requests.post("http://127.0.0.1:8000/api/token/refresh/", json={
            "refresh": request.session.get("refresh")
        })
        new_access = refresh_resp.json().get("access")
        
        request.session["access"] = new_access

        access = new_access

    headers = {"Authorization": f"Bearer {access}",
               "Content-Type": "application/json",
                "Accept": "application/json"}

    if request.method == 'GET':
        # book = Book.objects.get(id=book_id)

        # GET request with JWT auth
        resp = requests.get(f"http://127.0.0.1:8000/api/books/{book_id}/", headers=headers)
        book = resp.json()
  
        return render(request, 'book_detail.html', {'book': book})
    
    elif request.method == 'POST':
        method = request.POST.get('_method')
        if method == 'DELETE':
            
            #  DELETE request with JWT auth
            resp = requests.delete(f"http://127.0.0.1:8000/api/books/{book_id}/", headers=headers)

            return redirect('books-list')




@login_required(login_url='login')
def Book_Update(request, book_id):

    access = request.session.get('access')

    if not is_access_token_valid(access):
        refresh_resp = requests.post("http://127.0.0.1:8000/api/token/refresh/", json={
            "refresh": request.session.get("refresh")
        })
        new_access = refresh_resp.json().get("access")
        
        request.session["access"] = new_access

        access = new_access

    headers = {"Authorization": f"Bearer {access}",
               "Content-Type": "application/json",
                "Accept": "application/json"}

    if request.method == 'GET':

        #  GET request with JWT auth
        resp = requests.get(f"http://127.0.0.1:8000/api/books/{book_id}/", headers=headers)
        book = resp.json()

        return render(request, 'book_update.html', {'book': book})

    elif request.method == 'POST':

        # PUT and PATCH request with JWT auth
        payload = {
            'title':request.POST.get('title'),
            'author':request.POST.get('author'),
            'published_date':request.POST.get('published_date'),
            'price':request.POST.get('price'),
            'stock':request.POST.get('stock'),
        }

        # drop empty values
        payload = {k: v for k, v in payload.items() if v not in (None, '', [])}

        method = request.POST.get('_method', 'PUT')

        if method == 'PATCH':
            resp = requests.patch(f"http://127.0.0.1:8000/api/books/{book_id}/", json=payload,headers=headers)
            book = resp.json()
        else:
            resp = requests.put(f"http://127.0.0.1:8000/api/books/{book_id}/", json=payload, headers=headers)
            book = resp.json()
        
        if resp.status_code in (200, 204):
            return redirect('book-detail', book_id=book_id)
        else:
            return render(request, 'book_update.html', {"book":book})


""" 
Authors FrontEnd Code Views are here
"""


@login_required(login_url='login')
def Authors_List(request):
    access = request.session.get('access')

    if not is_access_token_valid(access):
        refresh_resp = requests.post("http://127.0.0.1:8000/api/token/refresh/", json={
            "refresh": request.session.get("refresh")
        })
        new_access = refresh_resp.json().get("access")
        
        request.session["access"] = new_access

        access = new_access

    headers = {"Authorization": f"Bearer {access}",
               "Content-Type": "application/json",
                "Accept": "application/json"}
    
    if request.method == 'GET':

        """Search Code"""
        item_name = request.GET.get('item_name')
        params = {}
        if item_name:
            params['search'] = item_name
        
        # GET request with JWT auth

        resp = requests.get(f"http://127.0.0.1:8000/api/authors/", params=params, headers=headers)
        authors = resp.json()

        return render(request, 'Author/authors.html',{'authors':authors})
                


@login_required(login_url='login')
def Author_Add(request):
    access = request.session.get('access')

    if not is_access_token_valid(access):
        refresh_resp = requests.post("http://127.0.0.1:8000/api/token/refresh/", json={
            "refresh": request.session.get("refresh")
        })
        new_access = refresh_resp.json().get("access")
        
        request.session["access"] = new_access
        
        access = new_access

    headers = {"Authorization": f"Bearer {access}",
               "Content-Type": "application/json",
                "Accept": "application/json"}
    
    if request.method == 'GET':
        return render(request, 'Author/author_add.html')
    
    elif request.method == 'POST':
        
        payload = {
            "name":request.POST.get('name'),
            "biography":request.POST.get('biography')            
        }

        # POST request with JWT auth
        resp = requests.post(f"http://127.0.0.1:8000/api/authors/", json=payload, headers=headers)

        return redirect('authors-list')



@login_required(login_url='login')
def Author_Detail(request, author_id):
    access = request.session.get('access')

    if not is_access_token_valid(access):
        refresh_resp = requests.post(f"http://127.0.0.1:8000/api/token/refresh/", json={
            "refresh": request.session.get("refresh")
        })
        new_access = refresh_resp.json().get("access")

        request.session["access"] = new_access

        access = new_access

    headers = {
        "Authorization": f"Bearer {access}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    if request.method == 'GET':
        
        # GET request for Detail Author with JWT auth
        resp = requests.get(f"http://127.0.0.1:8000/api/authors/{author_id}/", headers=headers)
        author = resp.json()
        print(author)

        return render(request, 'Author/author_detail.html', {'author':author})
    
    elif request.method == 'POST':

        method = request.POST.get('_method')

        if method == 'DELETE':
            
            resp = requests.delete(f"http://127.0.0.1:8000/api/authors/{author_id}/", headers=headers)

            return redirect('authors-list')



@login_required(login_url='login')
def Author_Update(request, author_id):
    access = request.session.get('access')

    if not is_access_token_valid(access):
        refresh_resp = requests.post("http://127.0.0.1:8000/api/token/refresh/", json={
            "refresh": request.session.get("refresh")
        })
        new_access = refresh_resp.json().get("access")
        
        request.session["access"] = new_access

        access = new_access

    headers = {"Authorization": f"Bearer {access}",
               "Content-Type": "application/json",
                "Accept": "application/json"}
    
    if request.method == 'GET':

        resp = requests.get(f"http://127.0.0.1:8000/api/authors/{author_id}/", headers=headers)
        author = resp.json()

        return render(request, 'Author/author_update.html', {'author':author})
    
    elif request.method == 'POST':

        payload = {
            "name":request.POST.get('name'),
            "biography":request.POST.get('biography')
        }

        payload = {k: v for k, v in payload.items() if v not in (None, '', [])}

        method = request.POST.get('_method','PUT')

        if method == 'PATCH':
            resp = requests.patch(f"http://127.0.0.1:8000/api/authors/{author_id}/", json=payload, headers=headers)
            author = resp.json()            
        else:
            resp = requests.patch(f"http://127.0.0.1:8000/api/authors/{author_id}/", json=payload, headers=headers)
            author = resp.json()

        if resp.status_code in (200,204):
            return redirect('author-detail', author_id=author_id)
        else:
            return render(request, 'author_update.html', {"author":author})



""" Login, Logout and Signup Functionality """




def Signup_View(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{"RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY})
    
    elif request.method == 'POST':
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if verify_recaptcha(request.POST.get("g-recaptcha-response")):

            if password != confirm_password:
                messages.info(request, "Password and Confirm Password are not same")
                return render(request, 'signup.html',{"RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY})

            else:
                user = User.objects.filter(username=username)

                if user.exists():
                    messages.info(request, "Username already exists")
                else:
                    user = User.objects.create_user(username=username, first_name=first_name, email=email, password=password, is_active=False)
                    # user.set_password(password)
                    # user.save()

                    token = get_random_string(32)

                    ActivationToken.objects.create(user=user, token=token)

                    send_verification_email(user.email, token)

                    messages.info(request, "Profile is Created")
                    return render(request, 'signup.html',{"RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY})
                
                return render(request, 'signup.html',{"RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY})
        
        else:
            messages.error(request, "Invalid reCAPTCHA")
            return render(request, 'signup.html',{"RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY})


def Login_View(request):
    if request.method == 'GET':
        return render(request, 'login.html', {"RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY})

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        if verify_recaptcha(request.POST.get("g-recaptcha-response")):

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                access = request.session.get("access")

                if access is None:
                    resp = requests.post("http://127.0.0.1:8000/api/token/", json={
                        "username": username,
                        "password": password
                    })
                    tokens = resp.json()

                    request.session["access"] = tokens["access"]
                    request.session["refresh"] = tokens["refresh"]
                
                elif not is_access_token_valid(access):
                    refresh_resp = requests.post("http://127.0.0.1:8000/api/token/refresh/", json={
                        "refresh": request.session.get("refresh")
                    })
                    new_access = refresh_resp.json().get("access")
                    
                    request.session["access"] = new_access

                return redirect('books-list')
            
            else:
                messages.info(request, "Username or Password is invalid")
            
            return render(request, 'login.html', {"RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY})
        
        else:
            messages.error(request, "Invalid reCAPTCHA")
            return render(request, 'login.html', {"RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY})
            

def Logout_View(request):
    if request.method == 'GET':
        logout(request)
        messages.info(request, "Logout Successful")
        return redirect('login')



""" Verification Email """

def send_verification_email(email, token):
    activation_link = f"{settings.SITE_URL}/activate/{token}"
    send_mail(
        subject="Activate your account",
        message=f"Click here to activate: {activation_link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )


""" Activate User Code """

def activate_user(request, token):
    activation = get_object_or_404(ActivationToken,token=token)

    # Reject stale tokens
    if timezone.now() - activation.created_at > timedelta(days=1):
        messages.info(request, "Token expired")
        return redirect("login", status=400)

    # Flip the switch
    user = activation.user
    user.is_active = True
    user.save()

    # Invalidate the token so it cannot be reused
    activation.delete()

    messages.info(request, "Account activated")
    return redirect("login")


""" Password Reset """


class MyPasswordResetView(PasswordResetView):
    template_name = 'reges/password_reset_form.html'
    email_template_name = 'reges/password_reset_email.html'
    subject_template_name = 'reges/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["RECAPTCHA_PUBLIC_KEY"] = settings.RECAPTCHA_PUBLIC_KEY
        return context

    def form_valid(self, form):
        """Check reCAPTCHA before proceeding with password reset"""
        recaptcha_response = self.request.POST.get("g-recaptcha-response")

        # Send verification request to Google
        data = {
            "secret": settings.RECAPTCHA_PRIVATE_KEY,
            "response": recaptcha_response
        }
        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
        result = r.json()

        if result.get("success"):
            # ✅ CAPTCHA passed → continue normal flow
            return super().form_valid(form)
        else:
            # ❌ CAPTCHA failed → reload form with error
            messages.error(self.request, "Invalid reCAPTCHA. Please try again.")
            return self.form_invalid(form)




""" Captcha Code """


def verify_recaptcha(response_token):
    data = {
        "secret": settings.RECAPTCHA_PRIVATE_KEY,
        "response": response_token
    }
    r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
    return r.json().get("success", False)


""" JWT Authentication for API -- checking if access token is valid """


def is_access_token_valid(token):
    try:
        # settings.SIMPLE_JWT["SIGNING_KEY"] is usually your Django SECRET_KEY
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_exp": True}  # will raise error if expired
        )
        return True
    except ExpiredSignatureError:
        return False
    except InvalidTokenError:
        return False