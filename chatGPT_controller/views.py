from django.http import JsonResponse

from chatGPT_controller.controller.responder import gpt_responder, gpt_responder_stream, gpt_responder_for_long_text
from get_jwt.jwt_controller import validate_access_jwt_intern


def gpt_for_chat(request):
    access_token = request.POST.get('access_token')
    gpt_message = request.POST.get('gpt_message')
    if request.method == 'POST':
        # 判断用户是否登录
        validate_result = validate_access_jwt_intern(access_token)
        if validate_result[0]:
            # 如果用户已登录，执行gpt_responder函数
            gpt_response = gpt_responder(gpt_message)
            return JsonResponse({'result': '成功', 'gpt_response': gpt_response})
        else:
            return JsonResponse({'result': '失败', 'reason': validate_result[1]})
    else:
        return JsonResponse({'result': '失败', 'reason': '请求方式错误'})


# def gpt_for_chat_stream(request):
#     access_token = request.POST.get('access_token')
#     gpt_message = request.POST.get('gpt_message')
#     if request.method == 'POST':
#         # 判断用户是否登录
#         validate_result = validate_access_jwt_intern(access_token)
#         if validate_result[0]:
#             # 如果用户已登录，执行gpt_responder函数
#             gpt_response = gpt_responder_stream(gpt_message)
#             return JsonResponse({'result': '成功', 'gpt_response': gpt_response})
#         else:
#             return JsonResponse({'result': '失败', 'reason': validate_result[1]})
#     else:
#         return JsonResponse({'result': '失败', 'reason': '请求方式错误'})


def gpt_for_chat_long_text(request):
    access_token = request.POST.get('access_token')
    gpt_message = request.POST.get('gpt_message')
    if request.method == 'POST':
        # 判断用户是否登录
        validate_result = validate_access_jwt_intern(access_token)
        if validate_result[0]:
            # 如果用户已登录，执行gpt_responder函数
            gpt_response = gpt_responder_for_long_text(gpt_message)
            return JsonResponse({'result': '成功', 'gpt_response': gpt_response})
        else:
            return JsonResponse({'result': '失败', 'reason': validate_result[1]})
    else:
        return JsonResponse({'result': '失败', 'reason': '请求方式错误'})
