from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('books/', views.Books_List, name='books-list'),
    path('books/add/', views.Books_Add, name='book-add'),
    path('books/detail/<int:book_id>/', views.Book_Detail, name='book-detail'),
    path('books/detail/update/<int:book_id>/', views.Book_Update, name='book-update'),

    path('authors/', views.Authors_List, name='authors-list'),
    path('authors/add/', views.Author_Add, name='author-add'),
    path('authors/detail/<int:author_id>/', views.Author_Detail, name='author-detail'),
    path('authors/detail/update/<int:author_id>/', views.Author_Update, name='author-update'),

    path('', views.Login_View, name='login'),
    path('logout/', views.Logout_View, name='logout'),
    path('signup/', views.Signup_View, name='signup'),
    path('activate/<str:token>/', views.activate_user, name='activate'),

    # Password reset views

    path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),

    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="reges/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reges/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="reges/reset_done.html"), name='password_reset_complete'),

]