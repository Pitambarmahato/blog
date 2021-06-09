from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='index'),
    path('create/', views.post, name='create'),
    path('post/<int:pk>', views.get_post, name='post_detail'),
    path('update/<int:pk>', views.update_post, name='update'),
    path('delete/<int:pk>', views.delete_post, name='delete'),
    path('category/<int:pk>', views.filter_post, name='category'),
    path('like/<int:pk>', views.post_like, name = 'post_like')

]