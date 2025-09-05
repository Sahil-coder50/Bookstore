from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Books_List, name='books-list'),
    path('detail/<int:book_id>/', views.Book_Detail, name='book-detail'),

    path('login/', views.Login_View, name='login'),
    path('logout/', views.Logout_View, name='logout'),
    path('signup/', views.Signup_View, name='signup'),

    # Password reset views

    path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),

    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="reges/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]