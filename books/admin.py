from django.contrib import admin
from .models import Book, BookGenres, BookLanguages, Awards, Reviews

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name','display_authors', 'first_published', 'isbn', 'display_languages')

    def display_authors(self, obj):
        return ", ".join(author.name for author in obj.authors.all())
    display_authors.short_description= "Authors"
    
    def display_languages(self, obj):
        return ", ".join(language.name for language in obj.languages.all())
    display_languages.short_description= "Languages"

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(BookLanguages)
admin.site.register(BookGenres)
admin.site.register(Awards)