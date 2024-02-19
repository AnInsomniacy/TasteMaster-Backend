from django.db import models


class Article(models.Model):
    # 文章编号
    article_id = models.AutoField(primary_key=True)
    author_name = models.CharField(max_length=100)
    author_id = models.IntegerField()
    title = models.CharField(max_length=100)
    content = models.TextField()
    image_url = models.CharField(max_length=500,default='https://img2.baidu.com/it/u=1337941324,845441152&fm=253&fmt=auto&app=138&f=JPEG?w=640&h=452')
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)

# Create your models here.
