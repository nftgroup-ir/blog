from django.db import IntegrityError
from sqlite3 import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework import status
from .forms import ArticleForm , MessageForm, HiringForm
from .models import Article, Wallets
from django.utils import timezone
from .models import Category
from django.core import serializers
import requests
from rest_framework.response import Response
#from django.shortcuts import render_to_response
from rest_framework.decorators import api_view
from django.template import RequestContext
from generativepy.color import Color
from generativepy.drawing import make_image, setup
from generativepy.geometry import Rectangle, Circle

def error_404(request, exception):
    data = {}
    return render(request, 'blogs/404.html', data)


def handler500(request, *args, **argv):
    response = render('500.html', {},context_instance=RequestContext(request))
    response.status_code = 500
    return response



def get_price():
    url = "https://api.nomics.com/v1/currencies/ticker?key=041e0dbf4707ba03ca9759d706dc36299d10515d&ids=BTC,ETH&interval=1h"
    my_api_data = requests.get(url)
    bitcoin_price = (my_api_data.json()[0]['price'])
    ethereum_price = (my_api_data.json()[1]['price'])
    prices = {'bitcoin':bitcoin_price,'ethereum': ethereum_price}
    return prices



def categoriesBase(request):
    articles = Article.objects.order_by('-created')
    listof_articles = []
    if articles == []:
        return({'categories' : Category.objects.all(), 'listof_articles': listof_articles, 'article': "s"})
    else:
        x = 0
        for article in articles:
            if x <= 4:
                listof_articles.append(article)
                x += 1
        return({'categories' : Category.objects.all(), 'listof_articles': listof_articles, 'article': "s"})


def index(request):
  context = {"home_page": "active"} # new info here
  return render(request, 'pages/index.html', context)

def about(request):
  context = {"about_page": "active"} # new info here
  return render(request, 'pages/about.html', context)

def contact(request):
  context = {"contact_page": "active"} # new info here
  return render(request, 'pages/contact.html', context)


def home(request):
    articles = Article.objects.order_by('-created')
    listof_articles=[]
    x=0
    for article in articles:
        if x<=3:
            listof_articles.append(article)
            x+=1
    return render(request, 'blogs/home.html', {'listof_articles':listof_articles, 'article':article , 'price' : get_price() })

def aboutus(request):
    if request.method == 'GET':
        return render(request, 'blogs/aboutus.html' , {'form': MessageForm()})
    else:
        try:
            form = MessageForm(request.POST)
            form.save()
            return render(request, 'blogs/aboutus.html' , {'form': MessageForm(),'msg' : True})
        except ValueError:
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
        return render(request, 'blogs/hiringuser.html', {'form': HiringForm()})
    elif request.method == 'POST':
        try:
            form = HiringForm(request.POST, request.FILES)
            form.save()
            return render(request, 'blogs/hiringuser.html',{'form': HiringForm(), 'msg' : True})
        except IntegrityError:
            return render(request, 'blogs/hiringuser.html',{'form': HiringForm(), 'error': 'اشتباهی رخ داده است'})


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
    articles = Article.objects.order_by('-created')
    p = Paginator(articles, 3)
    page_num = request.GET.get('page')
    page =p.get_page(page_num)
    return render(request, 'blogs/currentarticles.html', {'page':page, 'articles':articles})

    # articles = Article.objects.all()
    # p = Paginator(articles, 3)
    # return render(request, 'blogs/currentarticles.html', {'articles':articles})

def viewarticle(request, article_pk):
    article = get_object_or_404(Article, pk = article_pk)
    return render(request, 'blogs/viewarticle.html', {'article': article})


@login_required
def updatearticle(request, article_pk):
    article = get_object_or_404(Article, pk = article_pk)
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
        return render(request, 'blogs/categoryarticles.html', {'articles':articles, 'mylist' : mylist  })

def viewcategory_article(request, article_pk):     #SEE FULL ARTICLE OF A CATEGORY
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'GET':
        return render(request, 'blogs/viewarticle.html', {'article': article})

@api_view(['POST'])
def walletimage(request):
    wallet = request.data['address']
    wallet = wallet[2:120]
    f = ""
    for character in wallet:
        a = str(ord(character))
        if len(a) == 1:
            a = "00" + a
        elif len(a) == 2:
            a = "0" + a
        f = f + a

    def dayere(ctx, a, b, c, op, sizey):
        color = Color(a, b, c, op)
        Circle(ctx).of_center_radius((250, 250), sizey).fill(color)

    def draw(ctx, pixel_width, pixel_height, frame_no, frame_count):
        setup(ctx, pixel_width, pixel_height, background=Color(1))
        radius = 150
        for j in range(0, 119, 8):
            number1 = "0." + f[j] + f[j + 1]
            number2 = "0." + f[j + 2] + f[j + 3]
            number3 = "0." + f[j + 4] + f[j + 5]
            number4 = "0.9" + f[j + 6] + f[j + 7]
            dayere(ctx, float(number1), float(number2), float(number3), float(number4), radius)  #
            print(number1, number2, number3, number4)
            radius -= 10

    make_image(wallet+".png", draw, 500, 500)
    x = wallet+".png"
    return Response({"address":x}, status=status.HTTP_201_CREATED)











