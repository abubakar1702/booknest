from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import ReadingGoal, UsersBook, UsersList
from django.contrib.auth.decorators import login_required
from .forms import ListCreationForm
from django.utils import timezone
from books.models import Reviews
from books.models import Book
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from datetime import date, datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, TemplateView


@login_required
def user_library(request):
    user = request.user
    books = UsersBook.objects.filter(user=user)

    # Fetch reading goals
    goals = ReadingGoal.objects.filter(user=user).order_by('-year', '-month')
    monthly_goals = goals.exclude(month__isnull=True)
    yearly_goals = goals.filter(month__isnull=True)


    # Build goal data for progress bars
    goal_data = []
    for goal in goals:
        if goal.month is not None:
            name = f"{goal.month_name} {goal.year}"
            total = goal.monthly_goal
            goal_type = "Monthly"
        else:
            name = f"{goal.year}"
            total = goal.yearly_goal
            goal_type = "Yearly"

        goal_data.append({
            'name': name,
            'type': goal_type,
            'completed': goal.completed_books(),
            'total': total,
            'percentage': goal.progress_percentage(),
        })

    # Final context
    context = {
        'books': books,
        'total_books': books.count(),
        'total_read_books': books.filter(status='read').count(),
        'user_lists': UsersList.objects.filter(user=user),
        'currently_reading': books.filter(status='reading'),
        'currently_reading_count': books.filter(status='reading').count(),
        'total_lists': UsersList.objects.filter(user=user).count(),
        'user_reviews': Reviews.objects.filter(user=user).select_related('book'),

        # Goal data
        'goals': goals,
        'monthly_goals': monthly_goals,
        'yearly_goals': yearly_goals,
        'goal_data': goal_data,
    }

    return render(request, 'library/library.html', context)



@login_required
def user_lists(request):
    lists = UsersList.objects.filter(user = request.user)

    context = {
        'lists': lists,
        'total_lists': UsersList.objects.filter(user = request.user).count()
    }

    return render(request, 'library/user_lists.html', context)

@login_required
def create_list(request):
    if request.method == 'POST':
        form = ListCreationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            selected_books = form.cleaned_data['books']

            userList = UsersList.objects.create(user= request.user, name = name)
            userList.books.set(selected_books)

            return redirect('user_library')
    else:
        form = ListCreationForm()
    return render(request, 'library/partials/create_list.html', {'form': form})
