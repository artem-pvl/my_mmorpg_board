from django.db import models
from django.contrib import auth

from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Ad(models.Model):
    user_id = models.ForeignKey(auth.get_user_model(),
                                on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    ad = RichTextUploadingField(default='')
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.header


class Reply(models.Model):
    user_id = models.ForeignKey(auth.get_user_model(),
                                on_delete=models.CASCADE)
    ad_id = models.ForeignKey(Ad, on_delete=models.CASCADE)
    reply = models.TextField(default='')
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reply
