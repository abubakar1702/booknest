from django.db import models

class AuthorGenres(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField()
    date_of_death = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=100)
    website = models.URLField(null=True, blank=2)
    image = models.ImageField(upload_to='author_images/')
    genres = models.ManyToManyField(AuthorGenres)
    is_varified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name