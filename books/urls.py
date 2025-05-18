from django.urls import path
from . import views

urlpatterns = [
    path('',  views.all_books, name="all_books"),
    path('<int:book_id>/',views.book_details, name = "book_details"),
    path('<int:book_id>/update-status/', views.update_book_status, name='update_book_status'),
]
