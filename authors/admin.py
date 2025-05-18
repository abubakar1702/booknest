from django.contrib import admin
from .models import Author, AuthorGenres


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'total_books', 'is_varified')

    def total_books(self, obj):
        return obj.book_set.count()


admin.site.register(AuthorGenres)