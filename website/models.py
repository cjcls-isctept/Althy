from django.db import models
import datetime
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django import forms
from PIL import Image

class User(models.Model):
    email =models.CharField(max_length=40)
    username =models.CharField(max_length=20)
    password =models.CharField(max_length=20)
    reg_date = models.DateTimeField('data de registo')
    bio = models.TextField(max_length=300)
    avatar = models.ImageField(upload_to='user/',default='user/noAvatar.png')
    comment_listing=models.IntegerField()
    def __str__(self):
        return self.username
    def foi_criado_recentemente(self):
	    return self.reg_data >= timezone.now() - datetime.timedelta(days=1)

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    text = models.TextField(max_length=10000)
    post_date = models.DateTimeField('data de criação')
    upvotes = models.IntegerField()
    topic = models.CharField(max_length=20)
    upvoteList= models.TextField(null=True)
    downvoteList=models.TextField(null=True)
    was_upvoted=models.IntegerField()
    was_downvoted=models.IntegerField()
    image=models.ImageField(upload_to='',default='notFound.png')
    youtube_url=models.CharField(max_length=50)
    preview_text=models.CharField(max_length=200)
    video_preview=models.IntegerField()
    def __str__(self):
        return self.title
    def foi_criado_recentemente(self):
	    return self.post_data >= timezone.now() - datetime.timedelta(days=1)

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    post_title=models.CharField(max_length=40)
    text = models.TextField(max_length=1000)
    comm_date = models.DateTimeField('data do comentário')
    upvotes = models.IntegerField()
    upvoteList= models.TextField(null=True)
    downvoteList=models.TextField(null=True)
    was_upvoted=models.IntegerField(null=0)
    was_downvoted=models.IntegerField(null=0)
    was_read=models.IntegerField(null=0)
    poster_username=models.CharField(max_length=20)
    def __str__(self):
        return self.text
    def foi_criado_recentemente(self):
	    return self.comm_data >= timezone.now() - datetime.timedelta(days=1)

class Message(models.Model):
    sender_user=models.ForeignKey(User,on_delete=models.CASCADE)
    receiver_user_id=models.IntegerField()
    subject=models.CharField(max_length=40)
    text=models.TextField(max_length=1000)
    mess_date=models.DateTimeField('data da mensagem')
    was_read=models.IntegerField(null=0)
    sender_user_username=models.CharField(max_length=20)
    def __str__(self):
        return self.text
    def foi_criado_recentemente(self):
	    return self.comm_data >= timezone.now() - datetime.timedelta(days=1)


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image= forms.ImageField()