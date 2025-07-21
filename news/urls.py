from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns  = [
    path('',views.welcome,name='welcome'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('today/',views.todays_news, name='todays_news'),
    path('archives/<slug:past_date>/', views.past_news, name='past_news'),
    path('today/article/<int:article_id>/', views.single_article, name='article'),
    path('register/', views.register_user, name='register_user'),
    path('newsletter/', views.ajax_newsletter, name='ajax_newsletter'),
    path('api/merch/', views.MerchListView.as_view(), name='merch-list')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
