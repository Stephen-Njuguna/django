from django.db import models
from django.utils import timezone

# Create your models here.
class Editor(models.Model):
    first_name= models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10, blank=True)

    def save_editor(self):
        self.save()

    def __str__(self):
        return self.first_name
    
class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=60)
    content = models.TextField()
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='articles')
    article_image = models.ImageField(upload_to='articles/', blank=True, null=True)


    def __str__(self):
        return self.title
    
    @classmethod
    def todays_news(cls):
        today = timezone.now().date()
        return cls.objects.filter(pub_date__date=today)