from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.user_library, name="user_library"),
    path('lists/', views.user_lists, name="user_lists"),
    path('create_list/', views.create_list, name="create_list"),
]
