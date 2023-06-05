from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from account_manager.models import DataLinker
from article_manager.models import Article
from get_jwt.jwt_controller import validate_access_jwt_intern


@csrf_exempt
def get_user_list(request, page_begin, page_end):
    if request.method == 'GET':
        # 按页码，获取user数据库里的10个用户,只获取username和last_login字段，并按last_login降序排列，一一对应
        user_list = User.objects.all().order_by('-last_login').values('username', 'last_login')[page_begin:page_end]
        return JsonResponse({'result': '获取用户列表成功', 'user_list': list(user_list)})
    else:
        return JsonResponse({'result': '仅支持GET调用，获取用户列表失败'})


@csrf_exempt
def follow_user(request):
    access_token = request.POST.get('access_token')
    follow_user_id = request.POST.get('follow_user_id')
    if request.method == 'POST':
        # 校验access_token
        validate_result = validate_access_jwt_intern(access_token)
        if validate_result[0]:
            try:
                current_user_str = validate_result[1]

                current_user = User.objects.get(username=current_user_str)
                follow_user = User.objects.get(id=follow_user_id)

                current_user_id = current_user.id
                follow_user_id = follow_user.id

                # 为current_user新建DataLinker对象，如果已存在，则不新建
                DataLinker.objects.get_or_create(user_id=current_user_id)

                # 为follow_user新建DataLinker对象，如果已存在，则不新建
                DataLinker.objects.get_or_create(user_id=follow_user_id)

                # 获取current_user的DataLinker对象
                current_user_data_linker = DataLinker.objects.get(user_id=current_user_id)
                current_user_data_linker.followed_user_list.add(follow_user_id)
                current_user_data_linker.save()

                # 返回成功，并且注明谁关注了谁
                return JsonResponse(
                    {'result': '关注用户成功', 'current_user': current_user_str, 'follow_user': follow_user_id})
            except Exception as e:
                return JsonResponse({'result': '关注用户失败', 'reason': '用户不存在'})
        else:
            return JsonResponse({'result': 'access_token校验失败，关注用户失败', 'reason': validate_result[1]})
    else:
        return JsonResponse({'result': '仅支持POST调用，关注用户失败'})


@csrf_exempt
def unfollow_user(request):
    access_token = request.POST.get('access_token')
    unfollow_user_id = request.POST.get('unfollow_user_id')
    if request.method == 'POST':
        # 校验access_token
        validate_result = validate_access_jwt_intern(access_token)
        if validate_result[0]:
            try:
                current_user_str = validate_result[1]

                current_user = User.objects.get(username=current_user_str)
                unfollow_user = User.objects.get(id=unfollow_user_id)

                current_user_id = current_user.id
                unfollow_user_id = unfollow_user.id

                # 为current_user新建DataLinker对象，如果已存在，则不新建
                DataLinker.objects.get_or_create(user_id=current_user_id)

                # 为unfollow_user新建DataLinker对象，如果已存在，则不新建
                DataLinker.objects.get_or_create(user_id=unfollow_user_id)

                # 获取current_user的DataLinker对象
                current_user_data_linker = DataLinker.objects.get(user_id=current_user_id)
                current_user_data_linker.followed_user_list.remove(unfollow_user_id)
                current_user_data_linker.save()

                # 返回成功，并且注明谁取消关注了谁
                return JsonResponse(
                    {'result': '取消关注用户成功', 'current_user': current_user_str,
                     'unfollow_user': unfollow_user_id})
            except Exception as e:
                return JsonResponse({'result': '取消关注用户失败', 'reason': '用户不存在'})
        else:
            return JsonResponse({'result': 'access_token校验失败，取消关注用户失败', 'reason': validate_result[1]})
    else:
        return JsonResponse({'result': '仅支持POST调用，取消关注用户失败'})


