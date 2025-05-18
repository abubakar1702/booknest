from django.urls import path
from . import views

urlpatterns = [
    path('<int:author_id>/', views.authors_profile, name="authors_profile")
]
