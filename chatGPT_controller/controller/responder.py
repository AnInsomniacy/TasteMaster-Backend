import json

import openai
import requests

openai.api_key = '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'
openai.api_base = 'https://service-i501wcby-1318284291.jp.apigw.tencentcs.com/v1'


# 主GPT函数，接收一个字符串，返回由GPT生成的字符串
def gpt_responder(user_content):
    # content是一个字符串，是用户输入的内容
    # 截断user_content，只保留1500个字符
    user_content = user_content[:1500]
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user',
             'content': user_content}
        ],
        temperature=0,

    )
    result = json.loads(str(response))  # 从结构体提取出字符串
    # 从结构体提取出字符串
    result_str = result['choices'][0]['message']['content']

    return result_str


def gpt_responder_stream(user_content):
    # content是一个字符串，是用户输入的内容
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user',
             'content': user_content}
        ],
        temperature=0,
        stream=True,

    )
    return response

# response = gpt_responder_stream('从1数到100')
# for i in response:
#     print(i)
