from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    verified_at = models.DateTimeField(null=True)
    middle_name = models.CharField(max_length=100, null=True)
    login_count = models.IntegerField(null=True, default=0)
    # avatar = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile_user')
    image = models.ImageField(upload_to='profiles/', default = 'profiles/default.jpg')
    bio = models.TextField()
    
    def __str__(self):
        return self.user.username

class Following(models.Model):
    followed_to = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name = 'user_followed')
    followed_by = models.ManyToManyField(CustomUser, related_name = 'user_follower')
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def follow(cls, followed_to, followed_by):
        obj, create = cls.objects.get_or_create(followed_to = followed_to)
        obj.followed_by.add(followed_by)

    @classmethod
    def unfollow(cls, followed_to, followed_by):
        obj, create = cls.objects.get_or_create(followed_to = followed_to)
        obj.followed_by.remove(followed_by)
        
    def __str__(self):
        return self.followed_to.username