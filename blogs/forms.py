from django.forms import ModelForm
from django import forms
from .models import Article, Category



choices = Category.objects.all().values_list('name', 'name')
choice_list = []

for i in choices:
    choice_list.append(i)

class ArticleForm(ModelForm):
     class Meta:
         model = Article
         fields = [ 'title', 'description', 'category' , 'image' ]

     widgets = {
        'category' : forms.Select(choices=choice_list , attrs={'class': 'form-control' })
     }
