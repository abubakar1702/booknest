from . import views
from django.urls import path

urlpatterns = [
    path('signup/', views.UserSignUpView, name='signup'),
    path('login/', views.UserLoginView, name='login'),
]
