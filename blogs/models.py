from django.db import models
from django.contrib.auth.models import User
#from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    #article = models.ManyToManyField(Article)

    def __str__(self):
        return self.name
'''
    #def get_absolute_url(self):  # url name
        # return reverse('article-detail', args=(str(self.id)))
        return reverse('home')
'''

class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='blogs/images/', null=True)
    #updater = models.Charfield
    #dateupdated = models.DateTimeField(null=True, blank=True)



    def __str__(self):
        return self.title
'''
    def get_absolute_url(self):  # url name
        # return reverse('article-detail', args=(str(self.id)))
        return reverse('home')
'''


class Hiring(models.Model):
    name = models.CharField(max_length=200)
    birthday = models.DateField(null=True, blank=True)
    about = models.TextField(max_length=1000)

    # resumefile =

    def __str__(self):
        return self.title