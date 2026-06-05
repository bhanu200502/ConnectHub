from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('create-post/', views.create_post, name='create_post'),
    path('delete-post/<int:pk>/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('add-comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('delete-comment/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('like-post/<int:pk>/', views.like_post, name='like_post'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('search/', views.search_users, name='search_users'),
    path('dashboard/', views.dashboard, name='dashboard'),
]