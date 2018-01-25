import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from vkbot_schedule.message_handler import message_handler
from vkbot_schedule.settings import TOKEN, CONFIRMATION_TOKEN


@csrf_exempt
def bot_processing(request):
    data = json.loads(request.body)
    token = TOKEN
    confirmation_token = CONFIRMATION_TOKEN
    if 'type' not in data.keys():
        return HttpResponse('not vk')
    if data['type'] == 'confirmation':
        return HttpResponse(confirmation_token)
    elif data['type'] == 'message_new':
        message_handler(data['object'], token)
        return HttpResponse('ok')
