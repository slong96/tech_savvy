from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # didn't put now() because I don't want to execute the function at that point. Just want to pass the function as a default value.
    date_posted = models.DateTimeField(default=timezone.datetime.now)
    # if user is delete, the user's post will be deleted too.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # dunder function
    def __str__(self):
        return f'{self.author}: {self.title} - {self.content}'
    
    # when post is created, this will take the user to the detail page of that post.
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.datetime.now)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f'{self.author}: {self.post}'
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})