from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse

from account_manager.models import DataLinker
from article_manager.models import Article
from get_jwt.jwt_controller import validate_access_jwt_intern


def create_article(request):
    access_token = request.POST.get('access_token')
    article_title = request.POST.get('article_title')
    article_content = request.POST.get('article_content')
    image_url = request.POST.get('image_url')
    if request.method == 'POST':
        # 校验access_token
        validate_result = validate_access_jwt_intern(access_token)
        if validate_result[0]:
            current_user_str = validate_result[1]

            current_user = User.objects.get(username=current_user_str)

            current_user_id = current_user.id

            # 建立Article对象
            article = Article(author_id=current_user_id, title=article_title, content=article_content,
                              author_name=current_user_str, image_url=image_url)
            article.save()

            article_id = article.article_id

            # 建立DataLinker对象
            table = DataLinker.objects.get_or_create(user_id=current_user_id)
            table[0].article_list.add(article_id)

            # 返回JsonResponse，包含文章的标题，作者和编号
            return JsonResponse({'result': 'success', '文章标题:': article_title, '文章作者:': current_user_str,
                                 '文章编号:': article_id, '图片url': image_url})
        else:
            return JsonResponse({'result': '失败', 'reason': validate_result[1]})
    else:
        return JsonResponse({'result': 'fail', 'reason': '请求方式错误'})


# 获取单个用户的文章列表
def show_articles(request):
    user_id = request.POST.get('user_id')
    if request.method == 'POST':
        # 根据user_id获取user对象
        try:
            user = User.objects.get(id=user_id)
        except:
            return JsonResponse({'result': '获取文章列表失败，用户不存在'})

        current_user = User.objects.get(id=user_id)
        current_user_id = current_user.id

        # 为current_user新建DataLinker对象，如果已存在，则不新建
        DataLinker.objects.get_or_create(user_id=current_user_id)

        # 获取current_user的DataLinker对象
        current_user_data_linker = DataLinker.objects.get(user_id=current_user_id)

        # 把article_list转换成一个新建的列表，列表里的元素包含模型Article里的title、content、author、create_time、update_time
        article_list = current_user_data_linker.article_list.all()
        article_list_str = []
        for article in article_list:
            article_list_str.append(
                {'article_id': article.article_id, 'article_title': article.title, 'image_url': article.image_url,
                 'article_author': article.author_name,
                 'create_time': article.create_time, 'update_time': article.update_time})

        # Return success and indicate the number of articles
        return JsonResponse(
            {'result': '成功获取文章信息', 'user_id': user.id, 'username': user.username,
             'article_count': len(article_list_str),
             'article_list': article_list_str})


    else:
        return JsonResponse({'result': '仅支持POST调用，获取文章列表失败'})


# 根据文章id获取文章
def show_article_by_id(request):
    article_id = request.POST.get('article_id')
    if request.method == 'POST':
        try:
            article = Article.objects.get(article_id=article_id)
        except:
            return JsonResponse({'result': '获取文章失败，文章不存在'})

            # 进一步获取文章的作者、标题、内容、创建时间、更新时间
        article_id = article.article_id
        article_author = article.author_name
        article_title = article.title
        article_content = article.content
        article_create_time = article.create_time
        article_update_time = article.update_time

        # 整合文章信息为列表
        article_info = {'article_id': article_id, 'author_id': article.author_id, 'author': article_author,
                        'title': article_title,
                        'article_img_url': article.image_url,
                        'content': article_content, 'created_time': article_create_time,
                        'updated_time': article_update_time}

        # 返回成功，并包含上述列表
        return JsonResponse({'result': 'success', 'article_list': article_info})
    else:
        return JsonResponse({'result': '仅支持POST调用，获取文章失败'})


# 随机返回十篇文章
def get_random_ten_articles(request):
    # 随即返回Article表中的十篇文章
    # GET方法
    if request.method == 'GET':
        # 无需校验access_token
        # 获取Article表中随机10篇文章
        article_list = Article.objects.order_by('?')[:10]
        article_list_str = []
        for article in article_list:
            article_list_str.append(
                {'文章id': article.article_id, '文章标题': article.title, '图片url': article.image_url,
                 '文章内容': article.content,
                 '文章作者': article.author_name,
                 '创建时间': article.create_time, '更新时间': article.update_time})
        # 返回成功，同时返回上述列表
        return JsonResponse(
            {'result': '获取文章列表成功', '文章数目': len(article_list_str), '文章列表': article_list_str})
    else:
        return JsonResponse({'result': '仅支持GET调用，获取文章列表失败'})


# 根据文章id修改文章
def update_article_by_id(request):
    # 根据文章编号更新文章
    access_token = request.POST.get('access_token')
    # 只允许更新自己的文章
    article_id = request.POST.get('article_id')
    article_title = request.POST.get('article_title')
    article_content = request.POST.get('article_content')
    image_url = request.POST.get('image_url')
    if request.method == 'POST':
        # 判断文章是否存在
        try:
            article = Article.objects.get(article_id=article_id)
        except:
            return JsonResponse({'result': '文章不存在，更新失败'})
        # 检查文章作者是否为当前用户
        if article.author_name != validate_access_jwt_intern(access_token)[1]:
            return JsonResponse({'result': '文章作者不是当前用户，更新失败'})
        # 更新文章
        article.title = article_title
        article.content = article_content
        article.image_url = image_url
        article.save()
        return JsonResponse({'result': '更新文章成功', 'article_id': article_id, 'article_title': article_title,})
    else:
        return JsonResponse({'result': '仅支持POST调用，更新文章失败'})


def delete_article_by_id(request):
    # 根据文章编号删除文章
    access_token = request.POST.get('access_token')
    # 只允许删除自己的文章
    article_id = request.POST.get('article_id')
    if request.method == 'POST':
        # 判断文章是否存在
        try:
            article = Article.objects.get(article_id=article_id)
        except:
            return JsonResponse({'result': '文章不存在，删除失败'})
        # 检查文章作者是否为当前用户
        if article.author_name != validate_access_jwt_intern(access_token)[1]:
            return JsonResponse({'result': '文章作者不是当前用户，删除失败'})
        # 删除文章
        article.delete()
        return JsonResponse({'result': '删除文章成功', 'article_id': article_id})
    else:
        return JsonResponse({'result': '仅支持POST调用，删除文章失败'})


# 根据关键字搜索文章，关键字匹配标题或作者的一部分或者全部都行
def search_article_by_keyword(request):
    # 仅支持POST调用
    if request.method == 'POST':
        # 获取关键字
        keyword = request.POST.get('keyword')
        # 获取文章列表，匹配标题或author_name的一部分或者全部，不区分大小写
        try:
            article_list = Article.objects.filter(Q(title__icontains=keyword) | Q(author_name__icontains=keyword))
        except:
            return JsonResponse({'result': '获取文章列表失败'})
        article_list_str = []
        for article in article_list:
            article_list_str.append(
                {'文章id': article.article_id, '文章标题': article.title, '作者id': article.author_id,
                 '文章作者': article.author_name,
                 '图片url': article.image_url,
                 '文章内容': article.content,
                 '创建时间': article.create_time, '更新时间': article.update_time})
        # 返回成功，并且说明文章数目
        return JsonResponse(
            {'result': '获取文章列表成功', '文章数': len(article_list_str), '文章列表': article_list_str})
    else:
        return JsonResponse({'result': '仅支持POST调用，获取文章列表失败'})
