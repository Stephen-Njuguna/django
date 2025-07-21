from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
import datetime as dt
from .models import Article, NewsLetterRecipients,Editor, Merch
from .forms import NewsLetterForm, CustomUserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .serializers import MerchSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAdminOrReadOnly




def welcome(request):
    date = dt.date.today()
    user = request.user
    context = {
        'date':date,
        'user':user
        }

    return render (request, 'news\welcome.html',context)


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            login(request,form.get_user())
            return redirect('todays_news')
    else:
        form = AuthenticationForm()

    context = {
        'form':form
    }
    return render(request, 'registration/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('welcome')

@login_required(login_url='login')
def todays_news(request):
    date = dt.date.today()

    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
    else:
        form = NewsLetterForm()

    news = Article.todays_news()

    context = {
        'date':date,
        'news': news,
        'form':form
        
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

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["username"]
            email = form.cleaned_data["email"]

            # Save editor record
            Editor.objects.create(first_name=name, email=email)

            # Save Django user
            form.save()

            # Send welcome email
            send_mail(
                'Welcome!',
                f'Thanks {name}, for registering with Tribune.',
                'stephenjuguna7828@gmail.com',
                [email],
                fail_silently=False
            )

            return redirect('welcome')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/registration_form.html', {'form': form})


@csrf_exempt
def ajax_newsletter(request):
    if request.method == 'POST':
        name = request.POST.get('your_name')
        email = request.POST.get('email')

        if not name or not email:
            return JsonResponse({'error': 'Missing name or email.'}, status=400)

        recipient = NewsLetterRecipients(name=name, email=email)
        recipient.save()

        send_mail(
            'Thank you for Subscribing',
            f'Hello {name},\nWelcome to the Tribune newsletter.\nWe will keep you updated.',
            'stephenjuguna7828@gmail.com',
            [email],
            fail_silently=False
        )

        return JsonResponse({'success': f'Thank you, {name}! You have subscribed.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)



class MerchListView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        merch_items = Merch.objects.all()
        serializer = MerchSerializer(merch_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MerchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# #Token generations permissions
# class MerchListView(APIView):
#     permission_classes = [IsAdminOrReadOnly]
    