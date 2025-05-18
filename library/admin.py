from django.contrib import admin
from .models import ReadingGoal, UsersList, UsersBook
from django.core.exceptions import ValidationError

@admin.register(UsersBook)
class UserBookAdmin(admin.ModelAdmin):
    list_display = ('book','display_authors','user', 'status','created_at', 'updated_at')
    def display_authors(self, obj):
        return ", ".join(author.name for author in obj.book.authors.all())
    display_authors.short_description = "Authors"

@admin.register(UsersList)
class UserBookAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'total_books','created_at', 'updated_at')

    def total_books(self, obj):
        return obj.books.count()



@admin.register(ReadingGoal)
class ReadingGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'goal_type', 'goal_count', 'year', 'progress', 'is_completed_display')

    def goal_type(self, obj):
        return "Monthly" if obj.month is not None else "Yearly"
    goal_type.short_description = 'Goal Type'

    def goal_count(self, obj):
        return obj.monthly_goal if obj.month is not None else obj.yearly_goal
    goal_count.short_description = 'Goal Count'

    def progress(self, obj):
        return f"{obj.progress_percentage()}%"
    progress.short_description = 'Progress'

    def is_completed_display(self, obj):
        return obj.is_completed()
    is_completed_display.boolean = True
    is_completed_display.short_description = 'Completed'
