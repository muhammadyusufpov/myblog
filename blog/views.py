from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth import get_user_model
from .models import Post
from .forms import PostForm

def blog_list(request):
    posts = Post.objects.all().order_by('-created_at')
    categories = Post.objects.values_list('category', flat=True).distinct()
    return render(request, 'post.html', {'posts': posts, 'categories': categories})

def create_post(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = PostForm()
        
    return render(request, 'write.html', {'form': form})

def edit_post(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
        
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.content_format = Post.FORMAT_MARKDOWN
            post.save()
            next_url = request.POST.get('next_url')
            return redirect(next_url if next_url else 'blog_list')
    else:
        form = PostForm(instance=post)
        next_url = request.META.get('HTTP_REFERER')

    return render(request, 'edit.html', {
        'form': form, 
        'post': post,
        'next_url': next_url
    })

def delete_post(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
        
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
    return redirect('blog_list')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})
