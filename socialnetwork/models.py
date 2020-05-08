from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    userBio = models.CharField(max_length=200)
    profile_picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT, related_name='user_of_profile')
    following = models.ManyToManyField(User)

    def __str__(self):
        return "user_id: {}, user_poc: {}".format(self.user_id, self.profile_picture)


class Post(models.Model):
    poster = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    poster_user_id = models.CharField(max_length=200, default=None)
    poster_name = models.CharField(max_length=200, default=None)
    post_input_text = models.CharField(max_length=200)
    date = models.DateTimeField(blank=True, default=None)

    # def __str__(self):
    #     return 'Posted by ' + self.poster.user_name + ' ' + self.content + ' \n--' + self.date


class Comment(models.Model):
    comment_text = models.CharField(max_length=200)
    post = models.ForeignKey(Post, default=None, on_delete=models.PROTECT)
    post_ref = models.CharField(max_length=200, default=None)
    user_name = models.CharField(max_length=200, default=None)
    user_id = models.CharField(max_length=200, default=None)
    comment_profile = models.ForeignKey(Profile, default=None, on_delete=models.PROTECT, related_name='poster_of_comment')
    comment_user = models.ForeignKey(User, default=None, on_delete=models.PROTECT, related_name='user_of_comment')
    comment_date_time = models.DateTimeField(blank=True, default=None)

    def __str__(self):
        return self.comment_text + "by" + self.user_name
