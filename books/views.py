from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Reviews
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from library.models import UsersBook


def all_books(request):
    books = Book.objects.all()

    return render(request, 'books/all_books.html', {"books": books})


def book_details(request, book_id):
    book = get_object_or_404(Book, pk=book_id)


    #button logic
    userbook_status = "Add to Library"
    
    if request.user.is_authenticated:
        user_book = UsersBook.objects.filter(
            book=book,
            user=request.user
        ).first()
        
        if user_book:
            userbook_status = user_book.get_status_display()
    #end of button logic

    user_review = None

    if request.user.is_authenticated:
        try:
            user_review = Reviews.objects.get(user=request.user, book=book)
        except Reviews.DoesNotExist:
            user_review = None

    if request.method == 'POST':
        if request.user.is_authenticated:
            rating = request.POST.get('rating')
            review_text = request.POST.get('text', '').strip()

            if not rating:
                messages.error(request, "Rating is required.")
            else:
                try:
                    rating = int(rating)
                    if rating < 1 or rating > 5:
                        raise ValueError

                    review, created = Reviews.objects.update_or_create(
                        user=request.user,
                        book=book,
                        defaults={'rating': rating, 'text': review_text}
                    )

                    if created:
                        messages.success(request, "Review submitted successfully.")
                    else:
                        messages.success(request, "Review updated successfully.")

                    return redirect('book_details', book_id=book.id)

                except ValueError:
                    messages.error(request, "Invalid rating. Please select between 1 and 5.")
        else:
            messages.error(request, "You must be logged in to submit a review.")
            return redirect('login')

    reviews = Reviews.objects.filter(book=book).order_by('-created_at')

    return render(request, 'books/book_details.html', {
        "book": book,
        "reviews": reviews,
        "user_review": user_review,
        "userbook_status": userbook_status,
        'book_is_added': userbook_status != 'Add to Library',
    })


def update_book_status(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user

    if request.method == 'POST':
        status = request.POST.get('status', 'added')

        user_book, created = UsersBook.objects.get_or_create(user=user, book=book)

        if status == 'REMOVE':
            user_book.delete()
        else:
            user_book.status = status
            user_book.save()

    return redirect('book_details', book_id=book_id)



# @require_POST
# @login_required
# def ChangeBookStatus(request, book_id):
#     book = get_object_or_404(Book, pk=book_id)

#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             status = request.POST.get('status')

    


# @require_POST
# def submit_review(request, book_id):
#     text = request.POST.get('text', '').strip()

#     if text and len(text) <= 700:
#         book = Book.objects.get(id=book_id)
#         Reviews.objects.create(
#             book=book,
#             user=request.user,
#             text=text
#         )
#         return redirect(f'/books/{book.id}/', book_id=book.id)
#     else:
#         # Handle error (e.g., show error message or redirect)
#         return redirect(f'/books/{book.id}/', book_id=book.id)
