from django.contrib.auth.models import User
from django.db import models
from djongo import models as djongo_models

class Post(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

    class Meta:
        ordering = ['-created_at']
        
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    def __str__(self):
        return self.user.username  
    
 
class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships2')

    def __str__(self):
        return f'{self.user1.username} - {self.user2.username}'
    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_received')
    is_accepted = models.BooleanField(default=False)

    def accept(self):
        if not self.is_accepted:
            # Update the friend request to mark it as accepted
            self.is_accepted = True
            self.save()

            # You can perform additional actions if needed, e.g., create a Friendship object
            Friendship.objects.create(user1=self.from_user, user2=self.to_user)

    def reject(self):
        # Delete the friend request
        self.delete()

    def __str__(self):
        return f'{self.from_user.username} -> {self.to_user.username}'


'''


class Comment(models.Model):
    post = models.ForeignKey('socialapp.Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

class PostLike(models.Model):
    post = models.ForeignKey('socialapp.Post', on_delete=models.CASCADE, related_name='post_likes')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    '''