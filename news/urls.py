from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns  = [
    path('',views.welcome,name='welcome'),
    path('login/', views.login, name='login'),
    path('today/',views.todays_news, name='todays_news'),
    path('archives/<slug:past_date>/', views.past_news, name='past_news'),
    path('today/article/<int:article_id>/', views.single_article, name='article'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
