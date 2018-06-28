import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from vkbot_schedule.message_handler import message_handler
from vkbot_schedule.settings import CONFIRMATION_TOKEN


@csrf_exempt
def bot_processing(request):
    data = json.loads(request.body.decode())
    if 'type' not in data.keys():
        return HttpResponse('not vk')
    if data['type'] == 'confirmation':
        return HttpResponse(CONFIRMATION_TOKEN)
    elif data['type'] == 'message_new':
        message_handler(data['object'])
        return HttpResponse('ok')