def update_user_info(request):
    access_token = request.POST.get('access_token')
    if request.method == 'POST':
        # 校验access_token
        validate_result = validate_access_jwt_intern(access_token)
        if validate_result[0]:
            current_user_str = validate_result[1]

            current_user = User.objects.get(username=current_user_str)
            current_user_id = current_user.id

            # 为current_user新建DataLinker对象，如果已存在，则不新建
            current_user_data_linker = DataLinker.objects.get_or_create(user_id=current_user_id)[0]

            # 获取用户信息avatar_url和self_indroduction
            avatar_url = request.POST.get('avatar_url')
            self_indroduction = request.POST.get('self_indroduction')

            # 更新用户信息
            current_user_data_linker.avatar_url = avatar_url
            current_user_data_linker.self_indroduction = self_indroduction
            current_user_data_linker.save()

            # 返回成功，注明更新的信息
            return JsonResponse(
                {'result': '更新用户信息成功', 'current_user': current_user_str, 'avatar_url': avatar_url,
                 'self_indroduction': self_indroduction})

        else:
            return JsonResponse({'result': 'access_token校验失败，更新用户信息失败', 'reason': validate_result[1]})
    else:
        return JsonResponse({'result': '仅支持POST调用，更新用户信息失败'})


def get_current_user_info(request):
    access_token = request.POST.get('access_token')
    if request.method == 'POST':
        # 校验access_token
        validate_result = validate_access_jwt_intern(access_token)
        if validate_result[0]:
            current_user_str = validate_result[1]

            current_user = User.objects.get(username=current_user_str)
            current_user_id = current_user.id

            # 为current_user新建DataLinker对象，如果已存在，则不新建
            current_user_data_linker = DataLinker.objects.get_or_create(user_id=current_user_id)[0]

            # 获取用户信息avatar_url和self_introduction
            avatar_url = current_user_data_linker.avatar_url
            self_introduction = current_user_data_linker.self_introduction

            # 获取用户的被关注数和关注数
            followed_user_list = current_user_data_linker.followed_user_list.all()
            followed_user_num = len(followed_user_list)  # 指定用户关注的用户数
            follower_user_list = DataLinker.objects.filter(followed_user_list=current_user_id)
            follower_user_num = len(follower_user_list)  # 指定用户的粉丝数

            # 获取用户发布的文章数
            article_list = Article.objects.filter(author_id=current_user_id)
            article_num = len(article_list)

            # 获取用户id
            user_id = current_user.id

            # 返回成功，并包含上述内容
            return JsonResponse({'result': '获取用户信息成功', '当前用户id': user_id, '当前用户名': current_user_str,
                                 '头像链接': avatar_url,
                                 '自我介绍': self_introduction, '关注数': followed_user_num,
                                 '粉丝数': follower_user_num, '文章数': article_num})

        else:
            return JsonResponse({'result': '获取用户信息失败', 'reason': validate_result[1]})
    else:
        return JsonResponse({'result': '仅支持POST调用，获取用户信息失败'})


