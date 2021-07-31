from django.forms import ModelForm
from django import forms
from .models import Article, Category , Message, Hiring



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

class MessageForm(ModelForm):
     class Meta:
        model = Message
        fields = [ 'name', 'email', 'phonenumber' , 'subject' , 'message_text' ]

     name =forms.CharField(widget=forms.TextInput(
         attrs={
         'class':'form-control',
         'placeholder':'نام شما',
         'required data-error':'لطفا نام خود را وارد کنید'
         }
    ))
     email =forms.CharField(widget=forms.TextInput(
         attrs={
         'class':'form-control',
         'placeholder':'ایمیل شما',
         'required data-error':'لطفا ایمیل خود را وارد کنید'
         }
    ))
     phonenumber =forms.CharField(widget=forms.TextInput(
         attrs={
         'class':'form-control',
         'placeholder':'تلفن شما',
         'required data-error':'لطفا تلفن خود را وارد کنید'
         }
    ))
     subject =forms.CharField(widget=forms.TextInput(
         attrs={
         'class':'form-control',
         'placeholder':'موضوع شما',
         'required data-error':'لطفا موضوع خود را وارد کنید'
         }
    ))
     message_text =forms.CharField(widget=forms.TextInput(
         attrs={
         'class':'form-control',
         'placeholder':'پیام شما',
         'required data-error':'پیام خود را بنویسید'
         }
    ))

class HiringForm(ModelForm):
     class Meta:
         model = Hiring
         fields = [ 'name', 'resumefile' ]
