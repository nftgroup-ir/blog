from django.db import IntegrityError
from sqlite3 import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from .models import Article
from django.utils import timezone
from .models import Category



def categories():
    return Category.objects.all()


def home(request):
    articles = Article.objects.order_by('-created')
    listof_articles=[]
    x=0
    for article in articles:
        if x<=3:
            listof_articles.append(article)
            x+=1
    return render(request, 'blogs/home.html', {'listof_articles':listof_articles})

def aboutus(request):
    return render(request, 'blogs/aboutus.html')



def signupuser(request):
    if request.method == 'GET' :
        return render(request, 'blogs/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('home')
                except IntegrityError:
                    return render(request, 'blogs/signupuser.html', {'form':UserCreationForm(), 'error':'The user name has already been taken'})
        else:
            return render(request, 'blogs/signupuser.html', {'form':UserCreationForm(), 'error':'passwords did not match'})


def loginuser(request):
    if request.method == 'GET' :
        return render(request, 'blogs/loginuser.html' , {'form':AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'] , password=request.POST['password'])
        if user is None:
            return render(request, 'blogs/loginuser.html', {'form':AuthenticationForm, 'error':'username and password did not match'})
        else:
            login(request, user)
            return redirect('currentarticles')

@login_required
def logoutuser(request):
    if request.method == 'POST' :
        logout(request)
        return redirect('home')

def hiringuser(request):
    if request.method == 'GET':
        return render(request, 'blogs/hiringuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'blogs/hiringuser.html',
                                {'form': UserCreationForm(), 'error': 'The user name has already been taken'})
        else:
            return render(request, 'blogs/hiringuser.html',
                            {'form': UserCreationForm(), 'error': 'passwords did not match'})

@login_required
def createarticle(request):
    if request.method == 'GET' :
        return render(request, 'blogs/createarticle.html', { 'form': ArticleForm() })
    else:
        try:
            form = ArticleForm(request.POST,request.FILES)
            newarticle = form.save(commit=False)
            newarticle.user = request.user
            newarticle.save()
            newarticle.category.add( *request.POST.getlist("category"))
            return redirect('currentarticles')
        except ValueError:
            return render(request, 'blogs/createarticle.html', { 'form': ArticleForm() , 'error' : 'Bad data passed in'})


def currentarticles(request):
    articles = Article.objects.all()
    return render(request, 'blogs/currentarticles.html', {'articles':articles})


def viewarticle(request, article_pk):
    article = get_object_or_404(Article, pk = article_pk)
    return render(request, 'blogs/viewarticle.html', {'article': article})


@login_required
def updatearticle(request, article_pk):
    article = get_object_or_404(Article, pk = article_pk, user=request.user)
    if request.method == 'GET':
        form = ArticleForm(instance=article)
        return render(request, 'blogs/updatearticle.html', {'article': article, 'form':form })
    else:
        try:
            form = ArticleForm(request.POST, instance=article)
            article.updated = timezone.now()
            form.save()
            return redirect('currentarticles')
        except ValueError:
            return render(request, 'blogs/updatearticle.html', {'article': article, 'form': form , 'error':'Badinfo'})

@login_required
def deletearticle(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk, user=request.user)
    if request.method == 'POST':
        article.delete()
        return redirect(currentarticles)

def viewcategories(request):
    categories = Category.objects.all()
    return render(request,'blogs/viewcategories.html', {'categories':categories})


def categoryarticles(request,category_name):
    if request.method == 'GET':
        articles = Article.objects.all()
        mylist = []
        for article in Article.objects.all():
            for cat in article.category.all():
                if category_name == cat.name:
                    mylist.append(article)
        return render(request, 'blogs/categoryarticles.html', {'articles':articles, 'mylist' : mylist })

def viewcategory_article(request, article_pk):     #SEE FULL ARTICLE OF A CATEGORY
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'GET':
        return render(request, 'blogs/viewarticle.html', {'article': article})

'''''
def postcategoryarticles(request, category_pk):                #VIEW ARTICLE THROUGH POST
    if request.method == 'POST':
        articles = Article.objects.all()
        mylist = []
        for article in Article.objects.all():
            for cat in article.category.all():
                if category_pk == cat.id:
                    mylist.append(article)
        return render(request, 'blogs/postcategoryarticles.html', {'articles':articles,'category_pk':category_pk, 'mylist' : mylist })
else:
        articles = Article.objects.all()
        mylist = []
        for article in Article.objects.all():
            for cat in article.category.all():
                if category_name == cat.name:
                    mylist.append(article)
        return render(request, 'blogs/categoryarticles.html',
                      {'articles': articles, 'category_name': category_name, 'mylist': mylist})
'''''














