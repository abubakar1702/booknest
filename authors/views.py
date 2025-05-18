from django.shortcuts import render, get_object_or_404
from .models import Author
from books.models import Book


def authors_profile(request, author_id):
    author = get_object_or_404(Author, pk = author_id)

    author_books = Book.objects.filter(authors=author).order_by('-first_published')

    context = {
        'author': author,
        'author_books': author_books,
    }

    return render(request, 'authors/authors_profile.html', context)
