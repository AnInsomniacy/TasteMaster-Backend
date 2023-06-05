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


# 处理超过1000字的gpt函数，每次处理1000个字符，循环调用上面的gpt_responder函数，最后拼接成一个字符串
def gpt_responder_for_long_text(user_content):
    # content是一个字符串，是用户输入的内容
    # 把user_content分成1000个字符一组的列表
    user_content_list = []
    while len(user_content) > 1000:
        user_content_list.append(user_content[:1000])
        user_content = user_content[1000:]
    user_content_list.append(user_content)
    # 调用gpt_responder函数，把每个1000个字符的字符串传入，得到一个列表
    gpt_response_list = []
    for i in user_content_list:
        gpt_response_list.append(gpt_responder(i))
        print('已处理完1000个字符')
    # 把列表拼接成一个字符串
    gpt_response = ''
    for i in gpt_response_list:
        gpt_response += i
    return gpt_response


# user_content = '''
# 润色下述文字:
#
# 在编程领域，Python是一种功能强大且易于学习的编程语言。它具有简洁的语法结构和丰富的库，使得开发人员能够快速高效地编写代码。Python广泛应用于各个领域，包括Web开发、数据分析、人工智能等。
#
# 在接下来的内容中，我将为您提供一个有关Python的简短介绍，并介绍一些Python的优点和特点。
#
# 首先，Python具有简洁优雅的语法，使得代码易于阅读和理解。Python的语法规则非常清晰，使用空白符号来表示代码块，而不是使用大括号。这种语法特点使得代码看起来更加整洁，减少了语法错误的可能性。
#
# 其次，Python具有丰富的库和工具生态系统。Python拥有大量的第三方库和工具，可以帮助开发人员解决各种问题。例如，NumPy和Pandas库用于数据分析和科学计算，Django和Flask库用于Web开发，TensorFlow和PyTorch库用于机器学习等。这些库的存在极大地简化了开发过程，提高了开发效率。
#
# 另一个Python的优点是其跨平台性。Python可以在多个操作系统上运行，包括Windows、Linux和macOS。这意味着开发人员可以在不同的平台上使用相同的Python代码，无需进行太多修改。这种跨平台性使得Python成为开发多平台应用程序的理想选择。
#
# 此外，Python还支持面向对象编程（OOP）。面向对象编程是一种常用的编程范式，通过将数据和操作封装在对象中，使得代码更加模块化和可重用。Python的面向对象特性使得代码的组织更加清晰，可维护性更高。
#
# 另外，Python还有一项强大的功能是动态类型。Python是一种动态类型语言，这意味着在编写代码时无需指定变量的类型，变量的类型会根据赋值自动推导。这种特性使得Python非常灵活，可以快速迭代开发，并且减少了类型相关的错误。
#
# 总而言之，Python是一种简洁、易于学习且功能强大的编程语言。它具有丰富的库和工具生态系统，跨平台性好，支持面向对象编程和动态类型。这些特点使得Python成为广大开发人员的首选语言之一。
#
# 希望这个简短的Python介绍能让您对Python有更好的了解，并为您在学习和使用Python时提供一些帮助。
# '''
#
# response = gpt_responder_for_long_text(user_content)
# print(response)


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
