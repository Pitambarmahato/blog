from django.contrib.auth import views
from django.urls import path

from .views import SignupView, ProfileView, follow
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('follow/<int:pk>', follow, name='follow')
]
