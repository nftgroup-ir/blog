"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from blogs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name= "home"),
    path('aboutus', views.aboutus, name= "aboutus"),
    # Auth
    path('signup/', views.signupuser, name= 'signupuser'),
    path('login/', views.loginuser, name= 'loginuser'),
    path('logout/', views.logoutuser, name= 'logoutuser'),
    path('hiring/', views.hiringuser, name= 'hiringuser'),
    # Article
    path('create/', views.createarticle, name='createarticle'),
    path('current/', views.currentarticles, name='currentarticles'),
    path('view/<int:article_pk>/', views.viewarticle, name='viewarticle'),
    path('view/<int:article_pk>/update', views.updatearticle, name='updatearticle'),
    path('view/<int:article_pk>/delete', views.deletearticle, name='deletearticle'),
    path('categories/', views.viewcategories, name='viewcategories'),
    path('categories/<str:category_name>/', views.categoryarticles, name='categoryarticles'),
    path('articles/<str:article_pk>', views.viewcategory_article, name='viewcategory_article'),

]
handler404 = 'blogs.views.error_404'
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

