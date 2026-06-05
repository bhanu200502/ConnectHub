from django.db import models
from django.contrib.auth.models import User

# User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_followers_count(self):
        return Follower.objects.filter(following=self.user).count()

    def get_following_count(self):
        return Follower.objects.filter(follower=self.user).count()

    def get_posts_count(self):
        return Post.objects.filter(user=self.user).count()


# Post Model
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True
    )
    caption = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s post - {self.created_at}"

    def get_likes_count(self):
        return Like.objects.filter(post=self).count()

    def get_comments_count(self):
        return Comment.objects.filter(post=self).count()

    class Meta:
        ordering = ['-created_at']


# Comment Model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.post.id}"

    class Meta:
        ordering = ['-created_at']


# Like Model
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"

    class Meta:
        unique_together = ('user', 'post')


# Follower Model
class Follower(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

    class Meta:
        unique_together = ('follower', 'following')