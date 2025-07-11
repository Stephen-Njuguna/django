from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
import datetime as dt
from .models import Article

def welcome(request):
    date = dt.date.today()

    context = {'date':date}

    return render (request, 'news\welcome.html',context)

from django.shortcuts import render

def login(request):
    date = dt.date.today()
    context = {
        'user_login': False,
        'date':date
    }
    return render(request, 'news/login.html', context)

def todays_news(request):
    date = dt.date.today()

    news = Article.todays_news()

    context = {
        'date':date,
        'news': news
    }
    return render(request, 'news/todays_news.html',context)

def past_news(request, past_date):
    try:
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()
    except ValueError:
        raise Http404("Invalid date format")

    if date == dt.date.today():
        return redirect(todays_news)

    context = {'date': date}
    return render(request, 'news/past_news.html', context)

def single_article(request, article_id):
    try:
        article = Article.objects.get(id =article_id)
    except Article.DoesNotExist:
        raise Http404
    
    context = { 'article': article}
    return render(request, 'news/article.html', context)
    