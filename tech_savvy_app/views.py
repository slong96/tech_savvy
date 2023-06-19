from typing import Any, Dict
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment

"""Class base views"""

# List of Post on home page
class PostListView(ListView):
    model = Post
    template_name = 'tech_savvy_app/all_post.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted'] # newest to oldest
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Latest Posts'
        return context



# List of User Post
class UserPostListView(ListView):
    model = Post
    template_name = 'tech_savvy_app/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    # getting user query set
    def get_queryset(self):
        # variable - get user object from User model - get a user with username equals username from URL
        # if user doesn't exist, return 404
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # return filter author that equals to user that I just got.
        return Post.objects.filter(author=user).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Your Posts'
        return context



# Detail Post
class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Viewing Post'
        return context



# Create Post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        # this is basically saying that the user trying to create a post, this will take the instance and set the author to equal to the user that's logged in.
        form.instance.author = self.request.user
        # running form valid method on parent class
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Post'
        return context



# Update Post
# LoginRequiredMixin and UserPassesTestMixin have to be on the left of UpdateView
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        # this is basically saying that the user trying to create a post, this will take the instance and set the author to equal to the user that's logged in.
        form.instance.author = self.request.user
        # running form valid method on parent class
        return super().form_valid(form)
    
    def test_func(self):
        # get post that the user wants to update
        post = self.get_object()
        # if logged in user equals author of post
        if self.request.user == post.author:
            # return true to allow user to update post
            return True
        # else return false to deny access to update post
        return False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Post'
        return context



# Delete Post
# LoginRequiredMixin and UserPassesTestMixin have to be on the left of DeleteView
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/post/all' # after deletion, redirect to home page

    def test_func(self):
        # get post that the user wants to update
        post = self.get_object()
        # if logged in user equals author of post
        if self.request.user == post.author:
            # return true to allow user to update post
            return True
        # else return false to deny access to update post
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Post'
        return context
    


# Add comment to post
class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        # this is basically saying that the user trying to create a post, this will take the instance and set the author to equal to the user that's logged in.
        form.instance.post_id = self.kwargs['pk']
        form.instance.author = self.request.user
        # running form valid method on parent class
        return super().form_valid(form)

    # https://stackoverflow.com/questions/55872523/what-does-integrityerror-not-null-constraint-failed-blog-comment-post-id-st
    # returns url where you 'll be redirected after the form is correctly filled
    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("post-detail", kwargs={"pk": pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Comment'
        return context



# Delete comment from a post
class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    
    # https://stackoverflow.com/questions/62469243/how-to-redirect-to-post-detail-page-after-deleting-a-comment-in-django
    # after deleting comment, get_success_url will redirect user to the post where the comment was deleted
    def get_success_url(self):
        post = Post.objects.get(pk=self.object.post.pk)
        return post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Comment'
        return context
    



def home(request):
    return render(request, 'tech_savvy_app/home.html', {'title': 'Home'})



def about(request):
    return render(request, 'tech_savvy_app/about.html', {'title': 'About'})



def search_post(request):
    if request.method == 'POST':
        search_post = request.POST['search-post'] # name='search-post' from html input
        search_site = Post.objects.filter(title__icontains=search_post) | Post.objects.filter(content__icontains=search_post)
        return render(request, 'tech_savvy_app/search_post.html', {'search_post': search_post, 'search_site': search_site, 'title': 'Search'})