from django.contrib import admin
from .models import Article
from .models import Category
from .models import Hiring

#class ArticleAdmin(admin.ModelAdmin):
   # readonly_fields = ('created',)

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Hiring)
#admin.site.register(ArticleAdmin)


