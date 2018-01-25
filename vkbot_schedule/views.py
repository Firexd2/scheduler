import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def bot_processing(request):
    data = json.loads(request.body)
    token = '5f268d3512f0bbd288530b0c551661ec4630a395ee6e21d852c07ef42603450b303e5bb95cee9e77c3087'
    confirmation_token = 'adcd62cf'
    if 'type' not in data.keys():
        return HttpResponse('not vk')
    if data['type'] == 'confirmation':
        return HttpResponse(confirmation_token)
    elif data['type'] == 'message_new':
        create_answer(data['object'], token)
        # Сообщение о том, что обработка прошла успешно
        return HttpResponse('ok')
