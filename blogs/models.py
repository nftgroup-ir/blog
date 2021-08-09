from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
<<<<<<< Updated upstream
from ckeditor_uploader.fields import RichTextUploadingField
=======
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
    description = RichTextUploadingField()
=======
    description = models.TextField(max_length=1000)
    description = RichTextField(blank=True, null=True)
>>>>>>> Stashed changes
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='blogs/images/', null=True, blank=True)
    #updater = models.Charfield
    #dateupdated = models.DateTimeField(null=True, blank=True)



    def __str__(self):
        return self.title
'''
    def get_absolute_url(self):  # url name
        # return reverse('article-detail', args=(str(self.id)))
        return reverse('home')
'''

class Message(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phonenumber = models.CharField(max_length=200)
    subject = models.CharField(max_length=300)
    message_text = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class Hiring(models.Model):
    name = models.CharField(max_length=200)
    resumefile = models.FileField(upload_to='blogs/documents/', default=False)

    def __str__(self):
        return self.name