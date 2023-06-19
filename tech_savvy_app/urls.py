from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, AddCommentView, DeleteCommentView
from . import views


urlpatterns = [
    path('', views.home, name='home'), # home.html
    path('post/all', PostListView.as_view(), name='all-post'), # all_post.html
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'), # user_posts.html
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), # post_detail.html
    path('post/new/', PostCreateView.as_view(), name='post-create'), # post_form.html
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), # post_form.html
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), # post_confirm_delete.html
    path('post/<int:pk>/add-comment', AddCommentView.as_view(), name='add-comment'), # post_detail.html
    path('comment/<int:pk>/delete-comment', DeleteCommentView.as_view(), name='delete-comment'), # .html
    path('post/search', views.search_post, name='search'), # search_post.html
    path('about/', views.about, name='blog-about'), # about.html
]