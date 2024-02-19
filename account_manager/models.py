from django.db import models


# Create your models here.


class DataLinker(models.Model):
    # userid设置为主键，因为userid是唯一的
    user_id = models.IntegerField(primary_key=True)

    followed_user_list = models.ManyToManyField('self', symmetrical=False, related_name='followed_user_list_str')

    article_list = models.ManyToManyField('article_manager.Article', symmetrical=False, related_name='article_list_str')

    # avatar_url代表头像的url
    avatar_url = models.CharField(max_length=1000,
                                  default='https://qiniu.jingpin365.com/uploads/weibo/201912/9e16d1d636af8434d50e1241bb59163e.jpeg')

    # self_introduction代表用户的自我介绍
    self_introduction = models.CharField(max_length=1000, default='这个人很懒，什么都没有留下')
