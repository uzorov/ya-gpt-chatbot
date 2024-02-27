import json


def extract_text_from_response(response):

    print(response.text)

    data = json.loads(response.text)


    try:
        # Получение значения поля text из блока message
        text = data['result']['alternatives'][0]['message']['text']
    except KeyError:
        text = "Я не хочу говорить на эту тему"

    return text
