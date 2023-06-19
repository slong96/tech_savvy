from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # One to one relationship with User
    image = models.ImageField(default='default.jpg', upload_to='profile-pics') # default image for any user

    # dunder function for admin
    def __str__(self):
        return f'{self.user.username} Profile'
    

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(self.image.path) # this will open the image of the current instance

    #     # resizing the image if over 300px
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)