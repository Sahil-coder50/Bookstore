from django.urls import path
from user.api import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('books/', views.Book_List_View.as_view(), name='api-books-list'),
    path('books/<int:book_id>/', views.Book_Detail_View.as_view(), name='api-book-detail'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]