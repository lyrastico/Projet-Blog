from django.contrib import admin
from django.urls import path
from blog import views 
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.blog_list, name='blog_list'),  # Page d'accueil
    path('post/<int:post_id>/', views.blog_detail, name='blog_detail'),  # Détail d'un post
    path('post/new/', views.blog_create, name='blog_create'),  # Création d'un nouveau post
    path('post/<int:post_id>/edit/', views.blog_edit, name='blog_edit'),  # Édition d'un post
    path('post/<int:post_id>/delete/', views.blog_delete, name='blog_delete'),  # Suppression d'un post
    path('signup/', views.signup, name='signup'),  # Inscription
    path('login/', LoginView.as_view(template_name='myapp/login.html'), name='login'),  # Connexion
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Déconnexion
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('my-blogs/', views.user_blog_list, name='user_blog_list'),
]
