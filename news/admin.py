from django.contrib import admin
from .models import Editor, Tag, Article

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'editor','pub_date'] # Columns to show in the admin list
    search_fields = ['title','content'] # add search box
    list_filter = ['pub_date'] #add filter sidebar
    filter_horizontal = ['tags'] #for manyTomant fields

#Register models to admin

admin.site.register(Editor)
admin.site.register(Tag)
admin.site.register(Article, ArticleAdmin)