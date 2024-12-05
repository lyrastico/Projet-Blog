from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView

def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'myapp/blog_list.html', {'posts': posts})

def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        body = request.POST.get('body')
        comment = Comment(post=post, name=name, body=body)
        comment.save()
        
        return redirect('blog_detail', post_id=post.id)

    comments = post.comments.all()
    
    return render(request, 'myapp/blog_detail.html', {'post': post, 'comments': comments})

def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user 
            post.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'myapp/blog_form.html', {'form': form})

def blog_edit(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', post_id=post.id)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'myapp/blog_form.html', {'form': form})

def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.post.author:
        comment.delete()
        return redirect('blog_detail', post_id=comment.post.id)
    else:
        return redirect('blog_list')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Compte créé avec succès ! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/signup.html', {'form': form})

def blog_delete(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if post.author == request.user:
        if request.method == 'POST':
            post.delete()
            return redirect('blog_list')
    else:
        messages.error(request, "Vous ne pouvez pas supprimer ce post.")
        return redirect('blog_list')
    return render(request, 'myapp/blog_confirm_delete.html', {'post': post})

def user_blog_list(request):
    # Récupère tous les blogs créés par l'utilisateur connecté
    posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'myapp/user_blog_list.html', {'posts': posts})


class CustomLoginView(LoginView):
    template_name = 'myapp/login.html'

class CustomLogoutView(LogoutView):
    next_page = '/'
