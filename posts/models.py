from django.db import models
from users.models import CustomUser

# Create your models here.
class Category(models.Model):
    name  = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = 'user')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name = 'category')
    title = models.CharField(max_length=255, null=False)
    description = models.TextField()
    views = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title

class Like(models.Model):
    user = models.ManyToManyField(CustomUser, related_name='like_user')
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    # likes = models.IntegerField(default=0)

    @classmethod
    def liked(cls, post, user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.user.add(user)

    @classmethod
    def dislike(cls, post, user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.user.remove(user)

    def __str__(self):
        return self.user.username