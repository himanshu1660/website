from django.db import models
from django.db.models import Max
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
User=get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blankprofile.jpg')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

    
class Like_post(models.Model):
    username=models.CharField(max_length=100)
    post_id=models.CharField(max_length=500)

    def __str__(self):
        return self.username
    
class FollowerCount(models.Model):
    follower = models.CharField(max_length = 100)
    user = models.CharField(max_length = 100)

    def __str__(self):
        return self.user
    
class Bookmarks(models.Model):
    username=models.CharField(max_length=100)
    post_id=models.CharField(max_length=500)

    def __str__(self):
        return self.username
    
class Message(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    sender=models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    reciepient=models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    body=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)

    def send_message(from_user, to_user, body):
        sender_message = Message(
            user = from_user,
            sender = from_user,
            reciepient = to_user,
            body = body,
            is_read = True
        )
        sender_message.save()

        reciepient_message = Message(
            user = to_user,
            sender = from_user,
            reciepient = from_user,
            body = body,
            is_read = True
        )
        reciepient_message.save()

        return sender_message
    
    def get_message(user):
        users=[]
        messages = Message.objects.filter(user=user).values('reciepient').annotate(last=Max('date')).order_by('-last')
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['reciepient']),
                'last': message['last'],
                'unread': Message.objects.filter(user=user, reciepient__pk=message['reciepient'], is_read=False).count()
            })
        return users

class Stories(models.Model):
    story_image = models.ImageField(upload_to='post_story')
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user