# 提取用户的关注列表
def show_followers(request):
    user_id = request.POST.get('user_id')
    if request.method == 'POST':
        try:
            current_user = User.objects.get(id=user_id)
            current_user_id = current_user.id
        except Exception as e:
            return JsonResponse({'result': '获取用户关注列表失败', 'reason': '用户不存在'})

        # 为current_user新建DataLinker对象，如果已存在，则不新建
        DataLinker.objects.get_or_create(user_id=current_user_id)

        # 获取current_user的DataLinker对象
        current_user_data_linker = DataLinker.objects.get(user_id=current_user_id)
        followed_user_list = current_user_data_linker.followed_user_list.all()

        # 把followed_user_list转换成一个新建的列表，列表里的元素是followed_user_list里的每个元素的username
        followed_user_id_list_str = []
        for followed_user in followed_user_list:
            followed_user_id_list_str.append(followed_user.user_id)

        # 根据followed_user_id_list_str，获取用户的avatar_url、self_introduction、被关注数和关注数、获取用户发布的文章数和用户名
        followed_user_info_list = []
        for followed_user_id in followed_user_id_list_str:
            followed_user_data_linker = DataLinker.objects.get(user_id=followed_user_id)
            # 用User表获取username
            followed_user_username = User.objects.get(id=followed_user_id).username
            followed_user_avatar_url = followed_user_data_linker.avatar_url
            followed_user_self_introduction = followed_user_data_linker.self_introduction
            followed_user_followed_user_list = followed_user_data_linker.followed_user_list.all()
            followed_user_followed_user_num = len(followed_user_followed_user_list)  # 指定用户关注的用户数
            followed_user_follower_user_list = DataLinker.objects.filter(followed_user_list=followed_user_id)
            followed_user_follower_user_num = len(followed_user_follower_user_list)  # 指定用户的粉丝数
            followed_user_article_list = Article.objects.filter(author_id=followed_user_id)
            followed_user_article_num = len(followed_user_article_list)
            followed_user_info_list.append({'当前用户名': followed_user_username, '当前用户id': followed_user_id,
                                            '头像链接': followed_user_avatar_url,
                                            '自我介绍': followed_user_self_introduction,
                                            '关注数': followed_user_followed_user_num,
                                            '粉丝数': followed_user_follower_user_num,
                                            '文章数': followed_user_article_num})
        # 返回成功，并包含上述内容
        return JsonResponse({'result': '获取关注用户列表成功', 'followed_user_info_list': followed_user_info_list})

    else:
        return JsonResponse({'result': '仅支持POST调用，获取关注用户列表失败'})


def get_user_info_by_id(request):
    user_id = request.POST.get('user_id')
    if request.method == 'POST':
        # 根据user_id获取用户
        try:
            current_user = User.objects.get(id=user_id)
        except:
            return JsonResponse({'result': '获取失败，用户不存在'})

        current_user_id = current_user.id

        # 为current_user新建DataLinker对象，如果已存在，则不新建
        current_user_data_linker = DataLinker.objects.get_or_create(user_id=current_user_id)[0]

        # 获取用户信息avatar_url和self_introduction
        avatar_url = current_user_data_linker.avatar_url
        self_introduction = current_user_data_linker.self_introduction

        # 获取用户的被关注数和关注数
        followed_user_list = current_user_data_linker.followed_user_list.all()
        followed_user_num = len(followed_user_list)  # 指定用户关注的用户数
        follower_user_list = DataLinker.objects.filter(followed_user_list=current_user_id)
        follower_user_num = len(follower_user_list)  # 指定用户的粉丝数

        # 获取用户发布的文章数
        article_list = Article.objects.filter(author_id=current_user_id)
        article_num = len(article_list)

        # 获取用户id
        user_id = current_user.id

        current_user_str = current_user.username

        # 返回成功，并包含上述内容
        return JsonResponse({'result': '获取用户信息成功', '当前用户id': user_id, '当前用户名': current_user_str,
                             '头像链接': avatar_url,
                             '自我介绍': self_introduction, '关注数': followed_user_num,
                             '粉丝数': follower_user_num, '文章数': article_num})
    else:
        return JsonResponse({'result': '仅支持POST调用，获取用户信息失败'})


