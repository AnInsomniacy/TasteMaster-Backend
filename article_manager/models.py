from django.db import models


class Article(models.Model):
    # 文章编号
    article_id = models.AutoField(primary_key=True)
    author_name = models.CharField(max_length=100)
    author_id = models.IntegerField()
    title = models.CharField(max_length=100)
    content = models.TextField()
    image_url = models.CharField(max_length=500,default='https://5b0988e595225.cdn.sohucs.com/images/20191217/110701b9a43b413883c5c104d818dd91.jpeg')
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)

# Create your models here.
