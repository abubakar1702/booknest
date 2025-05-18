from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from datetime import date
from django.core.exceptions import ValidationError


class UsersBook(models.Model):
    STATUS_CHOICES = [
        ('added', 'In Library'),
        ('reading', 'Currently Reading'),
        ('read', 'Read')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book')
    

    def __str__(self):
        return f"{self.book.name} in {self.user}'s Library"
    
class UsersList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(UsersBook, blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} by {self.user.username}"



class ReadingGoal(models.Model):
    MONTH_CHOICES = [
        (1, 'January'), (2, 'February'), (3, 'March'),
        (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'),
        (10, 'October'), (11, 'November'), (12, 'December'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Use either month (1-12) for monthly goals, or None for yearly goals
    month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES, null=True, blank=True)
    year = models.IntegerField(default=date.today().year)
    
    # Monthly goal applies only if month is set
    monthly_goal = models.PositiveSmallIntegerField(null=True, blank=True)
    # Yearly goal applies only if month is None
    yearly_goal = models.PositiveSmallIntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'year', 'month'],
                name='unique_user_goal_per_period',
            ),
            models.CheckConstraint(
                check=(
                    # Either monthly_goal is set and month is not null
                    (
                        models.Q(month__isnull=False) & 
                        models.Q(monthly_goal__isnull=False) & 
                        models.Q(yearly_goal__isnull=True)
                    ) |
                    # Or yearly_goal is set and month is null
                    (
                        models.Q(month__isnull=True) & 
                        models.Q(yearly_goal__isnull=False) & 
                        models.Q(monthly_goal__isnull=True)
                    )
                ),
                name='monthly_or_yearly_goal_only',
            )
        ]

    def clean(self):
        # Validate consistency of goals vs month field
        if self.month is None:
            # Yearly goal record
            if not self.yearly_goal:
                raise ValidationError("Yearly goal must be set for yearly goals.")
            if self.monthly_goal is not None:
                raise ValidationError("Monthly goal must be empty for yearly goals.")
        else:
            # Monthly goal record
            if not self.monthly_goal:
                raise ValidationError("Monthly goal must be set for monthly goals.")
            if self.yearly_goal is not None:
                raise ValidationError("Yearly goal must be empty for monthly goals.")
        super().clean()

    @property
    def month_name(self):
        if self.month is None:
            return None
        return dict(self.MONTH_CHOICES).get(self.month)

    def completed_books(self):
        from library.models import UsersBook  # Avoid circular import
        filters = {
            'user': self.user,
            'status': 'read',
        }
        if self.month is not None:
            filters['updated_at__month'] = self.month
            filters['updated_at__year'] = self.year
        else:
            filters['updated_at__year'] = self.year
        return UsersBook.objects.filter(**filters).count()

    def progress_percentage(self):
        goal = self.monthly_goal if self.month is not None else self.yearly_goal
        if not goal or goal == 0:
            return 0
        completed = self.completed_books()
        percentage = (completed / goal) * 100
        return min(100, round(percentage, 2))

    def is_completed(self):
        goal = self.monthly_goal if self.month is not None else self.yearly_goal
        return self.completed_books() >= goal

    def remaining_books(self):
        goal = self.monthly_goal if self.month is not None else self.yearly_goal
        remaining = goal - self.completed_books()
        return max(0, remaining)

    def __str__(self):
        if self.month is None:
            return f"{self.user.username}'s Yearly Goal ({self.year}): {self.yearly_goal} books"
        else:
            return f"{self.user.username}'s {self.month_name} {self.year} Goal: {self.monthly_goal} books"
