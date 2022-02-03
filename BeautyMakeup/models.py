from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class BeautyMakeupItem(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    #mail method
    availability = models.CharField(max_length=200)
    #stocks
    condition = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    item_img = models.ImageField(upload_to='', blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('BeautyMakeup:item-detail', args=[self.id])


admin_user = {"username": "xu", "password": "admin", "role":"Admin"}

class Comment(models.Model):
    author = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commentTitle = models.CharField(max_length=200)
    commentText = models.TextField(blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(BeautyMakeupItem, on_delete=models.CASCADE)