# 输入一个数字user_num，返回user_num个用户的信息，按照粉丝数排序
def get_user_info_by_follower_num(request):
    # 仅支持POST调用
    if request.method == 'POST':
        # 获取数字n
        user_num = request.POST.get('user_num')
        # 通过数据库指令，获取user_num个用户的信息，按照最后登录时间排序
        user_num=int(user_num)
        user_list = User.objects.order_by('-last_login')[:user_num]
        #转成user_id_list
        user_id_list = []
        for user in user_list:
            user_id_list.append(user.id)

        # 获取用户的avatar_url、self_introduction、被关注数和关注数、获取用户发布的文章数和用户名
        user_info_list = []
        for user_id in user_id_list:
            # 为current_user新建DataLinker对象，如果已存在，则不新建
            current_user_data_linker = DataLinker.objects.get_or_create(user_id=user_id)[0]

            # 获取用户信息avatar_url和self_introduction
            avatar_url = current_user_data_linker.avatar_url
            self_introduction = current_user_data_linker.self_introduction

            # 获取用户的被关注数和关注数
            followed_user_list = current_user_data_linker.followed_user_list.all()
            followed_user_num = len(followed_user_list)

            follower_user_list = DataLinker.objects.filter(followed_user_list=user_id)
            follower_user_num = len(follower_user_list)

            # 获取用户发布的文章数
            article_list = Article.objects.filter(author_id=user_id)
            article_num = len(article_list)

            # 获取用户名
            current_user = User.objects.get(id=user_id)
            current_user_str = current_user.username

            user_info_list.append({'当前用户名': current_user_str, '当前用户id': user_id, '头像链接': avatar_url,
                                      '自我介绍': self_introduction, '关注数': followed_user_num,
                                        '粉丝数': follower_user_num, '文章数': article_num})


        # 返回成功，并包含上述内容
        return JsonResponse({'result': '获取用户信息成功', 'user_info_list': user_info_list})
    else:
        return JsonResponse({'result': '仅支持POST调用，获取用户信息失败'})


# 判定current_user是否关注了user_id
def is_followed(request):
    if request.method == 'POST':
        access_token = request.POST.get('access_token')
        user_id = request.POST.get('user_id')
        # 校验access_token
        validate_result = validate_access_jwt_intern(access_token)
        if validate_result[0]:
            # 获取当前用户
            current_user_str = validate_result[1]
            current_user = User.objects.get(username=current_user_str)
            current_user_id = current_user.id

            # 获取当前用户的DataLinker对象
            current_user_data_linker = DataLinker.objects.get_or_create(user_id=current_user_id)[0]

            # 为current_user新建DataLinker对象，如果已存在，则不新建
            DataLinker.objects.get_or_create(user_id=current_user_id)

            # 获取current_user的DataLinker对象
            current_user_data_linker = DataLinker.objects.get(user_id=current_user_id)
            followed_user_list = current_user_data_linker.followed_user_list.all()

            # 把followed_user_list转换成一个新建的列表，列表里的元素是followed_user_list里的每个元素的username
            followed_user_id_list_str = []
            for followed_user in followed_user_list:
                followed_user_id_list_str.append(followed_user.user_id)

            # 根据followed_user_id_list_str，获取username
            followed_user_name_list_str = []
            for followed_user_id in followed_user_id_list_str:
                followed_user_name_list_str.append(User.objects.get(id=followed_user_id).username)

            # 判断user_id是否在followed_user_name_list_str里
            user_id = int(user_id)
            if user_id in followed_user_id_list_str:
                return JsonResponse({'isfollowed': True})
            else:
                return JsonResponse({'isfollowed': False})
        else:
            return JsonResponse({'result': '获取用户信息失败', 'reason': validate_result[1]})
    else:
        return JsonResponse({'result': '仅支持POST调用，获取用户信息失败'})


# 根据access_token修改用户信息
def modify_user_info(request):
    # 仅支持POST调用
    if request.method == 'POST':
        # 获取access_token
        access_token = request.POST.get('access_token')
        avatar_url = request.POST.get('avatar_url')
        self_introduction = request.POST.get('self_introduction')
        # 校验access_token
        validate_result = validate_access_jwt_intern(access_token)
        if validate_result[0]:
            # 获取当前用户
            current_user_str = validate_result[1]
            current_user = User.objects.get(username=current_user_str)
            current_user_id = current_user.id

            # 获取当前用户的DataLinker对象
            current_user_data_linker = DataLinker.objects.get_or_create(user_id=current_user_id)[0]

            # 修改用户信息
            current_user_data_linker.avatar_url = avatar_url
            current_user_data_linker.self_introduction = self_introduction
            current_user_data_linker.save()

            return JsonResponse({'result': '修改用户信息成功'})
        else:
            return JsonResponse({'result': '修改用户信息失败', 'reason': validate_result[1]})
    else:
        return JsonResponse({'result': '仅支持POST调用，修改用户信息失败'})
